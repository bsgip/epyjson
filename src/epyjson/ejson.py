#! /usr/bin/env python3
# vim:tw=120:et

import copy
from dataclasses import dataclass
import importlib.resources
import json
import logging
import sys
from typing import Any, Callable, Generator, List, Optional, Tuple, Union

import networkx as nx
from ordered_set import OrderedSet

from .dumper import dump_pretty, dumps_pretty


logger = logging.getLogger(__name__)


sys.setrecursionlimit(100000)


def get_schema() -> dict:
    path = importlib.resources.files('epyjson') / 'e-json-schema.json'
    with path.open() as f:
        schema = json.load(f)

    return schema


def order_component_keys(c):
    '''
    Nicely order the keys in an e-JSON component dict as follows:
    id, type, cons, phs, everything ... else, user_data
    '''

    first = [k for k in ('id', 'type', 'cons', 'phs') if k in c]
    last = ['user_data'] if 'user_data' in c else []
    middle = [k for k in c if k not in first + last]

    retval = {}
    for ks in (first, middle, last):
        retval.update({k: c[k] for k in ks})

    return retval


class EJson:
    def __init__(self, ejson_dict: dict):
        '''
        Constructor for EJson object using an e-JSON dict.

        Args:
            ejson_dict: dict the input e-JSON dict dict
        '''

        self.properties = {k: v for k, v in ejson_dict.items() if k != 'components'}
        self._make_graph(ejson_dict)

    def _make_graph(self, ejson_dict):
        self.graph = nx.MultiGraph()

        cons = {}
        for c in _netw_components(ejson_dict):
            if 'cons' in c:
                cons[c['id']] = c['cons']

            self.add_comp(c)

        for k, v in cons.items():
            for i, con in enumerate(v):
                try:
                    node_id = con['node']
                    self.connect(k, node_id, i, {k: v for k, v in con.items() if k != 'node'})
                except KeyError as e:
                    logger.error(f'Connection to non-existent node {node_id} for component {c["id"]} '
                                 f'with cons {c["cons"]}')
                    raise e

    def __str__(self):
        return dumps_pretty(self.raw_ejson)

    def add_comp(self, comp: dict):
        _graph_add_node(self.graph, {k: v for k, v in comp.items() if k != 'cons'})

        return self

    def connect(self, elem_id: str, node_id: str, con_idx: int, con: dict):
        _graph_add_edge(self.graph, elem_id, node_id, con_idx, con)

        return self

    @staticmethod
    def read_from_file(path):

        with open(path) as f:
            d = json.load(f)

        return EJson(d)

    def write_to_file(self, path):
        with open(path, 'w+') as f:
            dump_pretty(self.raw_ejson, f)

        return self

    def clone(self):
        return copy.deepcopy(self)

    @property
    def raw_ejson(self):
        '''
        Access raw e-JSON dict.
        '''

        # Re-add the connections data
        comps = [copy.deepcopy(x) for x in self.components()]
        for i, c in enumerate(comps):
            if c['type'] != 'Node':
                c['cons'] = [{'node': x[1]} | x[3] for x in self.connections_from(c['id'])]
                comps[i] = order_component_keys(c)

        return self.properties | {'components': comps}

    def components(self, ctype: str = None, nodes_only: bool = False, elems_only: bool = False) -> Generator:
        '''
        Generator to iterate through components in network.

        Args:
            ctype: Optional filter(id_, type_, dict_) for components to be included

        Returns:
            Generator over component dicts
        '''

        retval = (v for k, v in self.graph.nodes(data='comp'))
        if ctype is not None:
            retval = (x for x in retval if x['type'] == ctype)

        if nodes_only:
            retval = (x for x in retval if x['type'] == 'Node')

        if elems_only:
            retval = (x for x in retval if x['type'] != 'Node')

        return retval

    def component(self, cid: str) -> dict:
        return self.graph.nodes[cid]['comp']

    def connections(self):
        '''
        Return all connections in the network

        Returns:
            ((component_1, component_2, terminal_idx, connection_data), ...)
            where terminal_idx is the index in the element's 'cons' array,
            e.g. for a line or transformer with two terminals, terminal_idx
            could be either 0 or 1
        '''

        return (x for x in self.graph.edges(keys=True, data='con'))

    def connections_from(self, cid: str):
        '''
        Return all connections from cid

        Args:
            cid: The component we want to find connections from

        Returns:
            ((cid, connected_component, terminal_idx, connection_data), ...)
            where terminal_idx is the index in the element's 'cons' array,
            e.g. for a line or transformer with two terminals, terminal_idx
            could be either 0 or 1
        '''

        return (x for x in self.graph.edges(cid, keys=True, data='con'))

    def connections_between(self, cid_a: str, cid_b: str):
        '''
        Return generator of all connections between cid_a and cid_b

        Args:
            cid_a: The first component we want to find connections between
            cid_b: The second component we want to find connections between

        Returns:
            ((cid_a, cid_b, terminal_idx, connection_data), ...)
            where terminal_idx is the index in the element's 'cons' array,
            e.g. for a line or transformer with two terminals, terminal_idx
            could be either 0 or 1
        '''

        try:
            return ((cid_a, cid_b, k, v['con']) for k, v in self.graph.adj[cid_a][cid_b].items())
        except KeyError:
            return (x for x in ())

    def neighbors(self, cid: str):
        return self.graph.neighbors(cid)

    def reconnect_elem(self, cid, node_remap: dict):
        cons = list(list(x) for x in self.connections_from(cid))

        for con in cons:
            self.graph.remove_edge(con[0], con[1], con[2])

            for k, v in node_remap.items():
                if con[1] == k:
                    con[1] = v

        for con in cons:
            self.connect(*con)

        return self

    def remove_component(self, cid: str):
        '''
        Remove a component.
        '''

        self.graph.remove_node(cid)
        return self

    def remove_unconnected_nodes(self):
        '''
        Removes unconnected nodes from the graph
        '''
        to_remove = []
        for c in self.components(nodes_only=True):
            if len(list(self.connections_from(c['id']))) == 0:
                to_remove.append(c['id'])

        for cid in to_remove:
            self.remove_component(cid)

    def dfs(
        self,
        start: Union[dict, str],
        pre_cb: Optional[Callable] = None,
        stop_cb: Optional[Callable] = None,
        accum_cb: Optional[Callable] = None,
        post_cb: Optional[Callable] = None,
        accum: Any = None
    ) -> Tuple[List[dict], Any]:

        '''
        Depth first search on the network graph. Starting from start, follow the graph, adding to visited for each
        visited graph node. Before visiting a node, call pre_cb which returns (stop, accum), which seves two
        purposes: (1) decide if we want to visit the node, returning the decision in stop, and (2) modify accum if
        desired, returning the modified value in accum. stop_cb or accum_cb may be given in place of pre_cb as
        described below. After a node has been visited (and after its descendents have all been visited), a further
        callback may be called, post_cb, which can modify accum as described below.

        Args:
            start: cid of start component
            pre_cb(ejson, curr_comp, accum): Callback when node is pushed, return (stop, accum).
            stop_cb(ejson, curr_comp): Convenience alternative to pre_cb without accum, return stop.
            accum_cb(ejson, curr_comp, accum): Convenience alternative to pre_cb without stop, return accum.
            post_cb(ejson, curr_comp, accum): Callback when node is about to be popped, return accum.

        Returns:
            (visited, accum): set of visited nodes and accumulated value
        '''

        if type(start) is dict:
            start = start['id']

        if stop_cb is not None:
            # Defines pre_callback with return value in format (bool, None)
            assert pre_cb is None and accum_cb is None

            def pre_cb(netw, curr_comp, accum):
                return (stop_cb(netw, curr_comp), None)

        if accum_cb is not None:
            # Defines pre_callback with return value in format (False, int)
            assert pre_cb is None and stop_cb is None

            def pre_cb(netw, curr_comp, accum):
                return (False, accum_cb(netw, curr_comp, accum))

        visited = OrderedSet()

        return self._dfs(start, pre_cb, post_cb, visited, accum)

    def _dfs(
        self,
        curr_comp_id: str,
        pre_cb: Optional[Callable],
        post_cb: Optional[Callable],
        visited: OrderedSet,
        accum: Any
    ) -> Tuple[List[str], Any]:

        if (curr_comp_id in visited):
            return visited, accum

        curr_comp = self.component(curr_comp_id)

        if pre_cb is not None:
            stop, accum = pre_cb(self, curr_comp, accum)
            if stop:
                return visited, accum

        visited.add(curr_comp_id)
        for _, adj_comp, _, con in self.connections_from(curr_comp_id):
            visited, accum = self._dfs(adj_comp, pre_cb=pre_cb, post_cb=post_cb, visited=visited, accum=accum)

        if post_cb is not None:
            accum = post_cb(self, curr_comp, accum)

        return visited, accum

    def reorder(self, start_id: str):
        '''
        Reorder the components in the network, according to a depth-first search.

        Args:
            ejson: e-JSON network
            start_id: starting component for the depth first search.

        Returns:
            Reordered network.
        '''

        ordering = {n: i for i, n in enumerate(nx.dfs_preorder_nodes(self.graph, source=start_id))}
        new_graph = nx.MultiGraph()
        new_graph.add_nodes_from((k, {'comp': self.component(k)}) for k in ordering.keys())

        # Re-order connections. Don't mess with transformer ordering as this would swap primary and secondary.
        for _, c in new_graph.nodes(data='comp'):
            if c['type'] != 'Node':
                cons = list(self.connections_from(c['id']))

                if c['type'] != 'Transformer':
                    cons = sorted(cons, key=lambda x: ordering[x[1]])

                for i, con in enumerate(cons):
                    new_graph.add_edge(con[0], con[1], key=i, con=con[3])

        self.graph = new_graph

        return self

    def trim(self, start_id: str, stop_cb: Callable = None):
        '''
        Remove selected components.

        Args:
            graph: e-JSON graph, result of make_graph(...)
            start_id: ID of the starting component for depth first search
            stop_cb: Callback to decide where to prune the depth first search

        Returns:
            The mutated graph

        '''
        visited, _ = self.dfs(start_id, stop_cb=stop_cb)
        for cid in visited:
            self.remove_component(cid)

        self.remove_unconnected_nodes()

        return self

    def only(self, start_id: str, stop_cb: Callable = None):
        '''
        Keep only selected components.

        Args:
            graph: e-JSON graph, result of make_graph(...)
            start_id: ID of the starting component for depth first search
            stop_cb: Callback to decide where to prune the depth first search

        Returns:
            The mutated graph
        '''
        visited, _ = self.dfs(start_id, stop_cb=stop_cb)

        remove = (c['id'] for c in list(self.components()) if c['id'] not in visited)
        for cid in remove:
            self.remove_component(cid)

        self.remove_unconnected_nodes()

        return self

    def rename(self):
        '''
        Rename according to a standard naming scheme.

        Returns:
            New graph with renamed components.
        '''

        i_dict = {}
        rename_dict = {}
        for c in self.components():
            prefix_a = c['type'].lower()
            i = i_dict.setdefault(prefix_a, 1)
            i_dict[prefix_a] += 1
            rename_dict[c['id']] = f'{prefix_a}_{i}'

        return (self.rename_to(rename_dict), rename_dict)

    def rename_to(self, rename_dict: dict):
        '''
        Rename according to a provided dict.

        Args:
            rename_dict: {old_name: new_name} mapping.

        Returns:
            New graph with renamed components.
        '''

        self.graph = nx.relabel_nodes(self.graph, rename_dict)
        for cid, cdat in self.graph.nodes(data='comp'):
            cdat['id'] = cid

        return self


def _netw_components(netw_ejson, ctype: str = None) -> Generator:
    '''
    Generator to iterate through components in an e-JSON network.

    Args:
        ctype: Optional filter on component type for components to be included

    Returns:
        Generator with elements
    '''

    return (x for x in netw_ejson['components']) if ctype is None else \
           (x for x in netw_ejson['components'] if x[1] == ctype)


def _graph_add_node(graph: nx.MultiGraph, c: dict):
    graph.add_node(c['id'], comp=c)


def _graph_add_edge(graph: nx.MultiGraph, elem_id: str, node_id: str, con_idx: int, con: dict):
    graph.add_edge(elem_id, node_id, key=con_idx, con=con)
