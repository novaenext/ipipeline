from unittest import TestCase

from ipipeline.control.building import (
    build_graph, build_task_inputs, build_task_outputs, _check_diff_outputs_qty
)
from ipipeline.exceptions import BuildingError, CatalogError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.link import Link
from ipipeline.structure.node import Node
from ipipeline.structure.pipeline import Pipeline


class TestBuildGraph(TestCase):
    def test_build_graph__pipe_eq_class_wi_src_id_wi_dst_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            {
                'n1': Node('n1', None), 
                'n2': Node('n2', None), 
                'n3': Node('n3', None), 
                'n4': Node('n4', None)
            }, 
            {
                'l1': Link('l1', 'n1', 'n2'), 
                'l2': Link('l2', 'n1', 'n3'), 
                'l3': Link('l3', 'n2', 'n4')
            }
        )
        graph = build_graph(pipeline)

        self.assertDictEqual(
            graph, {'n1': ['n2', 'n3'], 'n2': ['n4'], 'n3': [], 'n4': []}
        )

    def test_build_graph__pipe_eq_class_wo_src_id_wi_dst_id(self) -> None:
        pipeline = Pipeline(
            'p1', {'n2': Node('n2', None)}, {'l1': Link('l1', 'n1', 'n2')}
        )

        with self.assertRaisesRegex(
            BuildingError, 
            r'src_id was not found in the pipeline._nodes: src_id == n1'
        ):
            _ = build_graph(pipeline)

    def test_build_graph__pipe_eq_class_wi_src_id_wo_dst_id(self) -> None:
        pipeline = Pipeline(
            'p1', {'n1': Node('n1', None)}, {'l1': Link('l1', 'n1', 'n2')}
        )

        with self.assertRaisesRegex(
            BuildingError, 
            r'dst_id was not found in the pipeline._nodes: dst_id == n2'
        ):
            _ = build_graph(pipeline)

    def test_build_graph__pipe_eq_class_wi_empty_links(self) -> None:
        pipeline = Pipeline('p1')
        graph = build_graph(pipeline)

        self.assertDictEqual(graph, {})


class TestBuildTaskInputs(TestCase):
    def setUp(self) -> None:
        self._catalog = Catalog('c1', items={'i1': 7, 'i2': 0})

    def test_single_placeholders(self) -> None:
        func_inputs = build_task_inputs(
            {'in1': 'c.i1', 'in2': 'c.i2'}, self._catalog
        )

        self.assertDictEqual(func_inputs, {'in1': 7, 'in2': 0})

    def test_multiple_placeholders(self) -> None:
        func_inputs = build_task_inputs(
            {'in1': 'c.[i1, i2]', 'in2': 'c.[i1]'}, self._catalog
        )

        self.assertDictEqual(func_inputs, {'in1': [7, 0], 'in2': [7]})

    def test_invalid_placeholders(self) -> None:
        with self.assertRaisesRegex(
            CatalogError, r'id was not found in the _items: id == i3'
        ):
            _ = build_task_inputs(
                {'in1': 'c.i3', 'in2': 'c.[]'}, self._catalog
            )

    def test_default_values(self) -> None:
        func_inputs = build_task_inputs(
            {'in1': 10, 'in2': 'python'}, self._catalog
        )

        self.assertDictEqual(func_inputs, {'in1': 10, 'in2': 'python'})

    def test_empty_values(self) -> None:
        func_inputs = build_task_inputs({}, self._catalog)

        self.assertDictEqual(func_inputs, {})


class TestBuildTaskOutputs(TestCase):
    def test_single_outputs(self) -> None:
        func_outputs = build_task_outputs(['out1'], [7, 0])

        self.assertDictEqual(func_outputs, {'out1': [7, 0]})

    def test_multiple_outputs(self) -> None:
        func_outputs = build_task_outputs(['out1', 'out2'], [7, 0])

        self.assertDictEqual(func_outputs, {'out1': 7, 'out2': 0})

    def test_empty_outputs(self) -> None:
        func_outputs = build_task_outputs([], None)

        self.assertDictEqual(func_outputs, {})

    def test_invalid_outputs(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs_qty is not equal to the returns_qty: 2 != 1'
        ):
            _ = build_task_outputs(['out1', 'out2'], 7)


class TestCheckDiffOutputsQty(TestCase):
    def test_diff_outputs_qty(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs_qty is not equal to the returns_qty: 2 != 1'
        ):
            _check_diff_outputs_qty(2, 1)

    def test_equal_outputs_qty(self) -> None:
        _check_diff_outputs_qty(1, 1)

        self.assertTrue(True)
