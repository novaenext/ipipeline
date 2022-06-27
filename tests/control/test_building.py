from unittest import TestCase

from ipipeline.control.building import (
    build_graph, build_inputs, build_task_outputs, _check_diff_outputs_qty
)
from ipipeline.exceptions import BuildingError, CatalogError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.link import Link
from ipipeline.structure.node import Node
from ipipeline.structure.pipeline import Pipeline


class TestBuildGraph(TestCase):
    def test_build_graph__pipeline_wi_src_ids_wi_dst_ids(self) -> None:
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

    def test_build_graph__pipeline_wi_src_ids_wo_dst_ids(self) -> None:
        pipeline = Pipeline(
            'p1', {'n1': Node('n1', None)}, {'l1': Link('l1', 'n1', 'n2')}
        )

        with self.assertRaisesRegex(
            BuildingError, 
            r'dst_id was not found in the pipeline._nodes: dst_id == n2'
        ):
            _ = build_graph(pipeline)

    def test_build_graph__pipeline_wo_src_ids_wi_dst_ids(self) -> None:
        pipeline = Pipeline(
            'p1', {'n2': Node('n2', None)}, {'l1': Link('l1', 'n1', 'n2')}
        )

        with self.assertRaisesRegex(
            BuildingError, 
            r'src_id was not found in the pipeline._nodes: src_id == n1'
        ):
            _ = build_graph(pipeline)

    def test_build_graph__pipeline_wo_src_ids_wo_dst_ids(self) -> None:
        pipeline = Pipeline('p1')
        graph = build_graph(pipeline)

        self.assertDictEqual(graph, {})

    def test_build_graph__pipeline_wi_duplicate_dst_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            {'n1': Node('n1', None), 'n2': Node('n2', None)}, 
            {'l1': Link('l1', 'n1', 'n2'), 'l2': Link('l2', 'n1', 'n2')}
        )

        with self.assertRaisesRegex(
            BuildingError, 
            r'dst_id was found in the graph\[link.src_id\]: dst_id == n2'
        ):
            _ = build_graph(pipeline)

    def test_build_graph__pipeline_wo_duplicate_dst_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            {'n1': Node('n1', None), 'n2': Node('n2', None)}, 
            {'l1': Link('l1', 'n1', 'n2')}
        )
        graph = build_graph(pipeline)

        self.assertDictEqual(graph, {'n1': ['n2'], 'n2': []})


class TestBuildInputs(TestCase):
    def setUp(self) -> None:
        self._catalog = Catalog('c1', items={'i1': 2, 'i2': 4})

    def test_build_inputs__inputs_eq_list_wi_ids(self) -> None:
        built_inputs = build_inputs(['i1', 'i2'], self._catalog)

        self.assertListEqual(built_inputs, [2, 4])

    def test_build_inputs__inputs_eq_list_wo_ids(self) -> None:
        built_inputs = build_inputs([], self._catalog)

        self.assertListEqual(built_inputs, [])

    def test_build_inputs__inputs_eq_dict_wi_ids(self) -> None:
        built_inputs = build_inputs({'p1': 'i1', 'p2': 'i2'}, self._catalog)

        self.assertDictEqual(built_inputs, {'p1': 2, 'p2': 4})

    def test_build_inputs__inputs_eq_dict_wo_ids(self) -> None:
        built_inputs = build_inputs({}, self._catalog)

        self.assertDictEqual(built_inputs, {})

    def test_build_inputs__inputs_eq_str_wi_id(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'inputs is not an instance of a list or dict: '
            r'type == <class \'str\'>'
        ):
            _ = build_inputs('i1', self._catalog)

    def test_build_inputs__inputs_eq_str_wo_id(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'inputs is not an instance of a list or dict: '
            r'type == <class \'str\'>'
        ):
            _ = build_inputs('', self._catalog)


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
