from unittest import TestCase

from ipipeline.structure.node import Node


class TestNode(TestCase):
    def setUp(self) -> None:
        self._mock_task = lambda p: p

    def test_init__task_eq_callable__in_eq_dict__out_eq_list(self) -> None:
        node = Node(
            'n1', 
            self._mock_task, 
            inputs={'i1': 2}, 
            outputs=['o1'], 
            tags=['t1']
        )

        self.assertEqual(node.id, 'n1')
        self.assertEqual(node.task, self._mock_task)
        self.assertDictEqual(node.inputs, {'i1': 2})
        self.assertListEqual(node.outputs, ['o1'])
        self.assertListEqual(node.tags, ['t1'])
