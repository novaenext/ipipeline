from unittest import TestCase
from unittest.mock import Mock

from ipipeline.exceptions import ExecutionError, InstanceError
from ipipeline.control.execution import BaseExecutor, SequentialExecutor


class MockBaseExecutor(BaseExecutor):
    def execute_pipeline(self) -> None:
        pass


class TestBaseExecutor(TestCase):
    def test_init_valid_args(self) -> None:
        base_executor = MockBaseExecutor('e1', tags=['data'])

        self.assertEqual(base_executor.id, 'e1')
        self.assertDictEqual(base_executor._catalog._items, {})
        self.assertListEqual(base_executor.tags, ['data'])

    def test_init_invalid_args(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == e1,'
        ):
            _ = MockBaseExecutor('e1,')

    def test_repr(self) -> None:
        base_executor = MockBaseExecutor('e1')
        instance_repr = base_executor.__repr__()

        self.assertEqual(
            instance_repr, 'MockBaseExecutor(id_=\'e1\', tags=[])'
        )


def mock_mul(param1: int, param2: int) -> int:
    return param1 * param2


def mock_print(param3: int) -> None:
    print(param3)


class TestSequentialExecutor(TestCase):
    def setUp(self) -> None:
        mock_nodes = {}

        for node_id, func, inputs, outputs in [
            ['n1', mock_mul, {'param1': 7, 'param2': 2}, ['param3']],
            ['n2', mock_print, {'n1': ['param3']}, []]
        ]:
            mock_nodes[node_id] = Mock(
                spec=['id', 'func', 'inputs', 'outputs', 'props', 'tags']
            )
            mock_nodes[node_id].id = node_id
            mock_nodes[node_id].func = func
            mock_nodes[node_id].inputs = inputs
            mock_nodes[node_id].outputs = outputs

        self._mock_pipeline = Mock(
            spec=['id', 'nodes', 'conns', 'graph', 'tags']
        )
        self._mock_pipeline.id = 'p1'
        self._mock_pipeline.nodes = mock_nodes

    def test_new_valid_args(self) -> None:
        executor = SequentialExecutor('e1')
        
        self.assertIsInstance(executor, BaseExecutor)

    def test_execute_pipeline_valid_topo_order(self) -> None:
        executor = SequentialExecutor('e1')
        items = executor.execute_pipeline(self._mock_pipeline, ['n1', 'n2'])

        self.assertDictEqual(items, {'n1': {'param3': 14}})

    def test_execute_pipeline_invalid_topo_order(self) -> None:
        executor = SequentialExecutor('e1')

        with self.assertRaisesRegex(
            ExecutionError, r'node_func not executed: node_id == n2'
        ):
            _ = executor.execute_pipeline(self._mock_pipeline, ['n2', 'n1'])

    def test_execute_pipeline_empty_topo_order(self) -> None:
        executor = SequentialExecutor('e1')
        items = executor.execute_pipeline(self._mock_pipeline, [])

        self.assertDictEqual(items, {})

    def test_create_func_inputs_valid_input_keys(self) -> None:
        executor = SequentialExecutor('e1')
        func_inputs = executor._create_func_inputs({'param1': 7, 'param2': 2})

        self.assertDictEqual(func_inputs, {'param1': 7, 'param2': 2})

    def test_create_func_inputs_valid_output_keys(self) -> None:
        executor = SequentialExecutor('e1')
        executor._catalog._items = {'n1': {'param1': 7}, 'n2': {'param2': 2}}
        func_inputs = executor._create_func_inputs(
            {'n1': ['param1'], 'n2': ['param2']}
        )

        self.assertDictEqual(func_inputs, {'param1': 7, 'param2': 2})

    def test_create_func_inputs_valid_mix_keys(self) -> None:
        executor = SequentialExecutor('e1')
        executor._catalog._items = {'n1': {'param1': 7, 'param2': 2}}
        func_inputs = executor._create_func_inputs(
            {'n1': ['param1', 'param2'], 'param3': 0}
        )

        self.assertDictEqual(
            func_inputs, {'param1': 7, 'param2': 2, 'param3': 0}
        )

    def test_create_func_inputs_invalid_output_keys(self) -> None:
        executor = SequentialExecutor('e1')
        executor._catalog._items = {'n1': {'param1': 7}}

        with self.assertRaisesRegex(
            ExecutionError, 
            r'output_key not found: input_key == n1 and output_key == param2'
        ):
            _ = executor._create_func_inputs({'n1': ['param1', 'param2']})

    def test_execute_func_valid_inputs(self) -> None:
        executor = SequentialExecutor('e1')
        unnamed_outputs = executor._execute_func(
            'n1', mock_mul, {'param1': 7, 'param2': 2}
        )

        self.assertEqual(unnamed_outputs, 14)

    def test_execute_func_invalid_inputs(self) -> None:
        executor = SequentialExecutor('e1')

        with self.assertRaisesRegex(
            ExecutionError, 
            r'node_func not executed: node_id == n1'
        ):
            _ = executor._execute_func(
                'n1', mock_mul, {'param1': 7, 'param3': 2}
            )

    def test_create_func_outputs_valid_single_output(self) -> None:
        executor = SequentialExecutor('e1')
        func_outputs = executor._create_func_outputs(['mul'], 14)

        self.assertDictEqual(func_outputs, {'mul': 14})

    def test_create_func_outputs_valid_multiple_output(self) -> None:
        executor = SequentialExecutor('e1')
        func_outputs = executor._create_func_outputs(
            ['mul1', 'mul2'], [7, 14]
        )

        self.assertDictEqual(func_outputs, {'mul1': 7, 'mul2': 14})

    def test_create_func_outputs_valid_empty_output(self) -> None:
        executor = SequentialExecutor('e1')
        func_outputs = executor._create_func_outputs([], None)

        self.assertDictEqual(func_outputs, {})

    def test_create_func_outputs_invalid_single_output(self) -> None:
        executor = SequentialExecutor('e1')

        with self.assertRaisesRegex(
            ExecutionError, 
            r'outputs not matched: node_outputs_qty == 2 and '
            r'unn_outputs_qty == 1'
        ):
            _ = executor._create_func_outputs(['mul1', 'mul2'], 7)

    def test_create_func_outputs_invalid_multiple_output(self) -> None:
        executor = SequentialExecutor('e1')

        with self.assertRaisesRegex(
            ExecutionError, 
            r'outputs not matched: node_outputs_qty == 2 and '
            r'unn_outputs_qty == 3'
        ):
            _ = executor._create_func_outputs(['mul1', 'mul2'], [7, 14, 21])

    def test_create_func_outputs_invalid_empty_output(self) -> None:
        executor = SequentialExecutor('e1')

        with self.assertRaisesRegex(
            ExecutionError, 
            r'outputs not matched: node_outputs_qty == 2 and '
            r'unn_outputs_qty == 1'
        ):
            _ = executor._create_func_outputs(['mul1', 'mul2'], None)
