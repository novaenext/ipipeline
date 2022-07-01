from unittest import TestCase

from ipipeline.control.executors import BaseExecutor, SequentialExecutor
from ipipeline.exceptions import ExecutorError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline


class TestBaseExecutor(TestCase):
    def setUp(self) -> None:
        BaseExecutor.__abstractmethods__ = frozenset()

        self._pipeline = Pipeline('p1', tags=['t1'])
        self._pipeline.add_node(
            'n1', 
            lambda p1, p2: p1 + p2, 
            pos_inputs=['i1', 'i2'], 
            outputs=['i3'], 
            tags=['t1']
        )
        self._pipeline.add_node(
            'n2', 
            lambda p3=0: print(f'p3: {p3}'), 
            key_inputs={'p3': 'i3'}, 
            tags=['t2']
        )
        self._pipeline.add_node(
            'n3', 
            lambda: [][0], 
            tags=['t3']
        )
        self._pipeline.add_link('l1', 'n1', 'n2')
        self._pipeline.add_link('l2', 'n1', 'n3')

        self._catalog = Catalog('c1', tags=['t1'])
        self._catalog.set_item('i1', 2)
        self._catalog.set_item('i2', 4)

    def test_get_ordering__pipeline_wi_nodes_wi_links(self) -> None:
        executor = BaseExecutor()
        ordering = executor.get_ordering(self._pipeline)

        self.assertListEqual(ordering, [['n1'], ['n2', 'n3']])

    def test_get_ordering__pipeline_wo_nodes_wo_links(self) -> None:
        executor = BaseExecutor()
        ordering = executor.get_ordering(Pipeline('p1', tags=['t1']))

        self.assertListEqual(ordering, [])

    def test_execute_node__node_wi_exception(self) -> None:
        executor = BaseExecutor()

        with self.assertRaisesRegex(
            ExecutorError, r'node was not executed by the executor: id == n3'
        ):
            _ = executor.execute_node(self._pipeline, self._catalog, 'n3')

    def test_execute_node__node_wo_exception(self) -> None:
        executor = BaseExecutor()
        items = executor.execute_node(self._pipeline, self._catalog, 'n1')

        self.assertDictEqual(items, {'i3': 6})


class TestSequentialExecutor(TestCase):
    def setUp(self) -> None:
        self._pipeline = Pipeline('p1', tags=['t1'])
        self._pipeline.add_node(
            'n1', 
            lambda p1, p2: p1 + p2, 
            pos_inputs=['i1', 'i2'], 
            outputs=['i3'], 
            tags=['t1']
        )
        self._pipeline.add_node(
            'n2', 
            lambda p1, p2: [p1 - p2, 0], 
            pos_inputs=['i1', 'i2'], 
            outputs=['i4', 'i5'], 
            tags=['t2']
        )
        self._pipeline.add_node(
            'n3', 
            lambda p3=0: print(f'p3: {p3}'), 
            key_inputs={'p3': 'i3'}, 
            tags=['t3']
        )
        self._pipeline.add_node(
            'n4', 
            lambda p4=0: print(f'p4: {p4}'), 
            key_inputs={'p4': 'i4'}, 
            tags=['t4']
        )

        self._pipeline.add_link('l1', 'n1', 'n3')
        self._pipeline.add_link('l2', 'n2', 'n4')

        self._catalog = Catalog('c1', tags=['t1'])
        self._catalog.set_item('i1', 2)
        self._catalog.set_item('i2', 4)

        self._ordering = [['n1', 'n2'], ['n3', 'n4']]

    def test_execute_pipeline__pipeline_wi_nodes_wi_links(self) -> None:
        executor = SequentialExecutor()
        catalog = executor.execute_pipeline(
            self._pipeline, self._catalog, self._ordering
        )

        self.assertDictEqual(
            catalog.items, {'i1': 2, 'i2': 4, 'i3': 6, 'i4': -2, 'i5': 0}
        )

    def test_execute_pipeline__pipeline_wo_nodes_wo_links(self) -> None:
        executor = SequentialExecutor()
        catalog = executor.execute_pipeline(
            Pipeline('p1', tags=['t1']), Catalog('c1', tags=['t1']), []
        )

        self.assertDictEqual(catalog.items, {})
