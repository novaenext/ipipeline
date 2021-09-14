from unittest import TestCase
from unittest.mock import Mock

from ipipeline.control.execution import BaseExecutor, SequentialExecutor
from ipipeline.exceptions import ExecutionError


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2


def mock_print(param3: int) -> None:
    print(param3)


class TestSequentialExecutor(TestCase):
    def setUp(self) -> None:
        mock_nodes = {}

        for id_, func, inputs, outputs, tags in [
            ['n1', mock_sum, {'param1': 7, 'param2': 3}, ['sum'], ['sum']],
            ['n2', mock_sub, {'param1': 7, 'param2': 3}, ['sub'], ['sub']],
            ['n3', mock_print, {'param3': 'c.sum'}, [], ['print']], 
            ['n4', mock_print, {'param3': 'c.sub'}, [], ['print']]
        ]:
            mock_nodes[id_] = Mock(
                spec=['id', 'func', 'inputs', 'outputs', 'tags']
            )
            mock_nodes[id_].id = id_
            mock_nodes[id_].func = func
            mock_nodes[id_].inputs = inputs
            mock_nodes[id_].outputs = outputs
            mock_nodes[id_].tags = tags

        self._mock_pipeline = Mock(
            spec=['id', 'nodes', 'conns', 'graph', 'tags']
        )
        self._mock_pipeline.id = 'p1'
        self._mock_pipeline.nodes = mock_nodes
        self._mock_pipeline.graph = {
            'n1': ['n3'], 'n2': ['n4'], 'n3': [], 'n4': []
        }
        self._exe_order = ['n1', 'n2', 'n4', 'n3']

    def test_new(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)

        self.assertIsInstance(executor, BaseExecutor)

    def test_flag_node_inexistent_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        executor.flag_node('n1', 'skip', True)

        self.assertDictEqual(executor._flagged, {'n1': {'skip': True}})

    def test_flag_node_existent_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        executor._flagged = {'n1': {'skip': True}}
        executor.flag_node('n1', 'skip', False)

        self.assertDictEqual(executor._flagged, {'n1': {'skip': False}})

    def test_flag_node_invalid_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)

        with self.assertRaisesRegex(
            ExecutionError, r'node not flagged: node_id == n1'
        ):
            executor.flag_node('n1', 'flag', True)

    def test_flag_node_inexistent_node_id(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)

        with self.assertRaisesRegex(
            ExecutionError, r'node not flagged: node_id == n11'
        ):
            executor.flag_node('n11', 'skip', True)

    def test_check_invalid_flag_invalid_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)

        with self.assertRaisesRegex(
            ExecutionError, 
            r'flag not found in the valid_flags: flag == flag'
        ):
            executor._check_invalid_flag('flag')

    def test_check_invalid_flag_valid_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        executor._check_invalid_flag('skip')

        self.assertTrue(True)

    def test_execute_node_existent_node_id(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        outputs = executor.execute_node('n1')

        self.assertDictEqual(outputs, {'sum': 10})

    def test_execute_node_inexistent_node_id(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)

        with self.assertRaisesRegex(
            ExecutionError, r'node not executed: node_id == n11'
        ):
            _ = executor.execute_node('n11')

    def test_obtain_exe_order(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        exe_order = executor.obtain_exe_order()

        self.assertListEqual(exe_order, ['n1', 'n2', 'n3', 'n4'])

    def test_execute_pipeline_without_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        executor.execute_pipeline(self._exe_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10, 'sub': 4})

    def test_execute_pipeline_with_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        executor._flagged = {
            'n2': {'skip': True}, 'n3': {'skip': False}, 'n4': {'skip': True}
        }
        executor.execute_pipeline(self._exe_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10})
