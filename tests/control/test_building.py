from unittest import TestCase

from ipipeline.control.building import (
    build_func_inputs, build_func_outputs, _check_diff_outputs_qty
)
from ipipeline.exception import BuildingError


class TestBuildFuncInputs(TestCase):
    def test_inputs_with_valid_items(self) -> None:
        func_inputs = build_func_inputs(
            {'in1': 'c.i1', 'in2': 'c.i2'}, {'i1': 7, 'i2': 0}
        )

        self.assertDictEqual(func_inputs, {'in1': 7, 'in2': 0})

    def test_inputs_with_invalid_items(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'in_value not found in the items: in_value == c\.i11'
        ):
            _ = build_func_inputs(
                {'in1': 'c.i11', 'in2': 'c.i22'}, {'i1': 7, 'i2': 0}
            )

    def test_inputs_with_defaults(self) -> None:
        func_inputs = build_func_inputs({'i1': 7, 'i2': '0'}, {})

        self.assertDictEqual(func_inputs, {'i1': 7, 'i2': '0'})

    def test_inputs_without_defaults(self) -> None:
        func_inputs = build_func_inputs({}, {'i1': 7, 'i2': 0})

        self.assertDictEqual(func_inputs, {})


class TestBuildFuncOutputs(TestCase):
    def test_single_outputs(self) -> None:
        func_outputs = build_func_outputs(['o1'], [7, 0])

        self.assertDictEqual(func_outputs, {'o1': [7, 0]})

    def test_multiple_outputs(self) -> None:
        func_outputs = build_func_outputs(['o1', 'o2'], [7, 0])

        self.assertDictEqual(func_outputs, {'o1': 7, 'o2': 0})

    def test_empty_outputs(self) -> None:
        func_outputs = build_func_outputs([], None)

        self.assertDictEqual(func_outputs, {})

    def test_diff_outputs1(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs_qty is not equal to the returns_qty: 2 != 1'
        ):
            _ = build_func_outputs(['o1', 'o2'], 7)

    def test_diff_outputs2(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs_qty is not equal to the returns_qty: 2 != 3'
        ):
            _ = build_func_outputs(['o1', 'o2'], [7, 0, 7])


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
