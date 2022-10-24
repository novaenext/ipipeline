from unittest import TestCase

from ipipeline.exceptions import NodeError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.node import Node


class TestNode(TestCase):
    def setUp(self) -> None:
        self._catalog = Catalog('c1', items={'i1': 2, 'i2': 4})
        self._tasks = [lambda p1, p2: [p1, p2], lambda p1, p2: (p1, p2)]

    def test_init__args_eq_types(self) -> None:
        node = Node(
            'n1', 
            self._tasks[0], 
            pos_inputs=['i1'], 
            key_inputs={'p2': 'i2'}, 
            outputs=['o1'], 
            tags=['t1']
        )

        self.assertEqual(node._id, 'n1')
        self.assertEqual(node._task, self._tasks[0])
        self.assertListEqual(node._pos_inputs, ['i1'])
        self.assertDictEqual(node._key_inputs, {'p2': 'i2'})
        self.assertListEqual(node._outputs, ['o1'])
        self.assertListEqual(node._tags, ['t1'])

    def test_get__args_eq_types(self) -> None:
        node = Node(
            'n1', 
            self._tasks[0], 
            pos_inputs=['i1'], 
            key_inputs={'p2': 'i2'}, 
            outputs=['o1'], 
            tags=['t1']
        )

        self.assertEqual(node.id, 'n1')
        self.assertEqual(node.task, self._tasks[0])
        self.assertListEqual(node.pos_inputs, ['i1'])
        self.assertDictEqual(node.key_inputs, {'p2': 'i2'})
        self.assertListEqual(node.outputs, ['o1'])
        self.assertListEqual(node.tags, ['t1'])

    def test_set__args_eq_types(self) -> None:
        node = Node(
            'n1', 
            self._tasks[0], 
            pos_inputs=['i1'], 
            key_inputs={'p2': 'i2'}, 
            outputs=['o1'], 
            tags=['t1']
        )
        node.id = 'n2'
        node.task = self._tasks[1]
        node.pos_inputs = ['i3']
        node.key_inputs = {'p4': 'i4'}
        node.outputs = ['o2']
        node.tags = ['t2']

        self.assertEqual(node.id, 'n2')
        self.assertEqual(node.task, self._tasks[1])
        self.assertListEqual(node.pos_inputs, ['i3'])
        self.assertDictEqual(node.key_inputs, {'p4': 'i4'})
        self.assertListEqual(node.outputs, ['o2'])
        self.assertListEqual(node.tags, ['t2'])

    def test_build_pos_args__pos_inputs_wi_ids(self) -> None:
        node = Node('n1', self._tasks[0], pos_inputs=['i1', 'i2'])
        pos_args = node.build_pos_args(self._catalog)

        self.assertListEqual(pos_args, [2, 4])

    def test_build_pos_args__pos_inputs_wo_ids(self) -> None:
        node = Node('n1', self._tasks[0], pos_inputs=[])
        pos_args = node.build_pos_args(self._catalog)

        self.assertListEqual(pos_args, [])

    def test_build_key_args__key_inputs_wi_ids(self) -> None:
        node = Node('n1', self._tasks[0], key_inputs={'p1': 'i1', 'p2': 'i2'})
        key_args = node.build_key_args(self._catalog)

        self.assertDictEqual(key_args, {'p1': 2, 'p2': 4})

    def test_build_key_args__key_inputs_wo_ids(self) -> None:
        node = Node('n1', self._tasks[0], key_inputs={})
        key_args = node.build_key_args(self._catalog)

        self.assertDictEqual(key_args, {})

    def test_execute_task__args_wi_values(self) -> None:
        node = Node('n1', self._tasks[0])
        results = node.execute_task([2], {'p2': 4})

        self.assertListEqual(results, [2, 4])

    def test_execute_task__args_wo_values(self) -> None:
        node = Node('n1', self._tasks[0])

        with self.assertRaisesRegex(
            NodeError, r'task was not executed: id == n1'
        ):
            _ = node.execute_task([], {})

    def test_build_items__outputs_wi_one__results_wi_one(self) -> None:
        node = Node('n1', None, outputs=['o1'])
        items = node.build_items(['r1'])

        self.assertDictEqual(items, {'o1': ['r1']})

    def test_build_items__outputs_wi_one__results_wi_zero(self) -> None:
        node = Node('n1', None, outputs=['o1'])
        items = node.build_items([])

        self.assertDictEqual(items, {'o1': []})

    def test_build_items__outputs_wi_zero__results_wi_one(self) -> None:
        node = Node('n1', None, outputs=[])
        items = node.build_items(['r1'])

        self.assertDictEqual(items, {})

    def test_build_items__outputs_wi_zero__results_wi_zero(self) -> None:
        node = Node('n1', None, outputs=[])
        items = node.build_items([])

        self.assertDictEqual(items, {})

    def test_build_items__outputs_wi_two__results_wi_two(self) -> None:
        node = Node('n1', None, outputs=['o1', 'o2'])
        items = node.build_items(['r1', 'r2'])

        self.assertDictEqual(items, {'o1': 'r1', 'o2': 'r2'})

    def test_build_items__outputs_wi_two__results_wi_zero(self) -> None:
        node = Node('n1', None, outputs=['o1', 'o2'])

        with self.assertRaisesRegex(
            NodeError, 
            r'outputs did not match the results in terms of size: 2 != 0'
        ):
            _ = node.build_items([])

    def test_build_items__outputs_wi_two__results_wi_one(self) -> None:
        node = Node('n1', None, outputs=['o1', 'o2'])

        with self.assertRaisesRegex(
            NodeError, 
            r'outputs did not match the results in terms of size: 2 != 1'
        ):
            _ = node.build_items(['r1'])

    def test_build_items__outputs_wi_one__results_wi_two(self) -> None:
        node = Node('n1', None, outputs=['o1'])
        items = node.build_items(['r1', 'r2'])

        self.assertDictEqual(items, {'o1': ['r1', 'r2']})

    def test_build_items__outputs_wi_three__results_wi_three(self) -> None:
        node = Node('n1', None, outputs=['o1', 'o2', 'o3'])
        items =node.build_items(['r1', 'r2', 'r3'])

        self.assertDictEqual(items, {'o1': 'r1', 'o2': 'r2', 'o3': 'r3'})

    def test_build_items__outputs_wi_three__results_wi_two(self) -> None:
        node = Node('n1', None, outputs=['o1', 'o2', 'o3'])

        with self.assertRaisesRegex(
            NodeError, 
            r'outputs did not match the results in terms of size: 3 != 2'
        ):
            _ = node.build_items(['r1', 'r2'])

    def test_build_items__outputs_wi_two__results_wi_three(self) -> None:
        node = Node('n1', None, outputs=['o1', 'o2'])

        with self.assertRaisesRegex(
            NodeError, 
            r'outputs did not match the results in terms of size: 2 != 3'
        ):
            _ = node.build_items(['r1', 'r2', 'r3'])

    def test_build_items__outputs_wi_none__results_wo_none(self) -> None:
        node = Node('n1', None, outputs=None)
        items = node.build_items('r1')

        self.assertDictEqual(items, {})

    def test_build_items__outputs_wo_none__results_wi_none(self) -> None:
        node = Node('n1', None, outputs=['o1'])
        items = node.build_items(None)

        self.assertDictEqual(items, {'o1': None})

    def test_build_items__outputs_wi_none__results_wi_none(self) -> None:
        node = Node('n1', None, outputs=None)
        items = node.build_items(None)

        self.assertDictEqual(items, {})

    def test_build_items__outputs_wo_none__results_wo_none(self) -> None:
        node = Node('n1', None, outputs=['o1'])
        items = node.build_items('r1')

        self.assertDictEqual(items, {'o1': 'r1'})
