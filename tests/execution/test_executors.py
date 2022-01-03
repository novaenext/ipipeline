from unittest import TestCase

from ipipeline.execution.executors import BaseExecutor, SequentialExecutor
from ipipeline.exceptions import ExecutionError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline


class MockBaseExecutor(BaseExecutor):
    def execute_pipeline(self) -> None:
        pass


class TestBaseExecutor(TestCase):
    def setUp(self) -> None:
        self._pipeline = Pipeline('p1', tags=['data'])
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

        self._catalog = Catalog('c1', tags=['data'])
        self._catalog.add_item('i1', 7)

    def test_init(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline, self._catalog)

        self.assertDictEqual(
            base_executor.pipeline.graph, {'n1': [], 'n2': []}
        )
        self.assertDictEqual(
            base_executor.catalog.items, {'i1': 7}
        )
        self.assertDictEqual(
            base_executor.signals, {}
        )

    def test_defaults(self) -> None:
        base_executor1 = MockBaseExecutor()
        base_executor2 = MockBaseExecutor()

        self.assertIsNot(base_executor1.pipeline, base_executor2.pipeline)
        self.assertIsNot(base_executor1.catalog, base_executor2.catalog)
        self.assertIsNot(base_executor1.signals, base_executor2.signals)

    def test_add_inexistent_pipeline(self) -> None:
        base_executor = MockBaseExecutor()
        base_executor.add_pipeline(self._pipeline)

        self.assertEqual(base_executor.pipeline.id, 'p1')
        self.assertEqual(base_executor.pipeline.tags, ['data'])

    def test_add_default_pipeline(self) -> None:
        base_executor = MockBaseExecutor()
        base_executor.add_pipeline(None)

        self.assertEqual(base_executor.pipeline.id, 'p0')
        self.assertEqual(base_executor.pipeline.tags, ['default'])

    def test_add_inexistent_catalog(self) -> None:
        base_executor = MockBaseExecutor()
        base_executor.add_catalog(self._catalog)

        self.assertEqual(base_executor.catalog.id, 'c1')
        self.assertEqual(base_executor.catalog.tags, ['data'])

    def test_add_default_catalog(self) -> None:
        base_executor = MockBaseExecutor()
        base_executor.add_catalog(None)

        self.assertEqual(base_executor.catalog.id, 'c0')
        self.assertEqual(base_executor.catalog.tags, ['default'])

    def test_add_inexistent_signals(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)
        base_executor.add_signal('s1', 'n1', 'skip', True)
        base_executor.add_signal('s2', 'n2', 'skip', True)

        self.assertListEqual(
            list(base_executor.signals.keys()), ['n1', 'n2']
        )
        self.assertListEqual(
            [signal.node_id for signal in base_executor.signals.values()], 
            ['n1', 'n2']
        )
        self.assertTrue(base_executor.signals['n1'].status)
        self.assertTrue(base_executor.signals['n2'].status)

    def test_add_existent_signals(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)
        base_executor.add_signal('s1', 'n1', 'skip', True)
        base_executor.add_signal('s2', 'n1', 'skip', False)

        self.assertListEqual(
            list(base_executor.signals.keys()), ['n1']
        )
        self.assertListEqual(
            [signal.node_id for signal in base_executor.signals.values()], 
            ['n1']
        )
        self.assertFalse(base_executor.signals['n1'].status)

    def test_add_inexistent_signals_with_inexistent_node_id(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)
        base_executor.add_signal('s1', 'n1', 'skip', True)

        with self.assertRaisesRegex(
            ExecutionError, 
            r'node_id not found in the _pipeline.nodes: node_id == n22'
        ):
            base_executor.add_signal('s2', 'n22', 'skips', True)

    def test_add_inexistent_signals_with_invalid_type(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)
        base_executor.add_signal('s1', 'n1', 'skip', True)

        with self.assertRaisesRegex(
            ExecutionError, r'type not found in the valid_types: type == skips'
        ):
            base_executor.add_signal('s2', 'n2', 'skips', True)

    def test_check_inexistent_node_id(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)

        with self.assertRaisesRegex(
            ExecutionError, 
            r'node_id not found in the _pipeline.nodes: node_id == n11'
        ):
            base_executor._check_inexistent_node_id('n11')

    def test_check_existent_node_id(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)
        base_executor._check_inexistent_node_id('n1')

        self.assertTrue(True)

    def test_check_invalid_type(self) -> None:
        base_executor = MockBaseExecutor()

        with self.assertRaisesRegex(
            ExecutionError, r'type not found in the valid_types: type == skips'
        ):
            base_executor._check_invalid_type('skips')

    def test_check_valid_type(self) -> None:
        base_executor = MockBaseExecutor()
        base_executor._check_invalid_type('skip')

        self.assertTrue(True)

    def test_execute_existent_node(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)
        func_outputs = base_executor.execute_node('n1')

        self.assertDictEqual(func_outputs, {'sum': 10})

    def test_execute_inexistent_node(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)

        with self.assertRaisesRegex(
            ExecutionError, r'node not executed by the executor: id == n11'
        ):
            _ = base_executor.execute_node('n11')

    def test_obtain_topo_order(self) -> None:
        base_executor = MockBaseExecutor(self._pipeline)
        topo_order = base_executor.obtain_topo_order()

        self.assertListEqual(topo_order, [['n1', 'n2']])


class TestSequentialExecutor(TestCase):
    def setUp(self) -> None:
        self._pipeline = Pipeline('p1', tags=['data'])
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

        self._catalog = Catalog('c1', tags=['data'])

    def test_deriv(self) -> None:
        executor = SequentialExecutor()

        self.assertIsInstance(executor, BaseExecutor)

    def test_execute_pipeline_without_signal(self) -> None:
        executor = SequentialExecutor(self._pipeline, self._catalog)
        topo_order = executor.obtain_topo_order()
        executor.execute_pipeline(topo_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10, 'sub': 4})

    def test_execute_pipeline_with_signal(self) -> None:
        executor = SequentialExecutor(self._pipeline)
        executor.add_signal('s1', 'n2', 'skip', True)
        executor.add_signal('s2', 'n3', 'skip', False)
        executor.add_signal('s3', 'n4', 'skip', True)
        topo_order = executor.obtain_topo_order()
        executor.execute_pipeline(topo_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10})


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2


def mock_print(param1: int, param2: str = '->') -> None:
    print(param1, param2)
