from unittest import TestCase

from ipipeline.exceptions import SortingError
from ipipeline.control.sorting import _check_diff_nodes_qty


class TestCheckDiffNodesQty(TestCase):
    def test_diff_nodes_qty(self) -> None:
        with self.assertRaisesRegex(
            SortingError, r'circular dependency found: curr_nodes_qty == 4'
        ):
            _check_diff_nodes_qty(7, 4)

    def test_equal_nodes_qty(self) -> None:
        _check_diff_nodes_qty(7, 7)

        self.assertTrue(True)