from unittest import TestCase

from ipipeline.exceptions import SortingError
from ipipeline.control.sorting import (
    _create_ind_node_ids, _check_diff_nodes_qty
)


class TestCreateIndNodeIds(TestCase):
    def test_node_ids_without_in_conns(self) -> None:
        ind_node_ids = _create_ind_node_ids({'n1': 0, 'n2': 0})

        self.assertListEqual(ind_node_ids, ['n1', 'n2'])

    def test_node_ids_with_in_conns(self) -> None:
        ind_node_ids = _create_ind_node_ids({'n1': 1, 'n2': 2})

        self.assertListEqual(ind_node_ids, [])


class TestCheckDiffNodesQty(TestCase):
    def test_diff_nodes_qty(self) -> None:
        with self.assertRaisesRegex(
            SortingError, r'circular dependency found: curr_nodes_qty == 4'
        ):
            _check_diff_nodes_qty(7, 4)

    def test_equal_nodes_qty(self) -> None:
        _check_diff_nodes_qty(7, 7)

        self.assertTrue(True)