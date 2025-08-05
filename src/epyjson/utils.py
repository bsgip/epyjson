import copy
from ordered_set import OrderedSet
from typing import Sequence, List

import jsonschema
import math
import networkx as nx
import numpy as np

from .ejson import get_schema, EJson, logger


def a2c(a: Sequence[float]) -> complex:
    '''
    Convert an array [re, im] to a complex.

    Args:
        a: Array-like quantity containing [re, im] components.

    Returns:
        Complex number
    '''

    return complex(*a)


def c2a(c: complex) -> List[float]:
    '''
    Convert a complex to an array [re, im].

    Args:
        c: Complex number

    Returns:
        [c.real, c.imag]
    '''

    return [float(c.real), float(c.imag)]  # Make sure we return regular float, not np.float64


def user_data(comp: dict) -> dict:
    '''
    Return component's user_data, or empty dict by default.

    Args:
        comp: component dict
    
    Returns:
        Component's user_data, or {} if absent
    '''
    return comp.get('user_data', {})


def is_in_service(comp: dict) -> bool:
    '''
    Return compnent's in_service property, or True if absent 

    Args:
        comp: component dict
    
    Returns:
        True iff the component is in service
    '''
    
    return comp.get('in_service', True)


def switch_state(comp: dict) -> str:
    '''
    Return compnent's switch_state property, or 'no_switch' if absent 

    Args:
        comp: component dict
    
    Returns:
        String specifying component's switch_state
    '''
    return comp.get('switch_state', 'no_switch')


def is_closed(comp: dict) -> bool:
    '''
    Return False if component's switch_state is 'open', or True otherwise

    Args:
        comp: component dict
    
    Returns:
        True iff the component has a closed switch or is unswitched
    '''
    return switch_state(comp) != 'open'


def is_live(comp: dict) -> bool:
    '''
    Return True if the component is electrically live (in service and switch
    closed), or False otherwise

    Args:
        comp: component dict
    
    Returns:
        True iff the component is electrically live.
    '''
    return is_in_service(comp) and is_closed(comp)


def remove_hanging_nodes(netw: EJson) -> EJson:
    '''
    Remove hanging nodes: a node that terminates a line and has no other attached components.

    Args:
        netw: eJson network

    Returns:
        in-place mutated network
    '''
    to_remove = []
    for comp in netw.components('Node'):
        adj = list(netw.connections_from(comp['id']))
        if len(adj) == 1:
            comp_to = netw.component(adj[0].cid_1)
            if comp_to['type'] in ('Line', 'Connector'):
                if len(list(netw.connections_from(comp_to['id']))) <= 2:
                    # Connectors could have any number of terminals.
                    to_remove.append(comp['id'])
                    to_remove.append(comp_to['id'])

    for cid in to_remove:
        netw.remove_component(cid)

    return netw


def remove_not_live(netw: EJson) -> EJson:
    '''
    Remove components that are not live.

    Args:
        netw: eJson network

    Returns:
        in-place mutated network
    '''

    for comp in list(netw.components()):
        if not is_live(comp):
            netw.remove_component(comp['id'])

    netw.remove_unconnected_nodes()
    
    return netw


def collapse_elem(netw: EJson, cid: str) -> EJson:
    '''
    Remove component cid (normally a connector or line) and coalesce the second
    and subsequent connected nodes into the first connected node.

    Args:
        netw: eJson network

    Returns:
        in-place mutated network
    '''

    cons = list(netw.connections_from(cid))
    netw.remove_component(cid)
    nodes = [x.cid_1 for x in cons]
    node_0 = nodes[0]
    other_nodes = [x for x in nodes[1:] if x != node_0]  # Guard against circular connections, just in case.
    for node in other_nodes:
        for con in list(netw.connections_from(node)):
            netw.reconnect_elem(con.cid_1, {node: nodes[0]})

    for node in other_nodes:
        assert len(list(netw.connections_from(node))) == 0
        netw.remove_component(node)
    
    return netw


def coalesce_connectors(
        netw: EJson, coalesce_switched: bool = True, coalesce_two_term: bool = True
) -> EJson:
    '''
    Coalesce switches and connectors - removing them where switches are open
    or the component is out of service, and thereafter merging all associated
    nodes.

    Args:
        netw: eJson network
        coalesce_switched: Whether to coalesce connectors that have a switch (default: True)
        coalesce_two_term: Whether to coalesce "branch-like" connectors that have two terminals (default: True)

    Returns:
        in-place mutated network
    '''

    for comp in list(netw.components('Connector')):
        if not coalesce_switched and 'switch_state' in comp and comp['switch_state'] != "no_switch":
            continue

        if not coalesce_two_term and len(list(netw.connections_from(comp['id']))) == 2:
            continue

        if is_live(comp):
            collapse_elem(netw, comp['id'])
        else:
            con_nds = [x.cid_1 for x in netw.connections_from(comp['id'])]
            netw.remove_component(comp['id'])
            for con_nd in con_nds:
                if len(list(netw.connections_from(con_nd))) == 0:
                    netw.remove_component(con_nd)

    return netw


def merge_short_circuits(netw: EJson) -> EJson:
    '''
    Merge short circuit lines where possible.

    A short circuit line is a line that fully short circuits all phases between two nodes. In such cases, we can
    simply remove the line and merge the two nodes.
    
    Args:
        netw: eJson network

    Returns:
        in-place mutated network
    '''

    merges = [l['id'] for l in netw.components('Line') if is_short_circuit(l, netw)]

    for cid in merges:
        collapse_elem(netw, cid)

    return netw


def is_zero_impedance(comp: dict) -> bool:
    '''
    Returns True if line length is zero OR all impedance values are zero.

    Args:
        comp: dict for a Line.

    Returns:
        boolean value that is true iff the line is zero length or has z == z0 == 0.
    '''

    return is_live(comp) and (
        comp['length'] == 0.0 or (
            all(value == 0.0 for value in comp['z']) and all(value == 0.0 for value in comp['z0'])
        )
    )


def is_short_circuit(comp: dict, netw: EJson) -> bool:
    '''
    Returns True if a line short circuits ALL phases between its nodes.

    Args:
        comp: dict for a Line.
        netw: eJson network

    Returns:
        boolean value that is true iff the line is zero impedance and connects all phases between its two nodes.
    '''

    if not is_zero_impedance(comp):
        return False

    l_phs = [con.con['phs'] for con in netw.connections_from(comp['id'])]
    nds = [netw.component(con.cid_1) for con in netw.connections_from(comp['id'])]
    nd_phs = [x['phs'] for x in nds]
    return l_phs == nd_phs


def merge_dups(netw: EJson) -> EJson:
    '''
    Merge duplicated lines.
    
    Args:
        netw: eJson network

    Returns:
        in-place mutated network
    '''

    all_lines = list(netw.components('Line'))

    dups = {}
    for comp in all_lines:
        cons = netw.connections_from(comp['id'])
        cons_sorted = sorted(cons, key=lambda con: f'{con.cid_1}:{con.term_idx}')
        con_nids = [x.cid_1 for x in cons_sorted]
        con_phs = [','.join(x.con['phs']) for x in cons_sorted]
        service_status = str(is_in_service(comp)) + str(is_closed(comp))
        k = '|'.join([','.join(x) for x in zip(con_nids, con_phs)] + [service_status])
        dups.setdefault(k, []).append(comp)

    dups = [v for k, v in dups.items() if len(v) > 1]

    def ys(l):
        z = a2c(l['z'])
        z0 = a2c(l['z0'])
        if z0 == 0.0 and z != 0.0:
            # KLUDGE: To avoid NaN in this situation, we can assume z0 = z.
            z0 = z

        return 1.0 / (l['length'] * np.array([z, z0]))

    for dup in dups:
        # We know that all lines in dup have the same nodes, the same service status and the same phasing.
        min_length = min([x['length'] for x in dup])
        l0 = dup[0]
        drop = []
        ys_merged = ys(l0)
        for l in dup[1:]:
            ys_merged += ys(l)
            drop.append(l['id'])

        for x in drop:
            netw.remove_component(x)

        zs_merged = (1.0 / ys_merged) / min_length

        l0['z'] = [zs_merged[0].real, zs_merged[0].imag]
        l0['z0'] = [zs_merged[1].real, zs_merged[1].imag]
        l0['length'] = min_length

    return netw


def _get_strings(netw: EJson) -> EJson:
    g = netw.graph

    subg: nx.MultiGraph = g.subgraph(
        k for k, v in g.nodes(data='comp') if v['type'] in ('Node', 'Line', 'Connector') and g.degree(k) == 2
    )

    def ensure_correct_degree(subg):
        # Nodes should have degree 2 in the subgraph
        subg: nx.MultiGraph = subg.subgraph(
            k for k, v in subg.nodes(data='comp') if v['type'] != 'Node' or subg.degree(k) == 2
        )
        
        # Elements should have degree > 0 in the subgraph 
        subg: nx.MultiGraph = subg.subgraph(k for k in subg.nodes() if subg.degree(k) != 0)
        return subg

    subg = ensure_correct_degree(subg)

    # Remove nodes or edges where there is a phasing mismatch. A mismatch at a node compoment means two adjacent
    # lines / connectors are differently connected. A mismatch at an element component means there is a transposition.
    # In either case, remove the component in question from consideration to be part of a string.
    keep = set()
    for nd in sorted(subg.nodes):
        edges = list(g.edges(nd, keys=True, data='con')) # Note: this may include edges to nodes not in subg
        assert len(edges) == 2
        phs0 = edges[0][3]['phs']
        phs1 = edges[1][3]['phs']
        if phs0 == phs1:
            keep.add(nd)

    subg = ensure_correct_degree(subg.subgraph(keep))

    strings = []

    for cc in nx.connected_components(subg):
        cc_subg = subg.subgraph(cc)
        ends = sorted(x for x in cc_subg.nodes if cc_subg.degree(x) == 1)
        if len(ends) == 0:
            # This must be a circular string: rare but a logical possibility
            # Simply break the string at any node and everything should be OK.
            nds = sorted(x for x in cc_subg.nodes if netw.component(x)['type'] == 'Node')
            cc_subg = cc_subg.subgraph(x for x in cc_subg if x != nds[0])
            if len(cc_subg.nodes()) < 3:
                # We want at least 2 lines or connectors separated by at least 1 node
                continue

            ends = sorted(x for x in cc_subg.nodes if cc_subg.degree(x) == 1)
        
        assert len(ends) == 2
        assert len(cc_subg.nodes) >= 3

        start, end = ends
        ord = list(nx.dfs_preorder_nodes(cc_subg, source=start))

        # Add on the two external nodes for convenience
        node_0 = [x for x in g.neighbors(start) if x not in cc_subg.nodes][0]
        node_1 = [x for x in g.neighbors(end) if x not in cc_subg.nodes][0]
        ord = [netw.component(x) for x in [node_0] + ord + [node_1]]

        phs = list(g[ord[0]['id']][ord[1]['id']].values())[0]['con']['phs']

        assert ord[0]['type'] == 'Node'
        assert ord[1]['type'] in ('Line', 'Connector')
        assert ord[-1]['type'] == 'Node'
        assert ord[-2]['type'] in ('Line', 'Connector')

        strings.append((ord, phs))

    # Order strings by the first component ID to ensure deterministic behaviour.
    if len(strings) > 0:
        strings = sorted(strings, key = lambda x: x[0][0]['id'])

    return strings


def _ud_is_merged(ud):
    return list(ud.keys()) == ['merged_user_data']


def _ud_list(lid, ud):
    return list(ud['merged_user_data'].items()) if _ud_is_merged(ud) else [(lid, ud)]


def _merge_ud(comps):
    return {'merged_user_data': dict(sum((_ud_list(x['id'], user_data(x)) for x in comps), []))}


def _merge_string(string: list, merge_i):
    lines = [x for x in string if x['type'] == 'Line']
    connectors = [x for x in string if x['type'] == 'Connector']
    nodes = [x for x in string if x['type'] == 'Node']

    new_is_in_service = all(is_in_service(x) for x in lines)
    has_switch = any(switch_state(x) != 'no_switch' for x in connectors)
    is_closed = all(switch_state(x) != 'open' for x in connectors)
    new_switch_state = ('closed' if is_closed else 'open') if has_switch else 'no_switch'

    new_line = None
    if len(lines) > 0:
        ls = np.array([x['length'] for x in lines])
        l_tot = float(sum(ls))
        zs = np.array([a2c(x['z']) for x in lines])
        z0s = np.array([a2c(x['z0']) for x in lines])
        any_bs = any('b_chg' in x for x in lines)
        bs = np.array([a2c(x['b_chg']) if 'b_chg' in x else 0.0 + 0.0j for x in lines]) if any_bs else None

        new_line = copy.deepcopy(lines[0])
        new_line['id'] = f'merge-{merge_i}-line'
        new_line['length'] = l_tot
        new_line['z'] = c2a(sum(zs * ls) / l_tot)
        new_line['z0'] = c2a(sum(z0s * ls) / l_tot)
        if any_bs:
            new_line['b_chg'] = c2a(sum(bs * ls) / l_tot)
        new_line['in_service'] = new_is_in_service
        new_line['user_data'] = _merge_ud(lines)
    
    new_connector = None
    if len(connectors) > 0:
        new_connector = copy.deepcopy(connectors[0])
        new_connector['id'] = f'merge-{merge_i}-connector'
        new_connector['in_service'] = new_is_in_service
        new_connector['switch_state'] = new_switch_state

    if new_line is not None and new_connector is not None:
        new_node = copy.deepcopy(nodes[1])
        new_node['id'] = f'merge-{merge_i}-node'
    else:
        new_node = None

    retval = [string[0]]

    if new_connector is not None:
        retval.append(new_connector)

    if new_node is not None:
        retval.append(new_node)

    if new_line is not None:
        retval.append(new_line)

    retval.append(string[-1])
   
    return retval


def merge_strings(netw: EJson) -> EJson:
    '''
    Merge strings of lines where possible.

    A string is a (line, node, ... , node, line) sequence whose nodes do not connect to any other elements in the
    sequence, and whose connection phasings are all the same.

    Args:
        netw: eJson network
    
    Returns:
        in-place mutated network
    '''

    strings = _get_strings(netw)
    merge_ids = [x['id'] for x in netw.components() if x['id'].startswith('merge-')] 
    merge_i = max(int(x.split('-')[1]) for x in merge_ids) + 1 if len(merge_ids) > 0 else 0
    for string, phs in strings:
        merged = _merge_string(string, merge_i)

        for c in string[1:-1]:
            netw.remove_component(c['id'])

        for c in merged[1:-1]:
            netw.add_comp(c)
        
        for nd, elem in zip(merged[0:-1:2], merged[1::2]):
            netw.connect(nd['id'], elem['id'], 0, {'phs': phs})
        for nd, elem in zip(merged[2::2], merged[1::2]):
            netw.connect(nd['id'], elem['id'], 1, {'phs': phs})
        
        merge_i += 1

    return netw


def reduce_network(netw: EJson) -> EJson:
    '''
    Reduce the size of the network by telescoping lines together, merging duplicated lines and removing unused spurs.

    Args:
        netw: eJson network
    
    Returns:
        in-place mutated network
    '''

    def report_stats(netw: EJson, prefix: str, log=logger.debug):
        l = 0.0
        for line in netw.components('Line'):
            l += line['length']

        by_type = {}
        for c in netw.components():
            by_type.setdefault(c['type'], 0)
            by_type[c['type']] += 1

        log(f'    {prefix}:')
        log(f'        Total line length = {l}')
        for t, n in by_type.items():
            log(f'        Number of {t}s = {n}')

    for line in netw.components('Line'):
        line.setdefault('user_data', {})['orig_ids'] = [line['id']]

    report_stats(netw, 'Initial', logger.info)
    while True:
        n = len(netw.graph.nodes)

        merge_strings(netw)
        report_stats(netw, 'After merge strings')

        remove_hanging_nodes(netw)
        report_stats(netw, 'After remove hanging')

        merge_short_circuits(netw)
        report_stats(netw, 'After merge short circuits')

        merge_dups(netw)
        report_stats(netw, 'After merge dups')

        if len(netw.graph.nodes) == n:
            break

    report_stats(netw, 'Final', logger.info)
    
    return netw


def remove_unsupplied(netw: EJson) -> EJson:
    '''
    Remove unsupplied components from the network, i.e. those that are not
    connected to an infeeder via a live path.

    Args:
        netw: the EJson network
    
    Returns:
        in-place mutated network
    '''

    connected = OrderedSet()
    for infeeder in netw.components('Infeeder'):
        if is_live(infeeder):
            visited, _ = netw.dfs(infeeder, stop_cb=lambda _, comp: not is_live(comp))
            connected.update(visited)

    netw.graph.remove_nodes_from([n for n in netw.graph if n not in connected])

    return netw


def _upstream_txs_cb(_, comp, accum):
    if not is_live(comp):
        return True, accum
    elif comp['type'] == 'Transformer':
        accum.append(comp['id'])
        return (True, accum)
    else:
        return (False, accum)

def annotate_upstream_transformers(netw: EJson, comp_types: list[str]) -> EJson:
    '''
    For selected component types, annotate components with a list of all
    live-connected upstream transformers. Only those immediately upstream are
    included, e.g. we stop the depth first search branch after finding a
    transformer.
    
    Args:
        netw: the EJson network
    
    Returns:
        in-place mutated network
    '''
    for comp_type in comp_types:
        for comp in netw.components(comp_type):
            _, txs = netw.dfs(comp, pre_cb=_upstream_txs_cb, accum=[])
            comp.setdefault("user_data", {})["upstream_txs"] = txs


def add_map(netw: EJson, points: Sequence[dict]) -> EJson:
    '''
    Given 2 or 3 points with both (x, y) and (lat, lon), find the transformation A, b st. latlon = A xy + b
    Then add the missing information, e.g. add xy if a node has lat_long or vice-versa.

    Args:
        netw: the EJson network
        points: list of points, [{'x': <x>, 'y': <y>, 'lat': <lat>, 'lon': <lon>}, ...]
    
    Returns:
        in-place mutated network
    '''

    x = [p['x'] for p in points]
    y = [p['y'] for p in points]
    lat = [p['lat'] for p in points]
    lon = [p['lon'] for p in points]
    if len(points) == 2:
        a00 = 0
        a01 = (lat[0] - lat[1]) / (y[0] - y[1])
        a10 = (lon[0] - lon[1]) / (x[0] - x[1])
        a11 = 0
        b0 = lat[0] - a01 * y[0]
        b1 = lon[0] - a10 * x[0]
    elif len(points) == 3:
        A = np.array(
            [
                [x[0], y[0],    0,    0,    1,    0],
                [   0,    0,    x[0], y[0], 0,    1],
                [x[1], y[1],    0,    0,    1,    0],
                [   0,    0,    x[1], y[1], 0,    1],
                [x[2], y[2],    0,    0,    1,    0],
                [   0,    0,    x[2], y[2], 0,    1]
            ]
        )
        rhs = np.array([lat[0], lon[0], lat[1], lon[1], lat[2], lon[2]])
        a00, a01, a10, a11, b0, b1 = np.linalg.solve(A, rhs)
    else:
        exit('Map must have either 2 or three test points.')

    A = np.array([[a00, a01], [a10, a11]])
    A_inv = np.linalg.inv(A)
    b = np.array([b0, b1])

    for c in netw.components('Node'):
        if 'lat_long' in c:
            c['xy'] = (A_inv @ (np.array(c['lat_long']) - b)).tolist()
        elif 'xy' in c:
            c['lat_long'] = (A @ np.array(c['xy']) + b).tolist()
    
    return netw


def _add_missing_locs_cb(netw, comp, accum, key):
    found = comp['type'] == 'Node' and key in comp
    if found:
        accum.append(comp[key])

    return (found, accum)


def add_missing_locations(netw: EJson, keys=['xy', 'lat_long']) -> EJson:
    '''
    Add missing locations by averaging the graph theoretic nearest locations.

    Args:
        netw: the EJson network
        keys: list containing elements of 'xy' and 'lat_long' to patch missing
    
    Returns:
        in-place mutated network
    '''
    for key in keys:
        all_poss = (nd[key] for nd in netw.components('Node') if key in nd)
        default = [sum(xs) / len(xs) for xs in zip(*all_poss)]

        nds_without_key = [nd for nd in netw.components('Node') if key not in nd]
        for nd in nds_without_key:
            _, poss = netw.dfs(
                nd['id'],
                pre_cb=lambda netw, comp, accum: _add_missing_locs_cb(netw, comp, accum, key),
                accum=[]
            )
            nd[key] = [sum(xs) / len(xs) for xs in zip(*poss)] if len(poss) > 0 else default

    return netw


def make_radial(netw: EJson, start_id: str) -> EJson:
    '''
    Break cycles, making the graph radial.

    Args:
        netw: EJson network
        start_id: Depth first search starting component.
    
    Returns:
        in-place mutated network
    '''

    # The code assumes everything is correctly ordered. Do it in case it hasn't already been done.
    netw.reorder(start_id)

    def pre_cb(netw: EJson, cur: dict, accum: list):
        if not is_live(cur):
            return (True, accum)

        if cur['type'] == 'Line':
            nd1 = list(netw.connections_from(cur['id']))[1].cid_1
            if nd1 in accum[0]:
                accum[1].append(cur['id'])
                return (True, accum)

        elif cur['type'] == 'Node':
            accum[0].append(cur['id'])

        return (False, accum)

    def post_cb(netw: EJson, cur: dict, accum: list):
        if cur['type'] == 'Node':
            accum[0].pop()

        return accum

    accum = ([], [])  # (stack_of_seen_nodes, to_remove)

    _, (_, to_remove) = netw.dfs(start_id, pre_cb=pre_cb, post_cb=post_cb, accum=accum)

    for cid in to_remove:
        netw.remove_component(cid)
    
    return netw


def make_single_phased(netw: EJson) -> EJson:
    '''
    Given a three / multi phase network, convert to a single phase balanced network.

    We use a system where:
        - voltages are line to line,
        - currents are sqrt(3) * the line current,
        - load power is total three phase power,
        - line impedances are modified to put z0 -> z.
        - delta shunt impedances become shunts scaled by 1/3.

    Args:
        netw: e-JSON network
    
    Returns:
        in-place mutated network
    '''

    s3 = math.sqrt(3.0)

    comps = list(netw.components())
    nodes = [x for x in comps if x['type'] == 'Node']
    elems = [x for x in comps if x['type'] != 'Node']
    lines = [x for x in elems if x['type'] == 'Line']
    txs = [x for x in elems if x['type'] == 'Transformer']
    infs = [x for x in elems if x['type'] == 'Infeeder']
    loads = [x for x in elems if x['type'] == 'Load']

    v_mult = s3 if netw.properties['voltage_type'] == 'lg' else 1.0
    netw.properties['voltage_type'] = 'lg'

    for line in lines:
        cons = list(netw.connections_from(line['id']))
        assert len(cons) == 2
        nph = len([x for x in cons[0].con['phs'] if x.lower() not in 'ng'])
        line['z'] = [x * 3 / nph for x in line['z']]
        line['z0'] = line['z']
        try:
            line['i_max'] *= s3
        except KeyError:
            pass

    for _, _, _, con in netw.connections():
        assert 'phs' in con
        con['phs'] = ['A']

    for node in nodes:
        node['phs'] = ['A']
        node['v_base'] *= v_mult

    for inf in infs:
        inf['v_setpoint'] *= v_mult

    for load in loads:
        load['wiring'] = 'wye'  # i.e. in this case, equivalent of a single line to ground.
        load['s_nom'] = [c2a(sum((a2c(x) for x in load['s_nom'])))]

    for tx in txs:
        vg = tx['vector_group']
        tx['vector_group'] = 'yy0'
        tx['n_winding_pairs'] = 1
        tx['is_grounded_p'] = True
        tx['is_grounded_s'] = True
        dy = [x for x in vg if x in 'dy']
        assert len(dy) == 2
        mult = [math.sqrt(3.0) if x == 'y' else 1.0 for x in dy]
        tx['v_winding_base'] = [v_mult * x * y for x, y in zip(tx['v_winding_base'], mult)]
        if isinstance(tx['nom_turns_ratio'], list):
            # Complex
            tx['nom_turns_ratio'] = [x * mult[0] / mult[1] for x in tx['nom_turns_ratio']]
        else:
            # Real
            tx['nom_turns_ratio'] = tx['nom_turns_ratio'] * mult[0] / mult[1]
        if 'taps' in tx:
            tx['taps'] = [tx['taps'][0]]
    
    return netw


def scale_loads(netw: EJson, factor: complex) -> EJson:
    '''
    Scale network loads by a complex factor.

    Args:
        netw: e-JSON object
        factor: scaling factor
    
    Returns:
        in-place mutated network
    '''

    for load in netw.components('Load'):
        load['s_nom'] = [c2a(factor * a2c(x)) for x in load['s_nom']]
    
    return netw


def set_balanced_loads(netw: EJson, tot_load: complex) -> EJson:
    '''
    Set all loads to a balanced constant load.

    Args:
        netw: e-JSON network
        factor: scaling factor
    
    Returns:
        in-place mutated network
    '''

    for load in netw.components('Load'):
        n = len(load['s_nom'])
        load['s_nom'] = [c2a(tot_load / n)] * n
    
    return netw


def audit(netw: EJson) -> dict:
    '''
    Audit e-JSON.

    Args:
        netw: e-JSON network

    Returns:
        dict containing the results of the audit.
        '''

    aud = {}

    # Audit based on the schema.
    _audit_schema(netw, aud)

    # Check for unconnected or ill-connected components.
    _audit_connections(netw, aud)

    # Check for circular connections.
    _audit_circular_cons(netw, aud)

    # Check for connection phasing.
    _audit_conn_phase_consistency(netw, aud)

    return aud


def _audit_schema(netw: EJson, aud: dict):
    probs = aud.setdefault(
        'schema_errors', {'description': 'List of JSON schema errors'}
    ).setdefault('problems', [])
    netw_ej = netw.raw_ejson
    val = jsonschema.validators.Draft202012Validator(get_schema())
    errs = sorted(val.iter_errors(netw_ej), key=lambda e: e.path)
    for e in errs:
        e_str = ' | '.join((x.strip() for x in str(e).split('\n') if len(x) > 0))
        probs.append({
            'type': 'error',
            'fixed': False,
            'details': {
                'path': e.json_path,
                'description': e_str
            }
        })


def _audit_connections(netw: EJson, aud: dict):
    probs = aud.setdefault(
        'connections', {'description': 'Check for wrongly connected components'}
    ).setdefault('problems', [])

    for comp in netw.components(elems_only=True):
        ncons = len(list(netw.connections_from(comp['id'])))
        if (
            (comp['type'] in ('Line', 'Transformer') and ncons != 2) or
            (comp['type'] in ('Infeeder', 'Load') and ncons != 1)
        ):
            probs.append({
                'type': 'error',
                'fixed': False,
                'details': {
                    'elem_id': comp,
                    'n_cons': ncons
                }
            })


def _audit_circular_cons(netw: EJson, aud: dict):
    probs = aud.setdefault(
        'circular_connections', {'description': 'Check for circular connections'}
    ).setdefault('problems', [])

    for comp in netw.components(elems_only=True):
        for cons in netw.connections_from(comp['id']):
            if len(cons) == 2 and cons[0].cid_1 == cons[1].cid_1:
                probs.append({
                    'type': 'error',
                    'fixed': False,
                    'details': {
                        'elem_id': comp['id']
                    }
                })


def _audit_conn_phase_consistency(netw: EJson, aud: dict):
    probs = aud.setdefault(
        'phase_consistency', {'description': 'Check that phases of connection exist in the node'}
    ).setdefault('problems', [])

    for con in netw.connections():
        try:
            nd_comp = netw.component(con.cid_1)
            con_phs = con.con['phs']
            nd_phs = nd_comp['phs']
            if not (set(con_phs) <= set(nd_phs)):
                probs.append({
                    'type': 'error',
                    'fixed': False,
                    'details': {
                        'elem_id': con.cid_0,
                        'node_id': con.cid_1,
                        'con_idx': con.term_idx,
                        'con_phs': con_phs,
                        'node_phs': nd_phs
                    }
                })
        except KeyError:
            # This error would have been picked up earlier. Don't let it cause trouble here.
            pass
