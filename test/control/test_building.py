from unittest import TestCase

from ipipeline.control.building import (
    build_func_inputs, build_func_outputs, _check_diff_outputs_qty
)
from ipipeline.control.catalog import Catalog
from ipipeline.exception import BuildingError, CatalogError


class TestBuildFuncInputs(TestCase):
    def setUp(self) -> None:
        self._catalog = Catalog()
        self._catalog._items = {'i1': 7, 'i2': 0}

    def test_single_inputs(self) -> None:
        func_inputs = build_func_inputs(
            {'in1': 'c.i1', 'in2': 'c.i2'}, self._catalog
        )

        self.assertDictEqual(func_inputs, {'in1': 7, 'in2': 0})

    def test_multiple_inputs(self) -> None:
        func_inputs = build_func_inputs(
            {'in1': 'c.[i1, i2]'}, self._catalog
        )

        self.assertDictEqual(func_inputs, {'in1': [7, 0]})

    def test_default_inputs(self) -> None:
        func_inputs = build_func_inputs(
            {'in1': 10, 'in2': 'python'}, self._catalog
        )

        self.assertDictEqual(func_inputs, {'in1': 10, 'in2': 'python'})

    def test_empty_inputs(self) -> None:
        func_inputs = build_func_inputs({}, self._catalog)

        self.assertDictEqual(func_inputs, {})

    def test_inexistent_inputs(self) -> None:
        with self.assertRaisesRegex(
            CatalogError, r'id not found in the _items: id == i3'
        ):
            _ = build_func_inputs(
                {'in1': 'c.i3', 'in2': 'c.i4'}, self._catalog
            )


class TestBuildFuncOutputs(TestCase):
    def test_single_outputs(self) -> None:
        func_outputs = build_func_outputs(['out1'], [7, 0])

        self.assertDictEqual(func_outputs, {'out1': [7, 0]})

    def test_multiple_outputs(self) -> None:
        func_outputs = build_func_outputs(['out1', 'out2'], [7, 0])

        self.assertDictEqual(func_outputs, {'out1': 7, 'out2': 0})

    def test_empty_outputs(self) -> None:
        func_outputs = build_func_outputs([], None)

        self.assertDictEqual(func_outputs, {})

    def test_diff_outputs1(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs_qty is not equal to the returns_qty: 2 != 1'
        ):
            _ = build_func_outputs(['out1', 'out2'], 7)

    def test_diff_outputs2(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs_qty is not equal to the returns_qty: 2 != 3'
        ):
            _ = build_func_outputs(['out1', 'out2'], [7, 0, 7])


class TestCheckDiffOutputsQty(TestCase):
    def test_diff_qty(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs_qty is not equal to the returns_qty: 2 != 1'
        ):
            _check_diff_outputs_qty(2, 1)

    def test_equal_qty(self) -> None:
        _check_diff_outputs_qty(1, 1)

        self.assertTrue(True)
