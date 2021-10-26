from unittest import TestCase
from unittest.mock import Mock

from ipipeline.control.execution import BaseExecutor, SequentialExecutor
from ipipeline.exception import ExecutionError


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2


def mock_print(param3: int, param4: str = '->') -> None:
    print(param3, param4)


class MockBaseExecutor(BaseExecutor):
    def execute_pipeline(self) -> None:
        pass


class TestBaseExecutor(TestCase):
    def setUp(self) -> None:
        self._mock_node = Mock(
            spec=['id', 'func', 'inputs', 'outputs', 'tags']
        )
        self._mock_node.id = 'n1'
        self._mock_node.func = mock_sum
        self._mock_node.inputs = {'param1': 7, 'param2': 3}
        self._mock_node.outputs = ['sum']
        self._mock_node.tags = ['math']

        self._mock_pipeline = Mock(
            spec=['id', 'nodes', 'conns', 'graph', 'tags']
        )
        self._mock_pipeline.nodes = {'n1': self._mock_node}
        self._mock_pipeline.graph = {'n1': []}

        self._mock_catalog = Mock(spec=['items'])
        self._mock_catalog.items = {'i1': 7}

    def test_init(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )

        self.assertDictEqual(base_executor.pipeline.graph, {'n1': []})
        self.assertDictEqual(base_executor.catalog.items, {'i1': 7})

    def test_check_inexistent_catalog(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, None
        )
        catalog = base_executor._check_inexistent_catalog(None)

        self.assertDictEqual(catalog.items, {})

    def test_check_existent_catalog(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )
        catalog = base_executor._check_inexistent_catalog(self._mock_catalog)

        self.assertDictEqual(catalog.items, {'i1': 7})

    def test_flag_inexistent_node(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )
        base_executor.flag_node('n1', 'skip', True)

        self.assertDictEqual(base_executor._flags, {'n1': {'skip': True}})

    def test_flag_existent_node(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )
        base_executor._flags = {'n1': {'skip': True}}
        base_executor.flag_node('n1', 'skip', False)

        self.assertDictEqual(base_executor._flags, {'n1': {'skip': False}})

    def test_flag_invalid_flag(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )

        with self.assertRaisesRegex(
            ExecutionError, r'node not flagged in the _flags: node_id == n1'
        ):
            base_executor.flag_node('n1', 'flag', True)

    def test_flag_invalid_node(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )

        with self.assertRaisesRegex(
            ExecutionError, r'node not flagged in the _flags: node_id == n11'
        ):
            base_executor.flag_node('n11', 'skip', True)

    def test_check_invalid_flag(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )

        with self.assertRaisesRegex(
            ExecutionError, r'flag not found in the valid_flags: flag == flag'
        ):
            base_executor._check_invalid_flag('flag')

    def test_check_valid_flag(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )
        base_executor._check_invalid_flag('skip')

        self.assertTrue(True)

    def test_execute_existent_node(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )
        outputs = base_executor.execute_node('n1')

        self.assertDictEqual(outputs, {'sum': 10})

    def test_execute_inexistent_node(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )

        with self.assertRaisesRegex(
            ExecutionError, 
            r'node not executed by the executor: node_id == n11'
        ):
            _ = base_executor.execute_node('n11')

    def test_obtain_topo_order(self) -> None:
        base_executor = MockBaseExecutor(
            self._mock_pipeline, self._mock_catalog
        )
        topo_order = base_executor.obtain_topo_order()

        self.assertListEqual(topo_order, [['n1']])


class TestSequentialExecutor(TestCase):
    def setUp(self) -> None:
        mock_nodes = {}

        for id_, func, inputs, outputs, tags in [
            ['n1', mock_sum, {'param1': 7, 'param2': 3}, ['sum'], ['math']],
            ['n2', mock_sub, {'param1': 7, 'param2': 3}, ['sub'], ['math']],
            ['n3', mock_print, {'param3': 'c.sum', 'param4': '<-'}, [], []], 
            ['n4', mock_print, {'param3': 'c.sub'}, [], ['view']]
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
        self._mock_pipeline.nodes = mock_nodes
        self._mock_pipeline.graph = {
            'n1': ['n3'], 'n2': ['n4'], 'n3': [], 'n4': []
        }
        self._topo_order = [['n1', 'n2'], ['n3', 'n4']]

    def test_deriv(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)

        self.assertIsInstance(executor, BaseExecutor)

    def test_execute_pipeline_without_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        executor.execute_pipeline(self._topo_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10, 'sub': 4})

    def test_execute_pipeline_with_flag(self) -> None:
        executor = SequentialExecutor(self._mock_pipeline)
        executor._flags = {
            'n2': {'skip': True}, 'n3': {'skip': False}, 'n4': {'skip': True}
        }
        executor.execute_pipeline(self._topo_order)

        self.assertDictEqual(executor.catalog.items, {'sum': 10})
