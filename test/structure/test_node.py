from unittest import TestCase

from ipipeline.structure.node import BaseNode, Node


def mock_func(param1: int) -> int:
    return param1


class TestBaseNode(TestCase):
    def test_init(self) -> None:
        base_node = BaseNode(
            'n1', 
            mock_func, 
            inputs={'param1': 7}, 
            outputs=['return1'], 
            tags=['data']
        )

        self.assertEqual(base_node.id, 'n1')
        self.assertEqual(base_node.func, mock_func)
        self.assertDictEqual(base_node.inputs, {'param1': 7})
        self.assertListEqual(base_node.outputs, ['return1'])
        self.assertListEqual(base_node.tags, ['data'])


class TestNode(TestCase):
    def test_deriv(self) -> None:
        node = Node('n1', None)

        self.assertIsInstance(node, BaseNode)
