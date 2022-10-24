from unittest import TestCase

from ipipeline.control.building import build_graph
from ipipeline.exceptions import BuildingError
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
