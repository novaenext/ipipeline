from unittest import TestCase

from ipipeline.exception import PipelineError
from ipipeline.structure.pipeline import Pipeline


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self._graph = {'n1': [], 'n2': [], 'n3': [], 'n4': []}
        self._nodes = {'n1': None, 'n2': None, 'n3': None, 'n4': None}
        self._conns = {'c1': None, 'c2': None, 'c3': None}

    def test_init(self) -> None:
        pipeline = Pipeline('p1', tags=['data'])

        self.assertEqual(pipeline.id, 'p1')
        self.assertDictEqual(pipeline.graph, {})
        self.assertDictEqual(pipeline.nodes, {})
        self.assertDictEqual(pipeline.conns, {})
        self.assertListEqual(pipeline.tags, ['data'])

    def test_defaults(self) -> None:
        pipeline1 = Pipeline('p1', tags=['data'])
        pipeline2 = Pipeline('p2', tags=['data'])

        self.assertIsNot(pipeline1.graph, pipeline2.graph)
        self.assertIsNot(pipeline1.nodes, pipeline2.nodes)
        self.assertIsNot(pipeline1.conns, pipeline2.conns)

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
        pipeline = Pipeline('p1', nodes={'n1': None})

        with self.assertRaisesRegex(
            PipelineError, r'node_id found in the _nodes: node_id == n1'
        ):
            pipeline._check_existent_node_id('n1')

    def test_check_inexistent_node_id(self) -> None:
        pipeline = Pipeline('p1')
        pipeline._check_existent_node_id('n1')

        self.assertTrue(True)

    def test_add_inexistent_conns(self) -> None:
        pipeline = Pipeline('p1', graph=self._graph, nodes=self._nodes)
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
        pipeline = Pipeline('p1', graph=self._graph, nodes=self._nodes)
        pipeline.add_conn('c1', 'n1', 'n2')
        pipeline.add_conn('c2', 'n1', 'n3')

        with self.assertRaisesRegex(
            PipelineError, r'conn_id found in the _conns: conn_id == c1'
        ):
            pipeline.add_conn('c1', 'n2', 'n4')

    def test_add_inexistent_conns_with_inexistent_src_node(self) -> None:
        pipeline = Pipeline('p1', graph=self._graph, nodes=self._nodes)
        pipeline.add_conn('c1', 'n1', 'n2')
        pipeline.add_conn('c2', 'n1', 'n3')

        with self.assertRaisesRegex(
            PipelineError, 
            r'node_id not found in the _nodes: conn_id == c3 and node_id == n7'
        ):
            pipeline.add_conn('c3', 'n7', 'n4')

    def test_add_inexistent_conns_with_inexistent_dst_node(self) -> None:
        pipeline = Pipeline('p1', graph=self._graph, nodes=self._nodes)
        pipeline.add_conn('c1', 'n1', 'n2')
        pipeline.add_conn('c2', 'n1', 'n3')

        with self.assertRaisesRegex(
            PipelineError, 
            r'node_id not found in the _nodes: conn_id == c3 and node_id == n7'
        ):
            pipeline.add_conn('c3', 'n2', 'n7')

    def test_check_existent_conn_id(self) -> None:
        pipeline = Pipeline('p1', conns=self._conns)

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

        with self.assertRaisesRegex(
            PipelineError, 
            r'node_id not found in the _nodes: conn_id == c1 and node_id == n1'
        ):
            pipeline._check_inexistent_node_id('c1', 'n1')

    def test_check_existent_node_id_with_conn_id(self) -> None:
        pipeline = Pipeline('p1', nodes=self._nodes)
        pipeline._check_inexistent_node_id('c1', 'n1')

        self.assertTrue(True)


def mock_sum(param1: int, param2: int) -> int:
    return param1 + param2


def mock_sub(param1: int, param2: int) -> int:
    return param1 - param2
