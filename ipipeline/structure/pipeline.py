from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from ipipeline.exceptions import PipelineError
from ipipeline.structure.node import BaseNode, Node
from ipipeline.structure.conn import BaseConn, Conn
from ipipeline.utils.instance import InstanceIdentifier


class BasePipeline(ABC, InstanceIdentifier):
    def __init__(self, id_: str, tags: List[str] = []) -> None:
        self._nodes = {}
        self._conns = {}
        self._graph = {}

        super().__init__(id_, tags)

    @property
    def nodes(self) -> Dict[str, BaseNode]:
        return self._nodes

    @property
    def conns(self) -> Dict[str, BaseConn]:
        return self._conns

    @property
    def graph(self) -> Dict[str, list]:
        return self._graph

    @abstractmethod
    def add_node(
        self, 
        id_: str, 
        func: Callable, 
        inputs: Dict[str, Any] = {}, 
        outputs: List[str] = [], 
        tags: List[str] = []
    ) -> None:
        pass

    @abstractmethod
    def add_conn(
        self, 
        id_: str, 
        src_id: str, 
        dst_id: str, 
        value: Any = None, 
        tags: List[str] = []
    ) -> None:
        pass


class Pipeline(BasePipeline):
    def add_node(
        self, 
        id_: str, 
        func: Callable, 
        inputs: Dict[str, Any] = {}, 
        outputs: List[str] = [], 
        tags: List[str] = []
    ) -> None:
        self._check_existent_node_id(id_)
        node = Node(id_, func, inputs, outputs, tags)

        self._nodes[node.id] = node
        self._graph[node.id] = []

    def _check_existent_node_id(self, node_id: str) -> None:
        if node_id in self._nodes:
            raise PipelineError(
                'node_id found in the _nodes', f'node_id == {node_id}'
            )

    def add_conn(
        self, 
        id_: str, 
        src_id: str, 
        dst_id: str, 
        value: Any = None, 
        tags: List[str] = []
    ) -> None:
        self._check_existent_conn_id(id_)
        self._check_inexistent_node_id(id_, src_id)
        self._check_inexistent_node_id(id_, dst_id)
        conn = Conn(id_, src_id, dst_id, value, tags)

        self._conns[conn.id] = conn
        self._graph[conn.src_id].append(conn.dst_id)

    def _check_existent_conn_id(self, conn_id: str) -> None:
        if conn_id in self._conns:
            raise PipelineError(
                'conn_id found in the _conns', f'conn_id == {conn_id}'
            )

    def _check_inexistent_node_id(self, conn_id: str, node_id: str) -> None:
        if node_id not in self._nodes:
            raise PipelineError(
                'node_id not found in the _nodes',
                f'conn_id == {conn_id} and node_id == {node_id}'
            )
