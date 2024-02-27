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


logger = logging.getLogger(__name__)


sys.setrecursionlimit(100000)


def get_schema() -> dict:
    path = importlib.resources.files('epyjson') / 'e-json-schema.json'
    with path.open() as f:
        schema = json.load(f)

    return schema


@dataclass
class Component:
    cid: str
    ctype: str
    cdata: dict

    def is_in_service(self):
        return self.cdata.get('in_service', True)

    def is_node(self):
        return self.ctype == 'Node'

    def is_elem(self):
        return not self.is_node()

    @property
    def user_data(self):
        '''
        Access user_data key, setting to an empty dict if not present.
        '''
        return self.cdata.setdefault('user_data', {})


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
        for cid, ctype, cdata in _netw_components(ejson_dict):
            if 'cons' in cdata:
                cons[cid] = cdata['cons']

            self.add_comp(cid, ctype, cdata)

        for k, v in cons.items():
            for i, con in enumerate(v):
                try:
                    node_id = con['node']
                    self.connect(k, node_id, i, {k: v for k, v in con.items() if k != 'node'})
                except KeyError as e:
                    logger.error(f'Connection to non-existent node {node_id} for component {cid} '
                                 f'with cons {cdata["cons"]}')
                    raise e

    def __str__(self):
        return json.dumps(self.raw_ejson, indent=2)

    def add_comp(self, cid: str, ctype: str, cdata: dict):
        _graph_add_node(self.graph, cid, ctype, {k: v for k, v in cdata.items() if k != 'cons'})

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
            json.dump(self.raw_ejson, f, indent=True)

        return self

    def clone(self):
        return copy.deepcopy(self)

    @property
    def raw_ejson(self):
        '''
        Access raw e-JSON dict.
        '''

        # Re-add the connections data
        comps = {}
        for c in self.components():
            if c.is_elem():
                add_cons = {'cons': [{'node': x[1]} | x[3] for x in self.connections_from(c.cid)]}
                comps[c.cid] = {c.ctype: c.cdata | add_cons}
            else:
                comps[c.cid] = {c.ctype: c.cdata}

        return self.properties | {'components': comps}

    def components(self, ctype: str = None, nodes_only: bool = False, elems_only: bool = False) -> Generator:
        '''
        Generator to iterate through components in network.

        Args:
            ctype: Optional filter(id_, type_, dict_) for components to be included

        Returns:
            Generator over Component objects
        '''

        retval = (v for k, v in self.graph.nodes(data='comp'))
        if ctype is not None:
            retval = (x for x in retval if x.ctype == ctype)

        if nodes_only:
            retval = (x for x in retval if x.ctype == 'Node')

        if elems_only:
            retval = (x for x in retval if x.ctype != 'Node')

        return retval

    def component(self, cid: str) -> Component:
        return self.graph.nodes[cid]['comp']

    def connections(self):
        return (x for x in self.graph.edges(keys=True, data='con'))

    def connections_from(self, cid: str):
        '''
        Return all connections from cid

        Args:
            cid: The component we want to find connections from

        Returns:
            ((connected_component, connection_data), ...)
        '''

        return (x for x in self.graph.edges(cid, keys=True, data='con'))

    def connections_between(self, cid_a: str, cid_b: str):
        '''
        Return generator of all connections between cid_a and cid_b

        Args:
            cid_a: The first component we want to find connections between
            cid_b: The second component we want to find connections between

        Returns:
            (connection_data, ...)
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
            if len(list(self.connections_from(c.cid))) == 0:
                to_remove.append(c.cid)

        for cid in to_remove:
            self.remove_component(cid)

    def dfs(
        self,
        start: Union[Component, str],
        pre_cb: Optional[Callable] = None,
        stop_cb: Optional[Callable] = None,
        accum_cb: Optional[Callable] = None,
        post_cb: Optional[Callable] = None,
        accum: Any = None
    ) -> Tuple[List[Component], Any]:

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

        if type(start) is Component:
            start = start.cid

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
            if c.ctype != 'Node':
                cons = list(self.connections_from(c.cid))

                if c.ctype != 'Transformer':
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

        remove = (c.cid for c in list(self.components()) if c.cid not in visited)
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
            prefix_a = c.ctype.lower()
            i = i_dict.setdefault(prefix_a, 1)
            i_dict[prefix_a] += 1
            rename_dict[c.cid] = f'{prefix_a}_{i}'

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
            cdat.cid = cid

        return self


def _netw_components(netw_ejson, ctype: str = None) -> Generator:
    '''
    Generator to iterate through components in an e-JSON network as (cid, ctype, cdata).

    Args:
        ctype: Optional filter on component type for components to be included

    Returns:
        Generator with elements of the form (cid, ctype, cdata).
    '''

    retval = ((k, next(iter(v.keys())), next(iter(v.values()))) for k, v in netw_ejson['components'].items())
    if ctype is not None:
        retval = (x for x in retval if x[1] == ctype)

    return retval


def _graph_add_node(graph: nx.MultiGraph, cid: str, ctype: str, cdata: dict):
    graph.add_node(cid, comp=Component(cid, ctype, cdata))


def _graph_add_edge(graph: nx.MultiGraph, elem_id: str, node_id: str, con_idx: int, con: dict):
    graph.add_edge(elem_id, node_id, key=con_idx, con=con)
