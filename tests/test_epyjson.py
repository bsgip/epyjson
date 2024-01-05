import pathlib

from epyjson import *

test_netws_path = pathlib.Path(__file__).parent / 'test_data'

def test_quick_tests():
    ''' Test as much functionality as possible, mainly for crashes.'''
    netw = EJson.read_from_file(test_netws_path / 'netw_generic_a.json')

    assert netw.component('nd1').cid == 'nd1'

    assert len(list(netw.components(ctype='Line'))) == 11

    assert len(list(netw.connections())) == 28

    assert len(list(netw.connections_between('nd1', 'tx1_2'))) == 1

    assert len(list(netw.connections_from('tx1_2'))) == 2

    visited, _ = netw.dfs(start='in1', pre_cb=lambda ejson, cur_comp, accum: (False, None))
    assert len(visited) == len(list(netw.components()))

    assert len(list(netw.neighbors('nd2'))) == 2

    netw_trim: EJson = netw.clone()
    netw_trim.trim('ln10_11', stop_cb = lambda netw, c: c.cid == 'nd10')
    assert len(list(netw_trim.components())) == len(list(netw.components())) - 4
    
    netw_trim: EJson = netw.clone()
    netw_trim.trim('nd4', stop_cb = lambda netw, c: c.cid == 'nd6')
    assert len(list(netw_trim.components())) == len(list(netw.components())) - 11
    
    netw_only: EJson = netw.clone()
    netw_only.only('nd5', stop_cb = lambda netw, c: c.cid == 'ln5_6')
    assert len(list(netw_only.components())) == 10

    netw_recon: EJson = netw.clone()
    netw_recon.reconnect_elem('ld8', {'nd8': 'nd4'})
    assert next(iter(netw_recon.connections_from('ld8')))[1] == 'nd4'
    
    netw_rename: EJson = netw.clone()
    netw_rename.rename()
    assert [c.cid for c in netw_rename.components()] == [
        'infeeder_1', 'node_1', 'transformer_1', 'node_2', 'line_1', 'node_3', 'line_2', 'node_4', 'line_3', 'node_5',
        'line_4', 'node_6', 'line_5', 'node_7', 'line_6', 'node_8', 'load_1', 'line_7', 'node_9', 'load_2', 'node_10',
        'line_8', 'node_11', 'line_9', 'node_12', 'line_10', 'node_13', 'line_11', 'load_3'
    ]


def test_round_trip():
    netw_a = EJson.read_from_file(test_netws_path / 'netw_generic_a.json')
    tmpfile = pathlib.Path('/tmp/netw_epyjson_test_round_trip.json')
    netw_a.write_to_file(tmpfile)
    netw_b = EJson.read_from_file('/tmp/netw_epyjson_test_round_trip.json')
    tmpfile.unlink()
    assert netw_a.raw_ejson() == netw_b.raw_ejson()


def test_reorder():
    netw = EJson.read_from_file(test_netws_path / 'netw_test_reorder.json')
    netw.reorder('ld3')
    assert [x.cid for x in netw.components()] == ['ld3', 'nd3', 'ln2_3', 'nd2', 'tx1_2', 'nd1', 'in1']
    tx_cons = [list(x[0:3]) for x in netw.connections_from('tx1_2')]
    assert tx_cons == [['tx1_2', 'nd1', 0], ['tx1_2', 'nd2', 1]]
    ln_cons = [list(x[0:3]) for x in netw.connections_from('ln2_3')]
    assert ln_cons == [['ln2_3', 'nd3', 0], ['ln2_3', 'nd2', 1]]


def test_make_radial():
    netw = EJson.read_from_file(test_netws_path / 'netw_test_make_radial.json')
    make_radial(netw, 'in1')
    assert [x.cid for x in netw.components()] == ['in1', 'nd1', 'tx1_2', 'nd2', 'ln2_3', 'nd3', 'ln3_4', 'nd4']


def test_remove_unconnected():
    netw = EJson.read_from_file(test_netws_path / 'netw_test_remove_unconnected.json')
    netw.remove_unconnected_nodes()
    assert [x.cid for x in netw.components()] == ['in1', 'nd1']


def test_remove_out_of_service():
    netw = EJson.read_from_file(test_netws_path / 'netw_test_remove_out_of_service.json')
    remove_out_of_service(netw)
    assert [x.cid for x in netw.components()] == ['in1', 'nd1']


def test_set_loads():
    netw = EJson.read_from_file(test_netws_path / 'netw_generic_a.json')
    set_balanced_loads(netw, 12.0 + 3.0j)
    assert netw.component('ld8').cdata['s_nom'] == [[4.0, 1.0], [4.0, 1.0], [4.0, 1.0]]
    scale_loads(netw, 2.0)
    assert netw.component('ld8').cdata['s_nom'] == [[8.0, 2.0], [8.0, 2.0], [8.0, 2.0]]


def test_make_single_phased():
    netw = EJson.read_from_file(test_netws_path / 'netw_test_make_single_phased.json')
    netw_sp = netw.clone()

    make_single_phased(netw_sp)
    assert netw_sp.properties['voltage_type'] == 'lg'
    
    for con in netw_sp.connections():
        assert con[3]['phs'] == ['A']

    for n in netw_sp.components(nodes_only=True):
        assert n.cdata['phs'] == ['A']
    
    for tx in netw_sp.components(ctype='Transformer'):
        assert tx.cdata['vector_group'] == 'yy0'

    assert netw_sp.component('ld8').cdata['s_nom'] == [[1.0, 1.0]]
    assert netw_sp.component('ld9').cdata['s_nom'] == [[3.0, 1.0]]

    def close(a, b):
        return abs(complex(*a) - complex(*b)) < 1e-9

    assert close(netw_sp.component('ln2_3').cdata['z'], [1.0, 1.1])
    assert close(netw_sp.component('ln2_3').cdata['z0'], [1.0, 1.1])

    assert close(netw_sp.component('ln6_8').cdata['z'], [6.0, 0.0])
    assert close(netw_sp.component('ln6_8').cdata['z0'], [6.0, 0.0])

    assert close(netw_sp.component('ln11_12').cdata['z'], [3.0, 3.15])
    assert close(netw_sp.component('ln11_12').cdata['z0'], [3.0, 3.15])


def test_reduce_merge_strings():
    ''' Test reduce where there is a string of lines to merge.'''
    netw = EJson.read_from_file(test_netws_path / 'netw_test_reduce_merge_strings.json')
    
    def get_imp(netw, z):
        return sum((complex(*x.cdata[z]) * x.cdata['length']) for x in netw.components('Line'))

    z_bef = get_imp(netw, 'z')
    reduce_network(netw)
    z_aft = get_imp(netw, 'z')

    assert len(list(netw.components('Node'))) == 3
    assert len(list(netw.components('Transformer'))) == 1
    assert len(list(netw.components('Line'))) == 1
    assert len(list(netw.components('Load'))) == 1
    assert len(list(netw.components('Infeeder'))) == 1
    assert sum((x.cdata['length'] for x in netw.components('Line'))) == 3
    assert abs(z_bef - z_aft) < 1e-9


def test_reduce_remove_hanging():
    ''' Test reduce where there is a hanging spur.'''
    expected_before = set(('in1', 'nd1', 'nd2', 'nd3', 'nd4', 'tx1_2', 'ln2_3', 'ln2_4', 'ld3'))
    expected_after = set(('in1', 'nd1', 'nd2', 'nd3', 'tx1_2', 'ln2_3', 'ld3'))

    netw = EJson.read_from_file(test_netws_path / 'netw_test_reduce_remove_hanging.json')
    assert set(x.cid for x in netw.components()) == expected_before
    reduce_network(netw)
    assert set(x.cid for x in netw.components()) == expected_after


def test_reduce_merge_shorts():
    ''' Test reduce where there are short circuit lines.'''
    expected_before = set(('in1', 'nd1', 'nd2', 'nd3', 'nd4', 'tx1_2', 'ln2_3', 'ln2_4', 'ld3', 'ld4'))
    expected_after = set(('in1', 'nd1', 'nd2', 'tx1_2', 'ld3', 'ld4'))

    netw = EJson.read_from_file(test_netws_path / 'netw_test_reduce_merge_shorts.json')
    assert set(x.cid for x in netw.components()) == expected_before
    reduce_network(netw)
    assert set(x.cid for x in netw.components()) == expected_after


def test_reduce_merge_dups():
    netw = EJson.read_from_file(test_netws_path / 'netw_test_reduce_merge_dups.json')
    reduce_network(netw)
    lines = list(netw.components('Line'))
    assert len(lines) == 1
    line = lines[0]
    assert line.cdata['z'] == [0.5, 0.5]
    assert line.cdata['z0'] == [0.5, 0.5]


def test_reduce():
    netw = EJson.read_from_file(test_netws_path / 'netw_test_reduce.json')
    assert len(list(netw.components('Line'))) == 11
    reduce_network(netw)
    line_ids = list(x.cid for x in netw.components('Line'))
    assert set(line_ids) == set(('ln2_3', 'ln4_5', 'ln5_6', 'ln6_8', 'ln6_7', 'ln9_10'))
    assert len(list(netw.components())) == 19


def test_audit():
    netw = EJson.read_from_file(test_netws_path / 'netw_generic_a.json')
    aud = audit(netw)
    for section in aud.values():
        assert len(section['problems']) == 0
