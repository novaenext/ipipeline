from unittest import TestCase

from ipipeline.exceptions import PipelineError
from ipipeline.structure.link import Link
from ipipeline.structure.node import Node
from ipipeline.structure.pipeline import Pipeline


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self._nodes = {'n1': Node('n1', None), 'n2': Node('n2', None)}
        self._links = {'l1': Link('l1', 'n1', 'n2')}
        self._task = [lambda arg1, arg2: arg1 + arg2]

    def test_init__args_eq_types(self) -> None:
        pipeline = Pipeline(
            'p1', nodes=self._nodes, links=self._links, tags=['t1']
        )

        self.assertEqual(pipeline._id, 'p1')
        self.assertDictEqual(pipeline._nodes, self._nodes)
        self.assertDictEqual(pipeline._links, self._links)
        self.assertListEqual(pipeline._tags, ['t1'])

    def test_get__args_eq_types(self) -> None:
        pipeline = Pipeline(
            'p1', nodes=self._nodes, links=self._links, tags=['t1']
        )

        self.assertEqual(pipeline.id, 'p1')
        self.assertDictEqual(pipeline.nodes, self._nodes)
        self.assertDictEqual(pipeline.links, self._links)
        self.assertListEqual(pipeline.tags, ['t1'])

    def test_set__args_eq_types(self) -> None:
        pipeline = Pipeline(
            'p1', nodes=self._nodes, links=self._links, tags=['t1']
        )
        pipeline.id = 'p2'
        pipeline.nodes = {'n3': None}
        pipeline.links = {'l2': None}
        pipeline.tags = ['t2']

        self.assertEqual(pipeline.id, 'p2')
        self.assertDictEqual(pipeline.nodes, {'n3': None})
        self.assertDictEqual(pipeline.links, {'l2': None})
        self.assertListEqual(pipeline.tags, ['t2'])

    def test_check_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)
        checked = pipeline.check_node('n1')

        self.assertTrue(checked)

    def test_check_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        checked = pipeline.check_node('n1')

        self.assertFalse(checked)

    def test_get_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)
        node = pipeline.get_node('n1')

        self.assertEqual(node, self._nodes['n1'])

    def test_get_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')

        with self.assertRaisesRegex(
            PipelineError, r'id was not found in the _nodes: id == n1'
        ):
            _ = pipeline.get_node('n1')

    def test_set_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)

        with self.assertRaisesRegex(
            PipelineError, r'id was found in the _nodes: id == n1'
        ):
            pipeline.set_node(self._nodes['n1'])

    def test_set_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.set_node(self._nodes['n1'])

        self.assertEqual(pipeline._nodes['n1'], self._nodes['n1'])

    def test_delete_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)
        pipeline.delete_node('n1')

        self.assertEqual(list(pipeline._nodes.keys()), ['n2'])

    def test_delete_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')

        with self.assertRaisesRegex(
            PipelineError, r'id was not found in the _nodes: id == n1'
        ):
            pipeline.delete_node('n1')

    def test_add_node__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)

        with self.assertRaisesRegex(
            PipelineError, r'id was found in the _nodes: id == n1'
        ):
            pipeline.add_node(
                'n1', 
                self._task, 
                key_inputs={'arg1': 2, 'arg2': 4}, 
                outputs=['sum']
            )

    def test_add_node__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.add_node(
            'n1', 
            self._task, 
            key_inputs={'arg1': 2, 'arg2': 4}, 
            outputs=['sum']
        )

        self.assertListEqual(list(pipeline.nodes.keys()), ['n1'])
        self.assertListEqual(
            [node.id for node in pipeline.nodes.values()], ['n1']
        )

    def test_check_link__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', links=self._links)
        checked = pipeline.check_link('l1')

        self.assertTrue(checked)

    def test_check_link__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        checked = pipeline.check_link('l1')

        self.assertFalse(checked)

    def test_get_link__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', links=self._links)
        link = pipeline.get_link('l1')

        self.assertEqual(link, self._links['l1'])

    def test_get_link__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')

        with self.assertRaisesRegex(
            PipelineError, r'id was not found in the _links: id == l1'
        ):
            _ = pipeline.get_link('l1')

    def test_set_link__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', links=self._links)

        with self.assertRaisesRegex(
            PipelineError, r'id was found in the _links: id == l1'
        ):
            pipeline.set_link(self._links['l1'])

    def test_set_link__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.set_link(self._links['l1'])

        self.assertEqual(pipeline._links['l1'], self._links['l1'])

    def test_delete_link__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', links=self._links)
        pipeline.delete_link('l1')

        self.assertEqual(list(pipeline._links.keys()), [])

    def test_delete_link__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')

        with self.assertRaisesRegex(
            PipelineError, r'id was not found in the _links: id == l1'
        ):
            pipeline.delete_link('l1')

    def test_add_link__id_eq_id(self) -> None:
        pipeline = Pipeline('p1', links=self._links)

        with self.assertRaisesRegex(
            PipelineError, r'id was found in the _links: id == l1'
        ):
            pipeline.add_link('l1', 'n1', 'n2')

    def test_add_link__id_ne_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.add_link('l1', 'n1', 'n2')

        self.assertListEqual(list(pipeline.links.keys()), ['l1'])
        self.assertListEqual(
            [link.id for link in pipeline.links.values()], ['l1']
        )
