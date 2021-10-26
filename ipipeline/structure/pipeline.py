"""Classes related to the pipeline procedures."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from ipipeline.exception import PipelineError
from ipipeline.structure.conn import BaseConn, Conn
from ipipeline.structure.node import BaseNode, Node
from ipipeline.util.instance import Identification


class BasePipeline(ABC, Identification):
    """Provides an interface to the pipeline classes.

    Attributes
    ----------
    _id : str
        ID of the pipeline.
    _nodes : Dict[str, BaseNode]
        Nodes of the graph. The keys are the node IDs and the values are 
        the node objects where the IDs were obtained.
    _conns : Dict[str, BaseConn]
        Connections of the graph. The keys are the connection IDs and the 
        values are the connection objects where the IDs were obtained.
    _graph : Dict[str, list]
        Graph of the pipeline. The keys are the IDs of the source nodes 
        and the values are the dependencies formed by the IDs of the 
        destination nodes.
    _tags : List[str]
        Tags of the pipeline to provide more context.
    """

    def __init__(self, id: str, tags: List[str] = []) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the pipeline.
        tags : List[str], default=[]
            Tags of the pipeline to provide more context.

        Raises
        ------
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        self._nodes = {}
        self._conns = {}
        self._graph = {}

        super().__init__(id, tags=tags)

    @property
    def nodes(self) -> Dict[str, BaseNode]:
        """Obtains the _nodes attribute.

        Returns
        -------
        nodes : Dict[str, BaseNode]
            Nodes of the graph. The keys are the node IDs and the values are 
            the node objects where the IDs were obtained.
        """

        return self._nodes

    @property
    def conns(self) -> Dict[str, BaseConn]:
        """Obtains the _conns attribute.

        Returns
        -------
        conns : Dict[str, BaseConn]
            Connections of the graph. The keys are the connection IDs and the 
            values are the connection objects where the IDs were obtained.
        """

        return self._conns

    @property
    def graph(self) -> Dict[str, list]:
        """Obtains the _graph attribute.

        Returns
        -------
        graph : Dict[str, list]
            Graph of the pipeline. The keys are the IDs of the source nodes 
            and the values are the dependencies formed by the IDs of the 
            destination nodes.
        """

        return self._graph

    @abstractmethod
    def add_node(
        self, 
        id: str, 
        func: Callable, 
        inputs: Dict[str, Any] = {}, 
        outputs: List[str] = [], 
        tags: List[str] = []
    ) -> None:
        """Provides an interface to add a node in the graph.

        Parameters
        ----------
        id : str
            ID of the node.
        func : Callable
            Function that performs a specific action.
        inputs : Dict[str, Any], default={}
            Inputs of the function. The keys are the function parameters and 
            the values are anything entered directly and/or obtained from the 
            catalog in the form of 'c.<item_id>'.
        outputs : List[str], default=[]
            Outputs of the function. The outputs must match the returns in 
            terms of length. If one output is expected, the returns can be of 
            any type, however, in cases with more than one output, the returns 
            must be some type of sequence.
        tags : List[str], default=[]
            Tags of the node to provide more context.
        """

        pass

    @abstractmethod
    def add_conn(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        value: Any = None, 
        tags: List[str] = []
    ) -> None:
        """Provides an interface to add a connection in the graph.

        Parameters
        ----------
        id : str
            ID of the connection.
        src_id : str
            ID of the source element.
        dst_id : str
            ID of the destination element.
        value : Any, default=None
            Value of the connection that indicates its strength.
        tags : List[str], default=[]
            Tags of the connection to provide more context.
        """

        pass


class Pipeline(BasePipeline):
    """Stores a graph formed by a group of nodes and their connections.

    The connections between nodes must form a directed acyclic graph from 
    which the topological order can be obtained.

    Attributes
    ----------
    _id : str
        ID of the pipeline.
    _nodes : Dict[str, BaseNode]
        Nodes of the graph. The keys are the node IDs and the values are 
        the node objects where the IDs were obtained.
    _conns : Dict[str, BaseConn]
        Connections of the graph. The keys are the connection IDs and the 
        values are the connection objects where the IDs were obtained.
    _graph : Dict[str, list]
        Graph of the pipeline. The keys are the IDs of the source nodes 
        and the values are the dependencies formed by the IDs of the 
        destination nodes.
    _tags : List[str]
        Tags of the pipeline to provide more context.
    """

    def add_node(
        self, 
        id: str, 
        func: Callable, 
        inputs: Dict[str, Any] = {}, 
        outputs: List[str] = [], 
        tags: List[str] = []
    ) -> None:
        """Adds a node in the graph.

        Parameters
        ----------
        id : str
            ID of the node.
        func : Callable
            Function that performs a specific action.
        inputs : Dict[str, Any], default={}
            Inputs of the function. The keys are the function parameters and 
            the values are anything entered directly and/or obtained from the 
            catalog in the form of 'c.<item_id>'.
        outputs : List[str], default=[]
            Outputs of the function. The outputs must match the returns in 
            terms of length. If one output is expected, the returns can be of 
            any type, however, in cases with more than one output, the returns 
            must be some type of sequence.
        tags : List[str], default=[]
            Tags of the node to provide more context.

        Raises
        ------
        PipelineError
            Informs that the node_id was found in the _nodes.
        """

        self._check_existent_node_id(id)
        node = Node(id, func, inputs, outputs, tags)

        self._nodes[node.id] = node
        self._graph[node.id] = []

    def _check_existent_node_id(self, node_id: str) -> None:
        """Checks if the node ID exists.

        Parameters
        ----------
        node_id : str
            ID of the node.

        Raises
        ------
        PipelineError
            Informs that the node_id was found in the _nodes.
        """

        if node_id in self._nodes:
            raise PipelineError(
                'node_id found in the _nodes', f'node_id == {node_id}'
            )

    def add_conn(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        value: Any = None, 
        tags: List[str] = []
    ) -> None:
        """Adds a connection in the graph.

        Parameters
        ----------
        id : str
            ID of the connection.
        src_id : str
            ID of the source element.
        dst_id : str
            ID of the destination element.
        value : Any, default=None
            Value of the connection that indicates its strength.
        tags : List[str], default=[]
            Tags of the connection to provide more context.

        Raises
        ------
        PipelineError
            Informs that the conn_id was found in the _conns.
        PipelineError
            Informs that the node_id was not found in the _nodes.
        """

        self._check_existent_conn_id(id)
        self._check_inexistent_node_id(id, src_id)
        self._check_inexistent_node_id(id, dst_id)
        conn = Conn(id, src_id, dst_id, value, tags)

        self._conns[conn.id] = conn
        self._graph[conn.src_id].append(conn.dst_id)

    def _check_existent_conn_id(self, conn_id: str) -> None:
        """Checks if the connection ID exists.

        Parameters
        ----------
        conn_id : str
            ID of the connection.

        Raises
        ------
        PipelineError
            Informs that the conn_id was found in the _conns.
        """

        if conn_id in self._conns:
            raise PipelineError(
                'conn_id found in the _conns', f'conn_id == {conn_id}'
            )

    def _check_inexistent_node_id(self, conn_id: str, node_id: str) -> None:
        """Checks if the node ID does not exist.

        Parameters
        ----------
        conn_id : str
            ID of the connection.
        node_id : str
            ID of the node.

        Raises
        ------
        PipelineError
            Informs that the node_id was not found in the _nodes.
        """

        if node_id not in self._nodes:
            raise PipelineError(
                'node_id not found in the _nodes',
                f'conn_id == {conn_id} and node_id == {node_id}'
            )
