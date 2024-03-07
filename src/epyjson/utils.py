import copy
from ordered_set import OrderedSet
from typing import Sequence, List

import jsonschema
import math
import networkx as nx
import numpy as np

from .ejson import Component, get_schema, EJson, logger


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

    return [c.real, c.imag]


def remove_hanging_nodes(netw: EJson):
    '''
    Remove hanging nodes: a node that terminates a line and has no other attached components.
    '''
    to_remove = []
    for comp in netw.components('Node'):
        adj = list(netw.connections_from(comp.cid))
        if len(adj) == 1:
            comp_to = netw.component(adj[0][1])
            if comp_to.ctype == 'Line':
                to_remove.append(comp.cid)
                to_remove.append(comp_to.cid)

    for cid in to_remove:
        netw.remove_component(cid)


def remove_out_of_service(netw: EJson):
    '''
    Remove components that are out of service.

    Args:
        graph: e-JSON graph, result of make_graph(...)
    '''

    for comp in list(netw.components()):
        if not comp.is_in_service():
            netw.remove_component(comp.cid)

    netw.remove_unconnected_nodes()
    assert [x.cid for x in netw.components()] == ['in1', 'nd1']


def collapse_elem(netw: EJson, cid):
    '''
    Remove component cid (normally a line) and coalesce the second and
    subsequent connected nodes into the first connected node.
    '''

    cons = list(netw.connections_from(cid))
    netw.remove_component(cid)
    nodes = [x[1] for x in cons]
    for node in nodes[1:]:
        for con in list(netw.connections_from(node)):
            netw.reconnect_elem(con[1], {node: nodes[0]})

    for node in nodes[1:]:
        assert len(list(netw.connections_from(node))) == 0
        netw.remove_component(node)


def merge_short_circuits(netw: EJson) -> EJson:
    '''
    Merge short circuit lines where possible.

    A short circuit line is a line that fully short circuits all phases between two nodes. In such cases, we can
    simply remove the line and merge the two nodes.
    '''

    merges = [l.cid for l in netw.components('Line') if is_short_circuit(l, netw)]

    for cid in merges:
        collapse_elem(netw, cid)

    return netw


def is_zero_impedance(comp: Component) -> bool:
    '''
    Returns True if line length is zero OR all impedance values are zero.

    Args:
        comp: Component for a Line.

    Returns:
        boolean value that is true iff the line is zero length or has z == z0 == 0.
    '''

    return comp.is_in_service() and (
        comp.cdata['length'] == 0.0
        or (all(value == 0.0 for value in comp.cdata['z']) and all(value == 0.0 for value in comp.cdata['z0']))
    )


def is_short_circuit(comp: Component, netw: EJson) -> bool:
    '''
    Returns True if a line short circuits ALL phases between its nodes.

    Args:
        netw: eJson network
        comp: Component for a Line.

    Returns:
        boolean value that is true iff the line is zero impedance and connects all phases between its two nodes.
    '''

    if not is_zero_impedance(comp):
        return False

    l_phs = [con[3]['phs'] for con in netw.connections_from(comp.cid)]
    nds = [netw.component(con[1]) for con in netw.connections_from(comp.cid)]
    nd_phs = [x.cdata['phs'] for x in nds]
    return l_phs == nd_phs


def merge_dups(netw: EJson) -> EJson:
    '''
    Merge duplicated lines.
    '''

    all_lines = list(netw.components('Line'))

    dups = {}
    for comp in all_lines:
        cons = netw.connections_from(comp.cid)
        cons_sorted = sorted(cons, key=lambda con: f'{con[1]}:{con[2]}')
        con_nids = [x[1] for x in cons_sorted]
        con_phs = [','.join(x[3]['phs']) for x in cons_sorted]
        in_serv = comp.is_in_service()
        k = '|'.join([','.join(x) for x in zip(con_nids, con_phs)] + [str(in_serv)])
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
        # We know that all lines in dup have the same nodes, the same in_service status and the same phasing.
        min_length = min([x.cdata['length'] for x in dup])
        l0 = dup[0]
        drop = []
        ys_merged = ys(l0.cdata)
        for l in dup[1:]:
            ys_merged += ys(l.cdata)
            drop.append(l.cid)

        for x in drop:
            netw.remove_component(x)

        zs_merged = (1.0 / ys_merged) / min_length

        l0.cdata['z'] = [zs_merged[0].real, zs_merged[0].imag]
        l0.cdata['z0'] = [zs_merged[1].real, zs_merged[1].imag]
        l0.cdata['length'] = min_length

    return netw


def merge_strings(netw: EJson):
    '''
    Merge strings of lines where possible.

    A string is a (line, node, ... , node, line) sequence whose nodes do not connect to any other elements in the
    sequence, and whose connection phasings are all the same.

    Args:
        graph: e-JSON graph, result of make_graph(...)
    '''

    def get_phasing(netw: EJson, comp):
        '''
        Get the phasing of a line. Returns None if there is a transposition.
        '''

        cons = netw.connections_from(comp.cid)
        phasings = [con[3]['phs'] for con in cons]
        if phasings[0] == phasings[1]:
            return phasings[0]
        else:
            return None

    def cap_lines(netw, g_sub):
        nodes = OrderedSet(x[0] for x in g_sub.nodes(data=True) if x[1]['comp'].ctype == 'Node')
        lines = [x[0] for x in g_sub.nodes(data=True) if x[1]['comp'].ctype == 'Line']
        adj_nodes = OrderedSet(e for x in lines for e in netw.graph.neighbors(x))
        caps = sorted(adj_nodes - nodes)
        assert len(caps) in (1, 2)
        return (netw.graph.subgraph(lines + list(adj_nodes)), caps)

    def do_str(netw, g_sub, remove, new):
        g_sub, caps = cap_lines(netw, g_sub)  # g_sub is unordered, caps are lexically ordered

        if len(caps) <= 1:
            # Special case: the string is circular.
            to_remove = OrderedSet(g_sub.nodes) - caps
            for x in to_remove:
                remove.add(x)

            return

        # Order from one end to the other.
        ordered = [g_sub.nodes[x]['comp'] for x in nx.dfs_preorder_nodes(g_sub, source=next(iter(caps)))]
        do_str_ordered(netw, ordered, remove, new)

    def do_str_ordered(netw, ordered, remove, new):
        # ordered is [(id, type, dict)] for all nodes in the string including the two terminal nodes.
        if len(ordered) < 5:
            # We need at least 3 nodes and 2 lines to do any collapsing.
            return

        assert ordered[0].ctype == 'Node'
        assert ordered[-1].ctype == 'Node'

        # Loop over internal Nodes to check if all line to line connections are compatible.
        # If not, do the pieces separately.
        cons = list(netw.connections_between(ordered[0].cid, ordered[1].cid))
        assert len(cons) == 1
        con = (ordered[0].cid, ordered[-1].cid, cons[0][3])
        for i_nd in range(2, len(ordered) - 1, 2):
            l0 = ordered[i_nd - 1]
            assert l0.ctype == 'Line'

            l1 = ordered[i_nd + 1]
            assert l1.ctype == 'Line'

            ph0 = get_phasing(netw, l0)
            ph1 = get_phasing(netw, l1)
            if (ph0 is None or ph1 is None or ph0 != ph1):
                # We need to do parts separately due to phasing mismatch at i_nd.
                do_str_ordered(netw, ordered[:i_nd + 1], remove, new)
                do_str_ordered(netw, ordered[i_nd:], remove, new)
                return

        repl_lines = ordered[1::2]

        has_in_serv = any('in_service' in x.cdata for x in repl_lines)
        in_serv = all(x.cdata['in_service'] if 'in_service' in x.cdata else True for x in repl_lines)

        ls = np.array([x.cdata['length'] for x in repl_lines])
        l_tot = sum(ls)
        zs = np.array([complex(*x.cdata['z']) for x in repl_lines])
        z0s = np.array([complex(*x.cdata['z0']) for x in repl_lines])
        any_bs = any('b_chg' in x.cdata for x in repl_lines)
        bs = np.array(
            [complex(*x.cdata['b_chg']) if 'b_chg' in x.cdata else 0.0+0.0j for x in repl_lines]
        ) if any_bs else None

        new_line_id = repl_lines[0].cid
        new_line_dict = copy.deepcopy(repl_lines[0].cdata)

        new_line_dict['length'] = l_tot
        new_line_dict['z'] = c2a(sum(zs * ls) / l_tot)
        new_line_dict['z0'] = c2a(sum(z0s * ls) / l_tot)
        if any_bs:
            new_line_dict['b_chg'] = c2a(sum(bs * ls)) / l_tot

        if has_in_serv:
            new_line_dict['in_service'] = in_serv

        for x in ordered[1:-1]:
            remove.add(x.cid)

        new_line_dict['user_data']['orig_ids'] = list(
            OrderedSet(sum([x.cdata['user_data']['orig_ids'] for x in repl_lines], []))
        )
        new.append((Component(new_line_id, 'Line', new_line_dict), con))

    # Find all nodes that are only connected to 2 lines.
    nodes = (x.cid for x in netw.components(nodes_only=True))
    nodes = (x for x in nodes if netw.graph.degree(x) == 2)
    nodes = [x for x in nodes if all(netw.component(y).ctype == 'Line' for y in netw.neighbors(x))]

    # Extend to all connected lines. Note use of dict to preserve ordering (?)
    lines = list(dict((l, None) for n in nodes for l in netw.graph.neighbors(n)).keys())

    remove = OrderedSet()
    new = []

    graph_strs = netw.graph.subgraph(nodes + lines)  # Not order preserving
    con_comps = sorted((sorted(x) for x in nx.connected_components(graph_strs)), key=lambda x: x[0])
    # Sorting is to preserve determinism.
    for con_comp in con_comps:
        graph_str = graph_strs.subgraph(con_comp)
        do_str(netw, graph_str, remove, new)

    for x in remove:
        netw.remove_component(x)

    for c, con in new:
        netw.add_comp(c.cid, c.ctype, c.cdata)
        netw.connect(c.cid, con[0], 0, con[2])
        netw.connect(c.cid, con[1], 1, con[2])


def reduce_network(netw: EJson):
    '''
    Reduce the size of the network by telescoping lines together, merging duplicated lines and removing unused spurs.

    Args:
        netw: eJson network
    '''

    def report_stats(netw: EJson, prefix: str, log=logger.debug):
        l = 0.0
        for line in netw.components('Line'):
            l += line.cdata['length']

        by_type = {}
        for c in netw.components():
            by_type.setdefault(c.ctype, 0)
            by_type[c.ctype] += 1

        log(f'    {prefix}:')
        log(f'        Total line length = {l}')
        for t, n in by_type.items():
            log(f'        Number of {t}s = {n}')

    for line in netw.components('Line'):
        line.cdata.setdefault('user_data', {})['orig_ids'] = [line.cid]

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


def add_map(netw: EJson, points: Sequence[dict], add_latlon: bool, add_xy: bool):
    '''
    Given 2 or 3 points with both (x, y) and (lat, lon), find the transformation A, b st. latlon = A xy + b
    Then add the missing information, e.g. add xy if a node has lat_long or vice-versa.

    Args:
        netw: the EJson network
        points: list of points, [{'x': <x>, 'y': <y>, 'lat': <lat>, 'lon': <lon>}, ...]
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
        if 'lat_long' in c.cdata:
            c.cdata['xy'] = (A_inv @ (np.array(c.cdata['lat_long']) - b)).tolist()
        elif 'xy' in c.cdata:
            c.cdata['lat_long'] = (A @ np.array(c.cdata['xy']) + b).tolist()


def make_radial(netw: EJson, start_id: str):
    '''
    Break cycles, making the graph radial.

    Args:
        netw: EJson network
        start_id: Depth first search starting component.
    '''

    # The code assumes everything is correctly ordered. Do it in case it hasn't already been done.
    netw.reorder(start_id)

    def pre_cb(netw: EJson, cur: Component, accum: list):
        if not cur.is_in_service():
            return (True, accum)

        if cur.ctype == 'Line':
            nd1 = list(netw.connections_from(cur.cid))[1][1]
            if nd1 in accum[0]:
                accum[1].append(cur.cid)
                return (True, accum)

        elif cur.ctype == 'Node':
            accum[0].append(cur.cid)

        return (False, accum)

    def post_cb(netw: EJson, cur: Component, accum: list):
        if cur.ctype == 'Node':
            accum[0].pop()

        return accum

    accum = ([], [])  # (stack_of_seen_nodes, to_remove)

    _, (_, to_remove) = netw.dfs(start_id, pre_cb=pre_cb, post_cb=post_cb, accum=accum)

    for cid in to_remove:
        netw.remove_component(cid)


def make_single_phased(netw: EJson):
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
    '''

    s3 = math.sqrt(3.0)

    comps = list(netw.components())
    nodes = [x for x in comps if x.ctype == 'Node']
    elems = [x for x in comps if x.ctype != 'Node']
    lines = [x for x in elems if x.ctype == 'Line']
    txs = [x for x in elems if x.ctype == 'Transformer']
    infs = [x for x in elems if x.ctype == 'Infeeder']
    loads = [x for x in elems if x.ctype == 'Load']

    v_mult = s3 if netw.properties['voltage_type'] == 'lg' else 1.0
    netw.properties['voltage_type'] = 'lg'

    for line in lines:
        cons = list(netw.connections_from(line.cid))
        assert len(cons) == 2
        nph = len([x for x in cons[0][3]['phs'] if x.lower() not in 'ng'])
        line.cdata['z'] = [x * 3 / nph for x in line.cdata['z']]
        line.cdata['z0'] = line.cdata['z']
        try:
            line.cdata['i_max'] *= s3
        except KeyError:
            pass

    for _, _, _, con in netw.connections():
        assert 'phs' in con
        con['phs'] = ['A']

    for node in nodes:
        node.cdata['phs'] = ['A']
        node.cdata['v_base'] *= v_mult

    for inf in infs:
        inf.cdata['v_setpoint'] *= v_mult

    for load in loads:
        load.cdata['wiring'] = 'wye'  # i.e. in this case, equivalent of a single line to ground.
        load.cdata['s_nom'] = [c2a(sum((a2c(x) for x in load.cdata['s_nom'])))]

    for tx in txs:
        vg = tx.cdata['vector_group']
        tx.cdata['vector_group'] = 'yy0'
        tx.cdata['n_winding_pairs'] = 1
        tx.cdata['is_grounded_p'] = True
        tx.cdata['is_grounded_s'] = True
        dy = [x for x in vg if x in 'dy']
        assert len(dy) == 2
        mult = [math.sqrt(3.0) if x == 'y' else 1.0 for x in dy]
        tx.cdata['v_winding_base'] = [v_mult * x * y for x, y in zip(tx.cdata['v_winding_base'], mult)]
        if isinstance(tx.cdata['nom_turns_ratio'], list):
            # Complex
            tx.cdata['nom_turns_ratio'] = [x * mult[0] / mult[1] for x in tx.cdata['nom_turns_ratio']]
        else:
            # Real
            tx.cdata['nom_turns_ratio'] = tx.cdata['nom_turns_ratio'] * mult[0] / mult[1]
        if 'taps' in tx.cdata:
            tx.cdata['taps'] = [tx.cdata['taps'][0]]


def scale_loads(netw: EJson, factor: complex) -> nx.Graph:
    '''
    Scale network loads by a complex factor.

    Args:
        netw: e-JSON object
        factor: scaling factor
    '''

    for load in netw.components('Load'):
        load.cdata['s_nom'] = [c2a(factor * a2c(x)) for x in load.cdata['s_nom']]


def set_balanced_loads(netw: EJson, tot_load: complex) -> nx.Graph:
    '''
    Set all loads to a balanced constant load.

    Args:
        netw: e-JSON network
        factor: scaling factor
    '''

    for load in netw.components('Load'):
        n = len(load.cdata['s_nom'])
        load.cdata['s_nom'] = [c2a(tot_load / n)] * n


def audit(netw: EJson) -> dict:
    '''
    Audit e-JSON.

    Args:
        graph: e-JSON graph, result of make_graph(...)

    Returns:
        dict containing the results of the audit.
        '''

    aud = {}

    # Audit based on the schema.
    _audit_schema(netw, aud)

    # Audit unit consistency.
    _audit_unit_consistency(netw, aud)

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


def _audit_unit_consistency(netw: EJson, aud: dict):
    probs = aud.setdefault(
        'unit_consistency', {'description': 'Check consistency of units'}
    ).setdefault('problems', [])
    try:
        units = netw.properties['units']
        i_unit = units['current']
        v_unit = units['voltage']
        z_unit = units['impedance']
        l_unit = units['length']
        p_unit = units['power']

        if v_unit != i_unit * z_unit * l_unit:
            probs.append({
                'type': 'error',
                'fixed': False,
                'details': {
                    'description': 'Units do not satisfy Ohm\'s law'
                }
            })

        if p_unit != i_unit * v_unit:
            probs.append({
                'type': 'error',
                'fixed': False,
                'details': {
                    'description': 'Units do not satisfy P := IV definition'
                }
            })

    except KeyError as e:
        probs.append({
            'type': 'error',
            'fixed': False,
            'details': {
                'description': f'Missing unit or units: {e}'
            }
        })


def _audit_connections(netw: EJson, aud: dict):
    probs = aud.setdefault(
        'connections', {'description': 'Check for wrongly connected components'}
    ).setdefault('problems', [])

    for comp in netw.components(elems_only=True):
        ncons = len(list(netw.connections_from(comp.cid)))
        if (
            (comp.ctype in ('Line', 'Transformer') and ncons != 2) or
            (comp.ctype in ('Infeeder', 'Load') and ncons != 1)
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
        for cons in netw.connections_from(comp.cid):
            if len(cons) == 2 and cons[0][1] == cons[1][1]:
                probs.append({
                    'type': 'error',
                    'fixed': False,
                    'details': {
                        'elem_id': comp.cid
                    }
                })


def _audit_conn_phase_consistency(netw: EJson, aud: dict):
    probs = aud.setdefault(
        'phase_consistency', {'description': 'Check that phases of connection exist in the node'}
    ).setdefault('problems', [])

    for con in netw.connections():
        try:
            nd_comp = netw.component(con[1])
            con_phs = con[3]['phs']
            nd_phs = nd_comp.cdata['phs']
            if not (set(con_phs) <= set(nd_phs)):
                probs.append({
                    'type': 'error',
                    'fixed': False,
                    'details': {
                        'elem_id': con[0],
                        'node_id': con[1],
                        'con_idx': con[2],
                        'con_phs': con_phs,
                        'node_phs': nd_phs
                    }
                })
        except KeyError:
            # This error would have been picked up earlier. Don't let it cause trouble here.
            pass
