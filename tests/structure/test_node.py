from unittest import TestCase

from ipipeline.structure.node import Node


class TestNode(TestCase):
    def test_init(self) -> None:
        node = Node(
            'n1', 
            mock_func, 
            inputs={'param1': 7}, 
            outputs=['return1'], 
            tags=['data']
        )

        self.assertEqual(node.id, 'n1')
        self.assertEqual(node.func, mock_func)
        self.assertDictEqual(node.inputs, {'param1': 7})
        self.assertListEqual(node.outputs, ['return1'])
        self.assertListEqual(node.tags, ['data'])

    def test_defaults(self) -> None:
        node1 = Node('n1', mock_func) 
        node2 = Node('n2', mock_func) 

        self.assertIsNot(node1.inputs, node2.inputs)
        self.assertIsNot(node1.outputs, node2.outputs)


def mock_func(param1: int) -> int:
    return param1
