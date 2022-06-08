from unittest import TestCase

from ipipeline.structure.node import Node


class TestNode(TestCase):
    def setUp(self) -> None:
        self._mock_tasks = [lambda p1: p1, lambda p2: p2]

    def test_init__task_eq_call__inputs_eq_dict__outputs_eq_list(self) -> None:
        node = Node(
            'n1', 
            self._mock_tasks[0], 
            inputs={'i1': 2}, 
            outputs=['o1'], 
            tags=['t1']
        )

        self.assertEqual(node._id, 'n1')
        self.assertEqual(node._task, self._mock_tasks[0])
        self.assertDictEqual(node._inputs, {'i1': 2})
        self.assertListEqual(node._outputs, ['o1'])
        self.assertListEqual(node._tags, ['t1'])

    def test_get__task_eq_call__inputs_eq_dict__outputs_eq_list(self) -> None:
        node = Node(
            'n1', 
            self._mock_tasks[0], 
            inputs={'i1': 2}, 
            outputs=['o1'], 
            tags=['t1']
        )

        self.assertEqual(node.task, self._mock_tasks[0])
        self.assertDictEqual(node.inputs, {'i1': 2})
        self.assertListEqual(node.outputs, ['o1'])

    def test_set__task_eq_call__inputs_eq_dict__outputs_eq_list(self) -> None:
        node = Node(
            'n1', 
            self._mock_tasks[0], 
            inputs={'i1': 2}, 
            outputs=['o1'], 
            tags=['t1']
        )
        node.task = self._mock_tasks[1]
        node.inputs = {'i2': 4}
        node.outputs = ['o2']

        self.assertEqual(node.task, self._mock_tasks[1])
        self.assertDictEqual(node.inputs, {'i2': 4})
        self.assertListEqual(node.outputs, ['o2'])
