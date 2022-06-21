from unittest import TestCase

from ipipeline.control.executors import BaseExecutor, SequentialExecutor
from ipipeline.exceptions import ExecutorError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline


class MockBaseExecutor(BaseExecutor):
    def execute_pipeline(self) -> None:
        pass


class TestBaseExecutor(TestCase):
    def setUp(self) -> None:
        self._pipeline = Pipeline(
            'p1', nodes=None, links=None, tags=['t1']
        )
        self._pipeline.add_node(
            'n1', 
            mock_sum, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sum'], 
            tags=None
        )
        self._pipeline.add_node(
            'n2', 
            mock_sub, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sub'], 
            tags=None
        )

        self._catalog = Catalog('c1', items=None, tags=['t1'])
        self._catalog.set_item('i1', 7)

    def test_init(self) -> None:
        executor = MockBaseExecutor(
            pipeline=self._pipeline, catalog=self._catalog
        )

        self.assertDictEqual(executor.catalog.items, {'i1': 7})

    def test_defaults(self) -> None:
        executor1 = MockBaseExecutor()
        executor2 = MockBaseExecutor()

        self.assertIsNot(executor1.pipeline, executor2.pipeline)
        self.assertIsNot(executor1.catalog, executor2.catalog)

    def test_add_inexistent_pipeline(self) -> None:
        executor = MockBaseExecutor(pipeline=None, catalog=None)
        executor.add_pipeline(self._pipeline)

        self.assertEqual(executor.pipeline.id, 'p1')
        self.assertEqual(executor.pipeline.tags, ['t1'])

    def test_add_default_pipeline(self) -> None:
        executor = MockBaseExecutor(pipeline=None, catalog=None)
        executor.add_pipeline(None)

        self.assertEqual(executor.pipeline.id, 'p0')
        self.assertEqual(executor.pipeline.tags, ['default'])

    def test_add_inexistent_catalog(self) -> None:
        executor = MockBaseExecutor(pipeline=None, catalog=None)
        executor.add_catalog(self._catalog)

        self.assertEqual(executor.catalog.id, 'c1')
        self.assertEqual(executor.catalog.tags, ['t1'])

    def test_add_default_catalog(self) -> None:
        executor = MockBaseExecutor(pipeline=None, catalog=None)
        executor.add_catalog(None)

        self.assertEqual(executor.catalog.id, 'c0')
        self.assertEqual(executor.catalog.tags, ['default'])

    def test_execute_existent_node(self) -> None:
        executor = MockBaseExecutor(
            pipeline=self._pipeline, catalog=None
        )
        func_outputs = executor.execute_node('n1')

        self.assertDictEqual(func_outputs, {'sum': 10})

    def test_execute_inexistent_node(self) -> None:
        executor = MockBaseExecutor(
            pipeline=self._pipeline, catalog=None
        )

        with self.assertRaisesRegex(
            ExecutorError, r'node not executed by the executor: id == n11'
        ):
            _ = executor.execute_node('n11')

    def test_obtain_topo_order(self) -> None:
        executor = MockBaseExecutor(
            pipeline=self._pipeline, catalog=None
        )
        topo_order = executor.obtain_topo_order()

        self.assertListEqual(topo_order, [['n1', 'n2']])


class TestSequentialExecutor(TestCase):
    def setUp(self) -> None:
        self._pipeline = Pipeline(
            'p1', nodes=None, links=None, tags=None
        )
        self._pipeline.add_node(
            'n1', 
            mock_sum, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sum'], 
            tags=['t1']
        )
        self._pipeline.add_node(
            'n2', 
            mock_sub, 
            inputs={'param1': 7, 'param2': 3}, 
            outputs=['sub'], 
            tags=['t2']
        )
        self._pipeline.add_node(
            'n3', 
            mock_print, 
            inputs={'param1': 'c.sum', 'param2': '<-'}, 
            outputs=None, 
            tags=['t3']
        )
        self._pipeline.add_node(
            'n4', 
            mock_print, 
            inputs={'param1': 'c.sub'}, 
            outputs=None, 
            tags=None
        )
        self._pipeline.add_link('l1', 'n1', 'n3', tags=None)
        self._pipeline.add_link('l2', 'n2', 'n4', tags=None)

    def test_deriv(self) -> None:
        executor = SequentialExecutor(
            pipeline=None, catalog=None
        )

        self.assertIsInstance(executor, BaseExecutor)

    def test_execute_pipeline(self) -> None:
        executor = SequentialExecutor(
            pipeline=self._pipeline, catalog=None
        )
        topo_order = executor.obtain_topo_order()
        executor.execute_pipeline(topo_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10, 'sub': 4})


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2


def mock_print(param1: int, param2: str = '->') -> None:
    print(param1, param2)