from unittest import TestCase

from ipipeline.control.sorting import (
    sort_graph_topo, 
    _check_circular_dependency, 
    _get_incomings_qty, 
    _get_unbound_ids
)
from ipipeline.exceptions import SortingError


class TestSortGraphTopo(TestCase):
    def test_dag_with_linear_topo(self) -> None:
        topo_order = sort_graph_topo({
            'n1': ['n2'], 'n2': ['n3'], 'n3': ['n4'], 'n4': []
        })

        self.assertListEqual(topo_order, [['n1'], ['n2'], ['n3'], ['n4']])

    def test_dag_with_nonlinear_topo(self) -> None:
        topo_order = sort_graph_topo({
            'n1': ['n3', 'n4', 'n6'], 'n2': ['n5'], 'n3': ['n6'], 
            'n4': ['n3', 'n6', 'n7', 'n8'], 'n5': ['n8'], 'n6': [], 
            'n7': ['n9'], 'n8': [], 'n9': []
        })

        self.assertListEqual(
            topo_order, 
            [['n1', 'n2'], ['n4', 'n5'], ['n3', 'n7', 'n8'], ['n6', 'n9']]
        )

    def test_dcg_with_linear_topo(self) -> None:
        with self.assertRaisesRegex(
            SortingError, r'circular dependency found in the graph: 4 != 0'
        ):
            _ = sort_graph_topo({
                'n1': ['n2'], 'n2': ['n3'], 'n3': ['n4'], 'n4': ['n1']
            })

    def test_dcg_with_nonlinear_topo(self) -> None:
        with self.assertRaisesRegex(
            SortingError, r'circular dependency found in the graph: 9 != 3'
        ):
            _ = sort_graph_topo({
                'n1': ['n3', 'n4', 'n6'], 'n2': ['n5'], 'n3': ['n6'], 
                'n4': ['n3', 'n6', 'n7', 'n8'], 'n5': ['n8'], 'n6': ['n4'], 
                'n7': ['n9'], 'n8': [], 'n9': []
            })


class TestGetIncomingsQty(TestCase):
    def test_get_incomings_qty__graph_wi_src_ids_wi_dst_ids(self) -> None:
        incomings_qty = _get_incomings_qty(
            {'n1': ['n2', 'n3'], 'n2': ['n4'], 'n3': ['n4'], 'n4': []}
        )

        self.assertDictEqual(
            incomings_qty, {'n1': 0, 'n2': 1, 'n3': 1, 'n4': 2}
        )

    def test_get_incomings_qty__graph_wi_src_ids_wo_dst_ids(self) -> None:
        incomings_qty = _get_incomings_qty(
            {'n1': [], 'n2': [], 'n3': [], 'n4': []}
        )

        self.assertDictEqual(
            incomings_qty, {'n1': 0, 'n2': 0, 'n3': 0, 'n4': 0}
        )

    def test_get_incomings_qty__graph_wo_src_ids_wi_dst_ids(self) -> None:
        with self.assertRaisesRegex(
            SortingError, r'dst_id was not set as a src_id: dst_id == n4'
        ):
            _ = _get_incomings_qty(
                {'n1': ['n2', 'n3'], 'n2': ['n4'], 'n3': ['n4']}
            )

    def test_get_incomings_qty__graph_wo_src_ids_wo_dst_ids(self) -> None:
        incomings_qty = _get_incomings_qty({})

        self.assertDictEqual(incomings_qty, {})


class TestGetUnboundIds(TestCase):
    def test_get_unbound_ids__incomings_qty_wi_ids_wi_qty(self) -> None:
        unbound_ids = _get_unbound_ids({'n1': 1, 'n2': 2})

        self.assertListEqual(unbound_ids, [])

    def test_get_unbound_ids__incomings_qty_wi_ids_wo_qty(self) -> None:
        unbound_ids = _get_unbound_ids({'n1': 0, 'n2': 0})

        self.assertListEqual(unbound_ids, ['n1', 'n2'])

    def test_get_unbound_ids__incomings_qty_wo_ids_wo_qty(self) -> None:
        unbound_ids = _get_unbound_ids({})

        self.assertListEqual(unbound_ids, [])


class TestCheckCircularDependency(TestCase):
    def test_diff_nodes_qty(self) -> None:
        with self.assertRaisesRegex(
            SortingError, r'circular dependency found in the graph: 7 != 4'
        ):
            _check_circular_dependency(7, 4)

    def test_equal_nodes_qty(self) -> None:
        _check_circular_dependency(7, 7)

        self.assertTrue(True)
