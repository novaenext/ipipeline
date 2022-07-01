from unittest import TestCase

from ipipeline.structure.node import Node


class TestNode(TestCase):
    def setUp(self) -> None:
        self._tasks = [lambda arg1: arg1, lambda arg2: arg2]

    def test_init__args_eq_types(self) -> None:
        node = Node(
            'n1', 
            self._tasks[0], 
            pos_inputs=[2], 
            key_inputs={'i1': 2}, 
            outputs=['o1'], 
            tags=['t1']
        )

        self.assertEqual(node._id, 'n1')
        self.assertEqual(node._task, self._tasks[0])
        self.assertListEqual(node._pos_inputs, [2])
        self.assertDictEqual(node._key_inputs, {'i1': 2})
        self.assertListEqual(node._outputs, ['o1'])
        self.assertListEqual(node._tags, ['t1'])

    def test_get__args_eq_types(self) -> None:
        node = Node(
            'n1', 
            self._tasks[0], 
            pos_inputs=[2], 
            key_inputs={'i1': 2}, 
            outputs=['o1'], 
            tags=['t1']
        )

        self.assertEqual(node.id, 'n1')
        self.assertEqual(node.task, self._tasks[0])
        self.assertListEqual(node.pos_inputs, [2])
        self.assertDictEqual(node.key_inputs, {'i1': 2})
        self.assertListEqual(node.outputs, ['o1'])
        self.assertListEqual(node.tags, ['t1'])

    def test_set__args_eq_types(self) -> None:
        node = Node(
            'n1', 
            self._tasks[0], 
            pos_inputs=[2], 
            key_inputs={'i1': 2}, 
            outputs=['o1'], 
            tags=['t1']
        )
        node.id = 'n2'
        node.task = self._tasks[1]
        node.pos_inputs = [4]
        node.key_inputs = {'i2': 4}
        node.outputs = ['o2']
        node.tags = ['t2']

        self.assertEqual(node.id, 'n2')
        self.assertEqual(node.task, self._tasks[1])
        self.assertListEqual(node.pos_inputs, [4])
        self.assertDictEqual(node.key_inputs, {'i2': 4})
        self.assertListEqual(node.outputs, ['o2'])
        self.assertListEqual(node.tags, ['t2'])
