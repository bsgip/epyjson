from .ejson import *


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

    l_phs = [con['phs'] for con in comp.cdata['cons']]
    nd_cds = [netw.graph.nodes[con['node']]['data'][1] for con in comp.cdata['cons']]
    nd_phs = [x['phs'] for x in nd_cds]
    return l_phs == nd_phs


def reduce_network(netw: EJson):
    '''
    Reduce the size of the network by telescoping lines together, merging duplicated lines and removing unused spurs.
    
    Args:
        netw: eJson network

    Returns:
        The mutated network.
    '''

    def report_stats(netw: EJson, prefix: str, log=logger.debug):
        l = 0.0
        for line in netw.components('Line'):
            l += line.cdata['length']

        by_type = {}
        for c in netw.components():
            by_type.setdefault(c.ctype, 0)
            by_type[c.ctype] += 1
        
        logger.debug(f'    {prefix}:')
        logger.debug(f'        Total line length = {l}')
        for t, n in by_type.items():
            logger.debug(f'        Number of {t}s = {n}')

    for line in netw.components('Line'):
        line.cdata.setdefault('user_data', {})['orig_ids'] = [line.cid]

    report_stats(netw, 'Initial', logger.info)
    while True:
        n = len(netw.graph.nodes)

        _merge_strings(netw)
        report_stats(netw, 'After merge strings')

        netw.remove_hanging_nodes()
        report_stats(netw, 'After remove hanging')

        _merge_short_circuits(netw)
        report_stats(netw, 'After merge short circuits')
        
        _merge_dups(netw)
        report_stats(netw, 'After merge dups')

        if len(netw.graph.nodes) == n:
            break

    report_stats(netw, 'Final', logger.info)


def remove_out_of_service(netw: EJson):
    '''
    Remove components that are out of service.

    Args:
        graph: e-JSON graph, result of make_graph(...) 

    Returns:
        The mutated graph
    '''
    
    to_remove = set()

    for comp in netw.components(): 
        if not comp.is_in_service():
            to_remove.add(comp.cid)

    for comp_id in to_remove:
        netw.remove_component(comp_id)

    netw.remove_unconnected_nodes()


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
        a00, a01, a10, a11, b0, b1 = la.solve(A, rhs)
    else:
        exit('Map must have either 2 or three test points.')

    A = np.array([[a00, a01], [a10, a11]])
    A_inv = la.inv(A)
    b = np.array([b0, b1])

    for c in netw.components('Node'):
        if 'lat_long' in c.cdata:
            c.cdata['xy'] = (A_inv @ (np.array(c.cdata['lat_long']) - b)).tolist()
        elif 'xy' in c.cdata:
            c.cdata['lat_long'] = (A @ np.array(c.cdata['xy']) + b).tolist()


def add_standard_map(graph: nx.Graph):
    '''
    Assuming that all nodes have a latlong, add xy and a standard map using a standard map transform.

    Args: 
        graph: e-JSON graph, result of make_graph(...) 
    '''

    nds = list(d for _, _, d in graph_components(graph, comp_type='Node'))
    if len(nds) == 0:
        logger.warning(f"WARNING: Can't add map for network with no nodes")
        return graph

    lats, longs = zip(*(x['lat_long'] for x in nds))
    lat_mean = np.mean(lats)
    long_mean = np.mean(longs)

    # Calculate the transform A, b s.t. latlong = A xy + b, xy = A_inv (latlong - b)
    A, A_inv, b = _std_map_transform(lat_mean, long_mean)

    for nd in nds:
        nd['xy'] = A_inv.dot(np.array(nd['lat_long']) - b).tolist() 

    return graph


def break_cycles(netw: EJson, start_id: str):
    '''
    Break graph cycles, making the graph radial.

    Args:
        graph: e-JSON graph, result of make_graph(...) 
        start_id: Depth first search starting component.

    Returns:
        The mutated graph
    '''
    
    # The code assumes everything is correctly ordered. Do it in case it hasn't already been done.
    netw.reorder(start_id)

    def pre_cb(netw: EJson, cur: Component, accum: list):
        if not cur.is_in_service():
            return (True, accum)

        if cur.ctype == 'Line':
            nd1 = cur.cdata['cons'][1]['node'] # We're already ordered so this is the "to" node.
            if nd1 in accum[0]:
                accum[1].append(cur.cid)
                return (True, accum)

        elif cur.ctype == 'Node':
            accum[0].append(cur.cid)

        return (False, accum)

    def post_cb(graph: nx.Graph, cur, accum):
        if cur.ctype == 'Node':
            accum[0].pop()

        return accum

    accum = ([], []) # (stack_of_seen_nodes, to_remove)

    _, accum = netw.dfs(start_id, pre_cb=pre_cb, post_cb=post_cb, accum=accum)
    to_remove = accum[1]
    for comp_id in to_remove:
        _remove_node(graph, comp_id)


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

    v_mult = s3 if netw['voltage_type'] == 'lg' else 1.0
    netw['voltage_type'] = 'lg'

    for line in lines:
        nph = len([x for x in line.cdata['cons'][0]['phs'] if x.lower() not in 'ng'])
        line.cdata['z'] = [x * 3 / nph for x in line.cdata['z']]
        line.cdata['z0'] = line.cdata['z']
        try:
            line.cdata['i_max'] *= s3
        except KeyError:
            pass

    for elem in elems:
        for con in elem.cdata['cons']:
            con['phs'] = ['A']

    for node in nodes:
        node.cdata['phs'] = ['A']
        node.cdata['v_base'] *= v_mult

    for inf in infs:
        inf.cdata['v_setpoint'] *= v_mult

    for load in loads:
        is_delta = load.cdata['wiring'] == 'delta'

        load.cdata['wiring'] = 'wye' # i.e. in this case, equivalent of a single line to ground.
        load.cdata['s_nom'] = [c2a(sum((a2c(x) for x in l.cdata['s_nom'])))]

    for tx in txs:
        vg = tx.cdata['vector_group']
        tx.cdata['vector_group'] = 'yy0'
        tx.cdata['n_winding_pairs'] = 1
        tx.cdata['is_grounded_p'] = True
        tx.cdata['is_grounded_s'] = True
        dy = [x for x in vg if x in 'dy']
        assert(len(dy) == 2)
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
        graph: e-JSON graph, result of make_graph(...) 
        factor: scaling factor
    '''

    for load in netw.components('Load'):
        load.cdata['s_nom'] = [c2a(factor * a2c(x)) for x in load.cdata['s_nom']]


def set_balanced_loads(graph: nx.Graph, tot_load: complex) -> nx.Graph:
    '''
    Set all loads to a balanced constant load.

    Args:
        netw: e-JSON network
        factor: scaling factor
    '''

    for load in netw.components('Load'):
        n = len(load.cdata['s_nom'])
        load.cdata['s_nom'] = [c2a(tot_load / n)] * n

    return graph


def audit(graph: nx.Graph) -> dict:
    '''
    Audit e-JSON.

    Args:
        graph: e-JSON graph, result of make_graph(...) 

    Returns:
        dict containing the results of the audit.
        '''

    aud = {}

    # Audit based on the schema.
    _audit_schema(graph, aud)
    
    # Audit unit consistency.
    _audit_unit_consistency(graph, aud)

    # Check for unreferenced connections.
    _audit_unreferenced_connections(graph, aud)

    # Check for circular connections.
    _audit_circular_cons(graph, aud)

    return aud


# Internal utility functions ---------------------------------------------------


def _merge_strings(netw: EJson):
    '''
    Merge strings of lines where possible. 
    
    A string is a (line, node, ... , node, line) sequence whose nodes do not connect to any other elements in the
    sequence, and whose connection phasings are all the same.

    Args:
        graph: e-JSON graph, result of make_graph(...) 
    
    Returns:
        the mutated graph.
    '''

    def get_phasing(comp_dict):
        '''
        Get the phasing of a line. Returns None if there is a transposition.
        '''
        phasings = [con['phs'] for con in comp_dict['cons']]
        if phasings[0] == phasings[1]:
            return phasings[0]
        else:
            return None

    def cap_lines(g_sub, g):
        nodes = set(x[0] for x in g_sub.nodes(data=True) if x[1]['comp'].ctype == 'Node')
        lines = [x[0] for x in g_sub.nodes(data=True) if x[1]['comp'].ctype[0] == 'Line']
        adj_nodes = set(e for x in lines for e in g.neighbors(x))
        caps = adj_nodes - nodes
        return (g.subgraph(lines + list(adj_nodes)), caps)

    def do_str(g_sub, g, remove, new):
        g_sub, caps = cap_lines(g_sub, g)

        if len(caps) <= 1:
            # Special case: the string is circular.
            to_remove = set(g_sub.nodes) - caps
            for x in to_remove:
                remove.add(x)

            return

        if len(g_sub.nodes) < 5:
            # We need at least 3 nodes and 2 lines to do any collapsing.
            return

        # Order from one end to the other.
        assert len(caps) == 2

        ordered = [g_sub.nodes[x]['comp'] for x in nx.dfs_preorder_nodes(g_sub, source=next(iter(caps)))]

        do_str_ordered(ordered, remove, new)

    def do_str_ordered(ordered, remove, new):
        # ordered is [(id, type, dict)] for all nodes in the string including the two terminal nodes.

        assert(ordered[0][1] == 'Node')
        assert(ordered[-1][1] == 'Node')

        # Loop over internal Nodes to check if all line to line connections are compatible.
        # If not, do the pieces separately.
        for i_nd in range(2, len(ordered) - 1, 2):
            l0_id, l0_tp, l0 = ordered[i_nd - 1]
            assert l0_tp == 'Line'

            l1_id, l1_tp, l1 = ordered[i_nd + 1]
            assert l1_tp == 'Line'

            ph0 = get_phasing(l0)
            ph1 = get_phasing(l1)
            if (ph0 is None or ph1 is None or ph0 != ph1):
                # We need to do parts separately due to phasing mismatch at i_nd.
                do_str_ordered(ordered[:i_nd + 1], remove, new)
                do_str_ordered(ordered[i_nd:], remove, new)
                return

        repl_lines = ordered[1::2]

        has_in_serv = any('in_service' in x[2] for x in repl_lines)
        in_serv = all(x[2]['in_service'] if 'in_service' in x[2] else True for x in repl_lines)

        ls = np.array([x[2]['length'] for x in repl_lines])
        l_tot = sum(ls)
        zs = np.array([complex(*x[2]['z']) for x in repl_lines])
        z0s = np.array([complex(*x[2]['z0']) for x in repl_lines])
        any_bs = any('b_chg' in x[2] for x in repl_lines)
        bs = np.array([complex(*x[2]['b_chg']) if 'b_chg' in x[2] else 0.0+0.0j for x in repl_lines]) if any_bs else None

        new_line_id = repl_lines[0][0]
        new_line_dict = copy.deepcopy(repl_lines[0][2])

        new_line_dict['length'] = l_tot
        new_line_dict['z'] = c2a(sum(zs * ls) / l_tot)
        new_line_dict['z0'] = c2a(sum(z0s * ls) / l_tot)
        if any_bs:
            new_line_dict['b_chg'] = c2a(sum(bs * ls)) / l_tot

        new_line_dict['cons'][0]['node'] = ordered[0][0]
        new_line_dict['cons'][1]['node'] = ordered[-1][0]

        if has_in_serv:
            new_line_dict['in_service'] = in_serv
        
        for x in ordered[1:-1]:
            remove.add(x[0])
        
        new_line_dict['user_data']['orig_ids'] = list(set(sum([x[2]['user_data']['orig_ids'] for x in repl_lines], [])))
        new.append(Component(new_line_id, 'Line', new_line_dict))

    graph = netw.graph

    # Find all nodes that are only connected to either 1 or 2 lines.
    nodes = (x.cid for x in netw.components(nodes_only=True))
    nodes = (x for x in nodes if graph.degree(x) in [1, 2])
    nodes = [x for x in nodes if all(netw.component(y).ctype == 'Line' for y in netw.neighbors(x))]

    # Extend to all connected lines. Note use of dict to preserve ordering (?)
    lines = list(dict((l, None) for n in nodes for l in graph.neighbors(n)).keys())

    graph_strs = graph.subgraph(nodes + lines)

    remove = set()
    new = []

    con_comps = sorted((sorted(x) for x in nx.connected_components(graph_strs)), key=lambda x: x[0])
    # Sorting is to preserve determinism.
    for con_comp in con_comps:
        graph_str = graph_strs.subgraph(con_comp)
        do_str(graph_str, graph, remove, new)

    for x in remove:
        netw.remove_component(x)

    for c in new:
        netw.add_comp(c.cid, c.ctype, c.cdata)
        cons = c.cdata['cons']
        for con in cons:
            netw.connect(c.cid, con['node'], con)


def _merge_short_circuits(netw: EJson) -> EJson:
    '''
    Merge short circuit lines where possible. 
    
    A short circuit line is a line that fully short circuits all phases between two nodes. In such cases, we can
    simply remove the line and merge the two nodes.
    '''

    merges = [l.cid for l in netw.components('Line') if is_short_circuit(l, netw)]
    
    for cid in merges:
        netw.collapse_elem(cid)

    return netw


def _merge_dups(netw: EJson) -> EJson:
    '''
    Merge duplicated lines.
    '''

    all_lines = list(netw.components('Line'))
    all_nodes = list(netw.components(nodes_only=True))

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
        min_length = min([x[1]['length'] for x in dup])
        l0 = dup[0]
        drop = []
        ys_merged = ys(l0[1])
        for l in dup[1:]:
            ys_merged += ys(l[1])
            drop.append(l[0])

        for x in drop:
            _remove_node (graph, x)

        zs_merged = (1.0 / ys_merged) / min_length

        l0[1]['z'] = [zs_merged[0].real, zs_merged[0].imag]
        l0[1]['z0'] = [zs_merged[1].real, zs_merged[1].imag]
        l0[1]['length'] = min_length

    return netw


def _std_map_transform(lat0, long0):
    '''
    latlong = A xy + b
    xy = A_inv (latlong - b)
    '''

    R_EARTH_M = 6378100.

    scale = R_EARTH_M * math.pi / 180.0
    cos_lat_0 = math.cos(lat0 * math.pi / 180.0)

    A_inv = np.array([[0.0, scale * cos_lat_0], [scale, 0.0]])
    A = la.inv(A_inv)
    b = np.array([lat0, long0])

    return (A, A_inv, b)


def _audit_schema(graph: nx.Graph, aud: dict):
    probs = aud.setdefault(
        'schema_errors', {'description': 'List of JSON schema errors'}
    ).setdefault('problems', [])
    netw_ej = graph.graph['netw']
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


def _audit_unit_consistency(graph: nx.Graph, aud: dict):
    probs = aud.setdefault(
        'unit_consistency', {'description': 'Check consistency of units'}
    ).setdefault('problems', [])
    netw_ej = graph.graph['netw']
    try:
        units = netw_ej['units']
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


def _audit_unreferenced_connections(graph: nx.Graph, aud: dict):
    probs = aud.setdefault(
        'unreferenced_conections', {'description': 'Check for connections to nodes that don\'t exist'}
    ).setdefault('problems', [])
    nds = set(x[0] for x in graph_components(graph, comp_type='Node'))
    for cid, ctype, cdict in (x for x in graph_components(graph) if x[1] != 'Node'):
        try:
            for i, con in enumerate(cdict['cons']):
                if con['node'] not in nds:
                    probs.append({
                        'type': 'error',
                        'fixed': False,
                        'details': {
                            'elem_id': cid,
                            'con_idx': i,
                            'con_node': con['node']
                        }
                    })

        except KeyError:
            # This error would have been picked up earlier. Don't let it cause trouble here.
            pass

    
def _audit_circular_cons(graph: nx.Graph, aud: dict):
    probs = aud.setdefault(
        'circular_conections', {'description': 'Check for circular connections'}
    ).setdefault('problems', [])
    for eid, _, edict in (x for x in graph_components(graph) if x[1] != 'Node'):
        cons = edict['cons']
        if len(cons) == 2 and cons[0]['node'] == cons[1]['node']:
            probs.append({
                'type': 'error',
                'fixed': False,
                'details': {
                    'elem_id': eid
                }
            })


def _audit_conn_phase_consistency(graph: nx.Graph, aud: dict):
    probs = aud.setdefault(
        'phase_consistency', {'description': 'Check that phases of connection exist in the node'}
    ).setdefault('problems', [])
    for eid, _, edict in (x for x in graph_components(graph) if x[1] != 'Node'):
        try:
            for i, con in enumerate(edict['cons']):
                nid = con['node']
                _, ndict = graph.nodes[nid]['data']
                cphs = set(con['phs'])
                nphs = set(ndict['phs'])
                if not cphs <= nphs:
                    probs.append({
                        'type': 'error',
                        'fixed': False,
                        'details': {
                            'elem_id': eid,
                            'con_idx': i,
                            'con_node': nid,
                            'con_phs': cphs,
                            'node_phs': nphs
                        }
                    })

        except KeyError:
            # This error would have been picked up earlier. Don't let it cause trouble here.
            pass


