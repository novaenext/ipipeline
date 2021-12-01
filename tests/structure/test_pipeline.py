from unittest import TestCase

from ipipeline.exception import PipelineError
from ipipeline.structure.pipeline import (
    BasePipeline, Pipeline, obtain_pipeline
)


class MockBasePipeline(BasePipeline):
    def add_node(self) -> None:
        pass

    def add_conn(self) -> None:
        pass


class TestBasePipeline(TestCase):
    def test_init(self) -> None:
        base_pipeline = MockBasePipeline('p1', tags=['data'])

        self.assertEqual(base_pipeline.id, 'p1')
        self.assertDictEqual(base_pipeline.nodes, {})
        self.assertDictEqual(base_pipeline.conns, {})
        self.assertDictEqual(base_pipeline.graph, {})
        self.assertListEqual(base_pipeline.tags, ['data'])


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self._nodes = {'n1': None, 'n2': None, 'n3': None, 'n4': None}
        self._graph = {'n1': [], 'n2': [], 'n3': [], 'n4': []}

    def test_deriv(self) -> None:
        pipeline = Pipeline('p1')

        self.assertIsInstance(pipeline, BasePipeline)

    def test_add_inexistent_nodes(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.add_node(
            'n1', mock_sum, inputs={'param1': 7, 'param2': 3}, outputs=['sum']
        )
        pipeline.add_node(
            'n2', mock_sub, inputs={'param1': 7, 'param2': 3}, outputs=['sub']
        )

        self.assertListEqual(
            list(pipeline.nodes.keys()), ['n1', 'n2']
        )
        self.assertListEqual(
            [node.id for node in pipeline.nodes.values()], ['n1', 'n2']
        )
        self.assertListEqual(
            list(pipeline.graph.keys()), ['n1', 'n2']
        )
        self.assertListEqual(
            list(pipeline.graph.values()), [[], []]
        )

    def test_add_existent_nodes(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.add_node(
            'n1', mock_sum, inputs={'param1': 7, 'param2': 3}, outputs=['sum']
        )

        with self.assertRaisesRegex(
            PipelineError, r'node_id found in the _nodes: node_id == n1'
        ):
            pipeline.add_node(
                'n1', 
                mock_sub, 
                inputs={'param1': 7, 'param2': 3}, 
                outputs=['sub']
            )

    def test_check_existent_node_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = {'n1': None}

        with self.assertRaisesRegex(
            PipelineError, r'node_id found in the _nodes: node_id == n1'
        ):
            pipeline._check_existent_node_id('n1')

    def test_check_inexistent_node_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._check_existent_node_id('n1')

        self.assertTrue(True)

    def test_add_inexistent_conns(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._nodes
        pipeline._graph = self._graph
        pipeline.add_conn('c1', 'n1', 'n2')
        pipeline.add_conn('c2', 'n1', 'n3')
        pipeline.add_conn('c3', 'n2', 'n4')

        self.assertListEqual(
            list(pipeline.conns.keys()), ['c1', 'c2', 'c3']
        )
        self.assertListEqual(
            [conn.id for conn in pipeline.conns.values()], ['c1', 'c2', 'c3']
        )
        self.assertListEqual(
            list(pipeline.graph.keys()), ['n1', 'n2', 'n3', 'n4']
        )
        self.assertListEqual(
            list(pipeline.graph.values()), [['n2', 'n3'], ['n4'], [], []]
        )

    def test_add_existent_conns(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._nodes
        pipeline._graph = self._graph
        pipeline.add_conn('c1', 'n1', 'n2')
        pipeline.add_conn('c2', 'n1', 'n3')

        with self.assertRaisesRegex(
            PipelineError, r'conn_id found in the _conns: conn_id == c1'
        ):
            pipeline.add_conn('c1', 'n2', 'n4')

    def test_add_inexistent_src_node(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._nodes
        pipeline._graph = self._graph

        with self.assertRaisesRegex(
            PipelineError, 
            r'node_id not found in the _nodes: conn_id == c1 and node_id == n7'
        ):
            pipeline.add_conn('c1', 'n7', 'n2')

    def test_add_inexistent_dst_node(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._nodes
        pipeline._graph = self._graph

        with self.assertRaisesRegex(
            PipelineError, 
            r'node_id not found in the _nodes: conn_id == c1 and node_id == n9'
        ):
            pipeline.add_conn('c1', 'n1', 'n9')

    def test_check_existent_conn_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._conns = {'c1': None}

        with self.assertRaisesRegex(
            PipelineError, r'conn_id found in the _conns: conn_id == c1'
        ):
            pipeline._check_existent_conn_id('c1')

    def test_check_inexistent_conn_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._check_existent_conn_id('c1')

        self.assertTrue(True)

    def test_check_inexistent_node_id_with_conn_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._conns = {'c1': None}

        with self.assertRaisesRegex(
            PipelineError, 
            r'node_id not found in the _nodes: conn_id == c1 and node_id == n1'
        ):
            pipeline._check_inexistent_node_id('c1', 'n1')

    def test_check_existent_node_id_with_conn_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = {'n1': None}
        pipeline._conns = {'c1': None}
        pipeline._check_inexistent_node_id('c1', 'n1')

        self.assertTrue(True)


class TestObtainPipeline(TestCase):
    def test_valid_names(self) -> None:
        pipeline = obtain_pipeline(
            'tests.structure.test_pipeline', 'mock_build_pipeline'
        )

        self.assertEqual(pipeline.id, 'p1')

    def test_invalid_mod_name(self) -> None:
        with self.assertRaisesRegex(
            PipelineError, 
            r'func_name not found in the module: func_name == '
            r'mock_build_pipeline'
        ):
            _ = obtain_pipeline(
                'tests.structure.test_pipelines', 'mock_build_pipeline'
            )

    def test_invalid_func_name(self) -> None:
        with self.assertRaisesRegex(
            PipelineError, 
            r'func_name not found in the module: func_name == '
            r'mock_build_pipelines'
        ):
            _ = obtain_pipeline(
                'tests.structure.test_pipeline', 'mock_build_pipelines'
            )


def mock_build_pipeline() -> Pipeline:
    pipeline = Pipeline('p1')
    pipeline.add_node(
        'n1', 
        lambda param1, param2: param1 + param2, 
        inputs={'param1': 7, 'param2': 3}, 
        outputs=['sum'], 
        tags = ['math']
    )

    return pipeline


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2
