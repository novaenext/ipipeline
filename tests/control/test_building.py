from unittest import TestCase

from ipipeline.control.building import (
    build_graph, build_key_args, build_pos_args, build_task_outputs
)
from ipipeline.exceptions import BuildingError
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


class TestBuildPosArgs(TestCase):
    def setUp(self) -> None:
        self._catalog = Catalog('c1', items={'i1': 2, 'i2': 4})

    def test_build_pos_args__pos_inputs_wi_ids(self) -> None:
        pos_args = build_pos_args(['i1', 'i2'], self._catalog)

        self.assertListEqual(pos_args, [2, 4])

    def test_build_pos_args__pos_inputs_wo_ids(self) -> None:
        pos_args = build_pos_args([], self._catalog)

        self.assertListEqual(pos_args, [])


class TestBuildKeyArgs(TestCase):
    def setUp(self) -> None:
        self._catalog = Catalog('c1', items={'i1': 2, 'i2': 4})

    def test_build_key_args__key_inputs_wi_ids(self) -> None:
        key_args = build_key_args({'p1': 'i1', 'p2': 'i2'}, self._catalog)

        self.assertDictEqual(key_args, {'p1': 2, 'p2': 4})

    def test_build_key_args__key_inputs_wo_ids(self) -> None:
        key_args = build_key_args({}, self._catalog)

        self.assertDictEqual(key_args, {})


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
