from unittest import TestCase

from ipipeline.exceptions import InstanceError
from ipipeline.structure.node import BaseNode, Node


def mock_sum(param1: int, param2: int = 0) -> int:
    return sum([param1, param2])


class TestBaseNode(TestCase):
    def test_valid_instance(self) -> None:
        base_node = BaseNode(
            'n1', 
            mock_sum, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sum'],
            tags=['math']
        )

        self.assertEqual(base_node.id, 'n1')
        self.assertEqual(base_node.func, mock_sum)
        self.assertDictEqual(base_node.inputs, {'param1': 7, 'param2': 3})
        self.assertListEqual(base_node.outputs, ['sum'])
        self.assertListEqual(base_node.props, [])
        self.assertListEqual(base_node.tags, ['math'])

    def test_invalid_instance(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == n1,'
        ):
            _ = BaseNode('n1,', None)

    def test_instance_repr(self) -> None:
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
    def test_base_class(self) -> None:
        node = Node('n1', None)
        
        self.assertIsInstance(node, BaseNode)
