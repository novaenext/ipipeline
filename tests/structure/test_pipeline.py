from unittest import TestCase

from ipipeline.exceptions import PipelineError
from ipipeline.structure.pipeline import Pipeline


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self._graph = {'n1': [], 'n2': [], 'n3': [], 'n4': []}
        self._nodes = {'n1': None, 'n2': None, 'n3': None, 'n4': None}
        self._links = {'l1': None, 'l2': None, 'l3': None, 'l4': None}

    def test_init__graph_eq_dict__nodes_eq_dict__links_eq_dict(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._graph, 
            nodes=self._nodes, 
            links=self._links, 
            tags=['t1']
        )

        self.assertEqual(pipeline._id, 'p1')
        self.assertDictEqual(
            pipeline._graph, {'n1': [], 'n2': [], 'n3': [], 'n4': []}
        )
        self.assertDictEqual(
            pipeline._nodes, {'n1': None, 'n2': None, 'n3': None, 'n4': None}
        )
        self.assertDictEqual(
            pipeline._links, {'l1': None, 'l2': None, 'l3': None, 'l4': None}
        )
        self.assertListEqual(pipeline._tags, ['t1'])

    def test_get__graph_eq_dict__nodes_eq_dict__links_eq_dict(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._graph, 
            nodes=self._nodes, 
            links=self._links, 
            tags=['t1']
        )

        self.assertEqual(pipeline.id, 'p1')
        self.assertDictEqual(
            pipeline.graph, {'n1': [], 'n2': [], 'n3': [], 'n4': []}
        )
        self.assertDictEqual(
            pipeline.nodes, {'n1': None, 'n2': None, 'n3': None, 'n4': None}
        )
        self.assertDictEqual(
            pipeline.links, {'l1': None, 'l2': None, 'l3': None, 'l4': None}
        )
        self.assertListEqual(pipeline.tags, ['t1'])

    def test_set__graph_eq_dict__nodes_eq_dict__links_eq_dict(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._graph, 
            nodes=self._nodes, 
            links=self._links, 
            tags=['t1']
        )
        pipeline.id = 'p2'
        pipeline.graph = {'n5': []}
        pipeline.nodes = {'n5': None}
        pipeline.links = {'l5': None}
        pipeline.tags = ['t2']

        self.assertEqual(pipeline.id, 'p2')
        self.assertDictEqual(pipeline.graph, {'n5': []})
        self.assertDictEqual(pipeline.nodes, {'n5': None})
        self.assertDictEqual(pipeline.links, {'l5': None})
        self.assertListEqual(pipeline.tags, ['t2'])

    def test_check_node__id_eq_node_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)
        checked = pipeline.check_node('n2')

        self.assertTrue(checked)

    def test_check_node__id_ne_node_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)
        checked = pipeline.check_node('n8')

        self.assertFalse(checked)

    def test_add_inexistent_nodes(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=None, links=None, tags=None
        )
        pipeline.add_node(
            'n1', 
            mock_sum, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sum'], 
            tags=None
        )
        pipeline.add_node(
            'n2', 
            mock_sub, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sub'], 
            tags=None
        )

        self.assertListEqual(
            list(pipeline.nodes.keys()), ['n1', 'n2']
        )
        self.assertListEqual(
            [node.id for node in pipeline.nodes.values()], ['n1', 'n2']
        )
        self.assertListEqual(
            list(pipeline.graph.keys()), ['n1', 'n2']
        )
        self.assertListEqual(
            list(pipeline.graph.values()), [[], []]
        )

    def test_add_existent_nodes(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=None, links=None, tags=None
        )
        pipeline.add_node(
            'n1', 
            mock_sum, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sum'], 
            tags=None
        )

        with self.assertRaisesRegex(
            PipelineError, r'node_id found in the _nodes: node_id == n1'
        ):
            pipeline.add_node(
                'n1', 
                mock_sub, 
                inputs={'param1': 7, 'param2': 3}, 
                outputs=['sub'], 
                tags=None
            )

    def test_check_existent_node_id_aff(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=self._nodes, links=None, tags=None
        )

        with self.assertRaisesRegex(
            PipelineError, r'node_id found in the _nodes: node_id == n1'
        ):
            pipeline._check_existent_node_id('n1')

    def test_check_inexistent_node_id_aff(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=None, links=None, tags=None
        )
        pipeline._check_existent_node_id('n1')

        self.assertTrue(True)

    def test_add_inexistent_links_with_existent_nodes(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._graph, 
            nodes=self._nodes, 
            links=None, 
            tags=None
        )
        pipeline.add_link('l1', 'n1', 'n2', tags=None)
        pipeline.add_link('l2', 'n1', 'n3', tags=None)
        pipeline.add_link('l3', 'n2', 'n4', tags=None)

        self.assertListEqual(
            list(pipeline.links.keys()), ['l1', 'l2', 'l3']
        )
        self.assertListEqual(
            [link.id for link in pipeline.links.values()], 
            ['l1', 'l2', 'l3']
        )
        self.assertListEqual(
            list(pipeline.graph.keys()), ['n1', 'n2', 'n3', 'n4']
        )
        self.assertListEqual(
            list(pipeline.graph.values()), [['n2', 'n3'], ['n4'], [], []]
        )

    def test_add_existent_links_with_existent_nodes(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._graph, 
            nodes=self._nodes, 
            links=None, 
            tags=None
        )
        pipeline.add_link('l1', 'n1', 'n2', tags=None)
        pipeline.add_link('l2', 'n1', 'n3', tags=None)

        with self.assertRaisesRegex(
            PipelineError, r'link_id found in the _links: link_id == l1'
        ):
            pipeline.add_link('l1', 'n2', 'n4', tags=None)

    def test_add_inexistent_links_with_inexistent_src_node(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._graph, 
            nodes=self._nodes, 
            links=None, 
            tags=None
        )
        pipeline.add_link('l1', 'n1', 'n2', tags=None)
        pipeline.add_link('l2', 'n1', 'n3', tags=None)

        with self.assertRaisesRegex(
            PipelineError, r'node_id not found in the _nodes: node_id == n7'
        ):
            pipeline.add_link('l3', 'n7', 'n4', tags=None)

    def test_add_inexistent_links_with_inexistent_dst_node(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._graph, 
            nodes=self._nodes, 
            links=None, 
            tags=None
        )
        pipeline.add_link('l1', 'n1', 'n2', tags=None)
        pipeline.add_link('l2', 'n1', 'n3', tags=None)

        with self.assertRaisesRegex(
            PipelineError, r'node_id not found in the _nodes: node_id == n7'
        ):
            pipeline.add_link('l3', 'n2', 'n7', tags=None)

    def test_check_existent_link_id(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=None, links=self._links, tags=None
        )

        with self.assertRaisesRegex(
            PipelineError, r'link_id found in the _links: link_id == l1'
        ):
            pipeline._check_existent_link_id('l1')

    def test_check_inexistent_link_id(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=None, links=None, tags=None
        )
        pipeline._check_existent_link_id('l1')

        self.assertTrue(True)

    def test_check_inexistent_node_id_neg(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=None, links=None, tags=None
        )

        with self.assertRaisesRegex(
            PipelineError, r'node_id not found in the _nodes: node_id == n1'
        ):
            pipeline._check_inexistent_node_id('n1')

    def test_check_existent_node_id_neg(self) -> None:
        pipeline = Pipeline(
            'p1', graph=None, nodes=self._nodes, links=None, tags=None
        )
        pipeline._check_inexistent_node_id('n1')

        self.assertTrue(True)


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2
