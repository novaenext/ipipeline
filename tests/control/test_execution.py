from unittest import TestCase

from ipipeline.control.execution import (
    BaseExecutor, SequentialExecutor, obtain_executor_class
)
from ipipeline.exception import ExecutionError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline


class MockBaseExecutor(BaseExecutor):
    def execute_pipeline(self) -> None:
        pass


class TestBaseExecutor(TestCase):
    def setUp(self) -> None:
        self._pipeline = Pipeline('p1')
        self._pipeline.add_node(
            'n1', 
            mock_sum, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sum'], 
            tags = ['math']
        )
        self._catalog = Catalog()
        self._catalog.add_item('i1', 7)

    def test_init(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)

        self.assertDictEqual(base_executor.pipeline.graph, {'n1': []})
        self.assertDictEqual(base_executor.catalog.items, {})

    def test_check_inexistent_catalog(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, None)
        catalog = base_executor._check_inexistent_catalog(None)

        self.assertDictEqual(catalog.items, {})

    def test_check_existent_catalog(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)
        catalog = base_executor._check_inexistent_catalog(self._catalog)

        self.assertDictEqual(catalog.items, {'i1': 7})

    def test_flag_inexistent_node(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)
        base_executor.flag_node('n1', 'skip', True)

        self.assertDictEqual(base_executor._flags, {'n1': {'skip': True}})

    def test_flag_existent_node(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)
        base_executor._flags = {'n1': {'skip': True}}
        base_executor.flag_node('n1', 'skip', False)

        self.assertDictEqual(base_executor._flags, {'n1': {'skip': False}})

    def test_flag_invalid_flag(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)

        with self.assertRaisesRegex(
            ExecutionError, r'node not flagged in the _flags: node_id == n1'
        ):
            base_executor.flag_node('n1', 'flag', True)

    def test_flag_invalid_node(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)

        with self.assertRaisesRegex(
            ExecutionError, r'node not flagged in the _flags: node_id == n11'
        ):
            base_executor.flag_node('n11', 'skip', True)

    def test_check_invalid_flag(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)

        with self.assertRaisesRegex(
            ExecutionError, r'flag not found in the valid_flags: flag == flag'
        ):
            base_executor._check_invalid_flag('flag')

    def test_check_valid_flag(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)
        base_executor._check_invalid_flag('skip')

        self.assertTrue(True)

    def test_execute_existent_node(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)
        outputs = base_executor.execute_node('n1')

        self.assertDictEqual(outputs, {'sum': 10})

    def test_execute_inexistent_node(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)

        with self.assertRaisesRegex(
            ExecutionError, 
            r'node not executed by the executor: node_id == n11'
        ):
            _ = base_executor.execute_node('n11')

    def test_obtain_topo_order(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)
        topo_order = base_executor.obtain_topo_order()

        self.assertListEqual(topo_order, [['n1']])


class TestSequentialExecutor(TestCase):
    def setUp(self) -> None:
        self._pipeline = Pipeline('p1')
        self._pipeline.add_node(
            'n1', 
            mock_sum, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sum'], 
            tags = ['math']
        )
        self._pipeline.add_node(
            'n2', 
            mock_sub, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sub'], 
            tags = ['math']
        )
        self._pipeline.add_node(
            'n3', 
            mock_print, 
            inputs={'param1': 'c.sum', 'param2': '<-'}, 
            tags = ['view']
        )
        self._pipeline.add_node(
            'n4', 
            mock_print, 
            inputs={'param1': 'c.sub'}
        )
        self._pipeline.add_conn('c1', 'n1', 'n3')
        self._pipeline.add_conn('c2', 'n2', 'n4')

        self._topo_order = [['n1', 'n2'], ['n3', 'n4']]

    def test_deriv(self) -> None:
        executor = SequentialExecutor(self._pipeline)

        self.assertIsInstance(executor, BaseExecutor)

    def test_execute_pipeline_without_flag(self) -> None:
        executor = SequentialExecutor(self._pipeline)
        executor.execute_pipeline(self._topo_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10, 'sub': 4})

    def test_execute_pipeline_with_flag(self) -> None:
        executor = SequentialExecutor(self._pipeline)
        executor._flags = {
            'n2': {'skip': True}, 'n3': {'skip': False}, 'n4': {'skip': True}
        }
        executor.execute_pipeline(self._topo_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10})


class TestObtainExecutorClass(TestCase):
    def test_valid_type(self) -> None:
        executor_class = obtain_executor_class('sequential')

        self.assertEqual(executor_class.__name__, 'SequentialExecutor')

    def test_invalid_type(self) -> None:
        with self.assertRaisesRegex(
            ExecutionError, 
            r'type not found in the executors: type == sequentials'
        ):
            _ = obtain_executor_class('sequentials')


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2


def mock_print(param1: int, param2: str = '->') -> None:
    print(param1, param2)
