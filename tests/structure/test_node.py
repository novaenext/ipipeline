from unittest import TestCase

from ipipeline.exceptions import InstanceError
from ipipeline.structure.node import BaseNode, Node


def mock_func(param1: int) -> int:
    return param1


class TestBaseNode(TestCase):
    def test_init_valid_args(self) -> None:
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
        self.assertListEqual(base_node.props, [])
        self.assertListEqual(base_node.tags, ['data'])

    def test_init_invalid_args(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == n1,'
        ):
            _ = BaseNode('n1,', None)

    def test_repr(self) -> None:
        base_node = BaseNode('n1', None)
        instance_repr = base_node.__repr__()

        self.assertEqual(
            instance_repr, 
            'BaseNode('
                'id_=\'n1\', '
                'func=None, '
                'inputs={}, '
                'outputs=[], '
                'props=[], '
                'tags=[]'
            ')'
        )


class TestNode(TestCase):
    def test_new_valid_args(self) -> None:
        node = Node('n1', None)
        
        self.assertIsInstance(node, BaseNode)
