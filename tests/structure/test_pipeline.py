from unittest import TestCase

from ipipeline.exceptions import PipelineError
from ipipeline.structure.pipeline import Pipeline


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self._mock_graph = {'n1': [], 'n2': []}
        self._mock_nodes = {'n1': None, 'n2': None}
        self._mock_links = {'l1': None}
        self._mock_node = object()
        self._mock_task = [lambda arg1, arg2: arg1 + arg2]

    def test_init__graph_eq_dict__nodes_eq_dict__links_eq_dict(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes, 
            links=self._mock_links, 
            tags=['t1']
        )

        self.assertEqual(pipeline._id, 'p1')
        self.assertDictEqual(pipeline._graph, {'n1': [], 'n2': []})
        self.assertDictEqual(pipeline._nodes, {'n1': None, 'n2': None})
        self.assertDictEqual(pipeline._links, {'l1': None})
        self.assertListEqual(pipeline._tags, ['t1'])

    def test_get__graph_eq_dict__nodes_eq_dict__links_eq_dict(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes, 
            links=self._mock_links, 
            tags=['t1']
        )

        self.assertEqual(pipeline.id, 'p1')
        self.assertDictEqual(pipeline.graph, {'n1': [], 'n2': []})
        self.assertDictEqual(pipeline.nodes, {'n1': None, 'n2': None})
        self.assertDictEqual(pipeline.links, {'l1': None})
        self.assertListEqual(pipeline.tags, ['t1'])

    def test_set__graph_eq_dict__nodes_eq_dict__links_eq_dict(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes, 
            links=self._mock_links, 
            tags=['t1']
        )
        pipeline.id = 'p2'
        pipeline.graph = {'n3': []}
        pipeline.nodes = {'n3': None}
        pipeline.links = {'l2': None}
        pipeline.tags = ['t2']

        self.assertEqual(pipeline.id, 'p2')
        self.assertDictEqual(pipeline.graph, {'n3': []})
        self.assertDictEqual(pipeline.nodes, {'n3': None})
        self.assertDictEqual(pipeline.links, {'l2': None})
        self.assertListEqual(pipeline.tags, ['t2'])

    def test_check_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._mock_nodes)
        checked = pipeline.check_node('n1')

        self.assertTrue(checked)

    def test_check_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        checked = pipeline.check_node('n1')

        self.assertFalse(checked)

    def test_add_node__id_eq_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes
        )

        with self.assertRaisesRegex(
            PipelineError, r'id was found in the _nodes: id == n1'
        ):
            pipeline.add_node(
                'n1', 
                self._mock_task, 
                inputs={'arg1': 2, 'arg2': 4}, 
                outputs=['sum']
            )

    def test_add_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.add_node(
            'n1', 
            self._mock_task, 
            inputs={'arg1': 2, 'arg2': 4}, 
            outputs=['sum']
        )

        self.assertListEqual(list(pipeline.graph.keys()), ['n1'])
        self.assertListEqual(list(pipeline.graph.values()), [[]])
        self.assertListEqual(list(pipeline.nodes.keys()), ['n1'])
        self.assertListEqual(
            [node.id for node in pipeline.nodes.values()], ['n1']
        )

    def test_get_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._mock_nodes)
        node = pipeline.get_node('n1')

        self.assertEqual(node, None)

    def test_get_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')

        with self.assertRaisesRegex(
            PipelineError, r'id was not found in the _nodes: id == n1'
        ):
            _ = pipeline.get_node('n1')

    def test_set_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._mock_nodes)
        pipeline.set_node('n1', self._mock_node)

        self.assertEqual(pipeline._nodes['n1'], self._mock_node)

    def test_set_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.set_node('n1', self._mock_node)

        self.assertEqual(pipeline._nodes['n1'], self._mock_node)

    def test_delete_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._mock_nodes)
        pipeline.delete_node('n1')

        self.assertEqual(list(pipeline._nodes.keys()), ['n2'])

    def test_delete_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')

        with self.assertRaisesRegex(
            PipelineError, r'id was not found in the _nodes: id == n1'
        ):
            pipeline.delete_node('n1')

    def test_check_link__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', links=self._mock_links)
        checked = pipeline.check_link('l1')

        self.assertTrue(checked)

    def test_check_link__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        checked = pipeline.check_link('l1')

        self.assertFalse(checked)

    def test_add_link__id_eq_id__src_id_eq_id__dst_id_eq_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes, 
            links=self._mock_links
        )

        with self.assertRaisesRegex(
            PipelineError, r'id was found in the _links: id == l1'
        ):
            pipeline.add_link('l1', 'n1', 'n2')

    def test_add_link__id_ne_id__src_id_eq_id__dst_id_eq_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes
        )
        pipeline.add_link('l1', 'n1', 'n2')

        self.assertListEqual(list(pipeline.graph.keys()), ['n1', 'n2'])
        self.assertListEqual(list(pipeline.graph.values()), [['n2'], []])
        self.assertListEqual(list(pipeline.links.keys()), ['l1'])
        self.assertListEqual(
            [link.id for link in pipeline.links.values()], ['l1']
        )

    def test_add_link__id_ne_id__src_id_ne_id__dst_id_eq_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes
        )

        with self.assertRaisesRegex(
            PipelineError, r'src_id was not found in the _nodes: src_id == n0'
        ):
            pipeline.add_link('l1', 'n0', 'n1')

    def test_add_link__id_ne_id__src_id_eq_id__dst_id_ne_id(self) -> None:
        pipeline = Pipeline(
            'p1', 
            graph=self._mock_graph, 
            nodes=self._mock_nodes
        )

        with self.assertRaisesRegex(
            PipelineError, r'dst_id was not found in the _nodes: dst_id == n3'
        ):
            pipeline.add_link('l1', 'n2', 'n3')
