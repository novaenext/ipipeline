from unittest import TestCase

from ipipeline.control.building import build_graph, build_items
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


class TestBuildItems(TestCase):
    def test_build_items__outputs_wi_one__returns_wi_one(self) -> None:
        items = build_items(['o1'], ['r1'])

        self.assertDictEqual(items, {'o1': ['r1']})

    def test_build_items__outputs_wi_one__returns_wi_zero(self) -> None:
        items = build_items(['o1'], None)

        self.assertDictEqual(items, {'o1': None})

    def test_build_items__outputs_wi_zero__returns_wi_one(self) -> None:
        items = build_items([], ['r1'])

        self.assertDictEqual(items, {})

    def test_build_items__outputs_wi_zero__returns_wi_zero(self) -> None:
        items = build_items([], None)

        self.assertDictEqual(items, {})

    def test_build_items__outputs_wi_two__returns_wi_two(self) -> None:
        items = build_items(['o1', 'o2'], ['r1', 'r2'])

        self.assertDictEqual(items, {'o1': 'r1', 'o2': 'r2'})

    def test_build_items__outputs_wi_two__returns_wi_zero(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'invalid type was found for the returns: '
            r'type == <class \'NoneType\'>'
        ):
            _ = build_items(['o1', 'o2'], None)

    def test_build_items__outputs_wi_two__returns_wi_one(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs did not match the returns in terms of size: 2 != 1'
        ):
            _ = build_items(['o1', 'o2'], ['r1'])

    def test_build_items__outputs_wi_one__returns_wi_two(self) -> None:
        items = build_items(['o1'], ['r1', 'r2'])

        self.assertDictEqual(items, {'o1': ['r1', 'r2']})

    def test_build_items__outputs_wi_three__returns_wi_three(self) -> None:
        items = build_items(['o1', 'o2', 'o3'], ['r1', 'r2', 'r3'])

        self.assertDictEqual(items, {'o1': 'r1', 'o2': 'r2', 'o3': 'r3'})

    def test_build_items__outputs_wi_three__returns_wi_two(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs did not match the returns in terms of size: 3 != 2'
        ):
            _ = build_items(['o1', 'o2', 'o3'], ['r1', 'r2'])

    def test_build_items__outputs_wi_two__returns_wi_three(self) -> None:
        with self.assertRaisesRegex(
            BuildingError, 
            r'outputs did not match the returns in terms of size: 2 != 3'
        ):
            _ = build_items(['o1', 'o2'], ['r1', 'r2', 'r3'])
