from unittest import TestCase
from unittest.mock import Mock

from ipipeline.exceptions import PipelineError, InstanceError
from ipipeline.structure.pipeline import BasePipeline, Pipeline


class MockBasePipeline(BasePipeline):
    def add_node(self) -> None:
        pass

    def add_conn(self) -> None:
        pass


class TestBasePipeline(TestCase):
    def test_init_valid_args(self) -> None:
        base_pipeline = MockBasePipeline('p1', tags=['data'])

        self.assertEqual(base_pipeline.id, 'p1')
        self.assertDictEqual(base_pipeline._nodes, {})
        self.assertDictEqual(base_pipeline._conns, {})
        self.assertDictEqual(base_pipeline._graph, {})
        self.assertListEqual(base_pipeline.tags, ['data'])

    def test_init_invalid_args(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == p1,'
        ):
            _ = MockBasePipeline('p1,')

    def test_repr(self) -> None:
        base_pipeline = MockBasePipeline('p1')
        instance_repr = base_pipeline.__repr__()

        self.assertEqual(
            instance_repr, 'MockBasePipeline(id_=\'p1\', tags=[])'
        )


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self._mock_nodes = {}
        self._mock_graph = {}

        for node_id in ['n1', 'n2', 'n3', 'n4']:
            self._mock_nodes[node_id] = Mock(
                spec=['id', 'func', 'inputs', 'outputs', 'props', 'tags']
            )
            self._mock_graph[node_id] = []

        self._mock_node = self._mock_nodes['n1']
        self._mock_conn = Mock(
            spec=['id', 'src_id', 'dst_id', 'weight', 'tags']
        )

    def test_new_valid_args(self) -> None:
        pipeline = Pipeline('p1')
        
        self.assertIsInstance(pipeline, BasePipeline)

    def test_add_node_inexistent_ids(self) -> None:
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

    def test_add_node_existent_ids(self) -> None:
        pipeline = Pipeline('p1')
        pipeline.add_node(
            'n1', mock_sum, inputs={'param1': 7, 'param2': 3}, outputs=['sum']
        )

        with self.assertRaisesRegex(
            PipelineError, r'existent node_id found: node_id == n1'
        ):
            pipeline.add_node(
                'n1', 
                mock_sub, 
                inputs={'param1': 7, 'param2': 3}, 
                outputs=['sub']
            )

    def test_check_existent_node_id_existent(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = {'n1': self._mock_node}

        with self.assertRaisesRegex(
            PipelineError, r'existent node_id found: node_id == n1'
        ):
            pipeline._check_existent_node_id('n1')

    def test_check_existent_node_id_inexistent(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._check_existent_node_id('n1')

        self.assertTrue(True)

    def test_add_conn_inexistent_ids(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._mock_nodes
        pipeline._graph = self._mock_graph
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

    def test_add_conn_existent_ids(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._mock_nodes
        pipeline._graph = self._mock_graph
        pipeline.add_conn('c1', 'n1', 'n2')

        with self.assertRaisesRegex(
            PipelineError, r'existent conn_id found: conn_id == c1'
        ):
            pipeline.add_conn('c1', 'n1', 'n3')

    def test_add_conn_missing_src_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._mock_nodes
        pipeline._graph = self._mock_graph

        with self.assertRaisesRegex(
            PipelineError, 
            r'inexistent node_id found: conn_id == c1 and node_id == n7'
        ):
            pipeline.add_conn('c1', 'n7', 'n1')

    def test_add_conn_missing_dst_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = self._mock_nodes
        pipeline._graph = self._mock_graph

        with self.assertRaisesRegex(
            PipelineError, 
            r'inexistent node_id found: conn_id == c1 and node_id == n7'
        ):
            pipeline.add_conn('c1', 'n1', 'n7')

    def test_check_existent_conn_id_existent(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._conns = {'c1': self._mock_conn}

        with self.assertRaisesRegex(
            PipelineError, r'existent conn_id found: conn_id == c1'
        ):
            pipeline._check_existent_conn_id('c1')

    def test_check_existent_conn_id_inexistent(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._check_existent_conn_id('c1')

        self.assertTrue(True)

    def test_check_inexistent_node_id_inexistent(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._conns = {'c1': self._mock_conn}

        with self.assertRaisesRegex(
            PipelineError, 
            r'inexistent node_id found: conn_id == c1 and node_id == n1'
        ):
            pipeline._check_inexistent_node_id('c1', 'n1')

    def test_check_inexistent_node_id_existent(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._nodes = {'n1': self._mock_node}
        pipeline._conns = {'c1': self._mock_conn}
        pipeline._check_inexistent_node_id('c1', 'n1')

        self.assertTrue(True)
