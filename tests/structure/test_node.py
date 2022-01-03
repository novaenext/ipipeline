from unittest import TestCase

from ipipeline.structure.node import Node


class TestNode(TestCase):
    def test_init(self) -> None:
        node = Node(
            'n1', 
            mock_task, 
            inputs={'param1': 7}, 
            outputs=['return1'], 
            tags=['data']
        )

        self.assertEqual(node.id, 'n1')
        self.assertEqual(node.task, mock_task)
        self.assertDictEqual(node.inputs, {'param1': 7})
        self.assertListEqual(node.outputs, ['return1'])
        self.assertListEqual(node.tags, ['data'])

    def test_defaults(self) -> None:
        node1 = Node('n1', mock_task) 
        node2 = Node('n2', mock_task) 

        self.assertIsNot(node1.inputs, node2.inputs)
        self.assertIsNot(node1.outputs, node2.outputs)


def mock_task(param1: int) -> int:
    return param1
