"""Class related to the pipeline procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.exceptions import PipelineError
from ipipeline.structure.conn import Conn
from ipipeline.structure.info import Info
from ipipeline.structure.node import Node
from ipipeline.utils.instance import check_none_arg


class Pipeline(Info):
    """Stores a graph formed by nodes and their connections.

    The graph must be acyclic to be able to obtain its topological order 
    that is used to order the execution of the nodes.

    Attributes
    ----------
    _id : str
        ID of the pipeline.
    _graph : Dict[str, list]
        Graph of the pipeline. The keys are the IDs of the source nodes 
        and the values are the dependencies formed by the IDs of the 
        destination nodes.
    _nodes : Dict[str, Node]
        Nodes of the graph. The keys are the node IDs and the values are 
        the node instances.
    _conns : Dict[str, Conn]
        Connections of the graph. The keys are the connection IDs and the 
        values are the connection instances.
    _tags : List[str]
        Tags of the pipeline to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        graph: Dict[str, list] = None,
        nodes: Dict[str, Node] = None, 
        conns: Dict[str, Conn] = None, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the pipeline.
        graph : Dict[str, list], default=None
            Graph of the pipeline. The keys are the IDs of the source nodes 
            and the values are the dependencies formed by the IDs of the 
            destination nodes.
        nodes : Dict[str, Node], default=None
            Nodes of the graph. The keys are the node IDs and the values are 
            the node instances.
        conns : Dict[str, Conn], default=None
            Connections of the graph. The keys are the connection IDs and the 
            values are the connection instances.
        tags : List[str], default=None
            Tags of the pipeline to provide more context.

        Raises
        ------
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._graph = check_none_arg(graph, {})
        self._nodes = check_none_arg(nodes, {})
        self._conns = check_none_arg(conns, {})

        super().__init__(id, tags=tags)

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

    @property
    def nodes(self) -> Dict[str, Node]:
        """Obtains the _nodes attribute.

        Returns
        -------
        nodes : Dict[str, Node]
            Nodes of the graph. The keys are the node IDs and the values are 
            the node instances.
        """

        return self._nodes

    @property
    def conns(self) -> Dict[str, Conn]:
        """Obtains the _conns attribute.

        Returns
        -------
        conns : Dict[str, Conn]
            Connections of the graph. The keys are the connection IDs and the 
            values are the connection instances.
        """

        return self._conns

    def add_node(
        self, 
        id: str, 
        task: Callable, 
        inputs: Dict[str, Any] = None, 
        outputs: List[str] = None, 
        tags: List[str] = None
    ) -> None:
        """Adds a node in the graph.

        Parameters
        ----------
        id : str
            ID of the node.
        task : Callable
            Task that represents an execution unit.
        inputs : Dict[str, Any], default=None
            Inputs of the task. The keys are the function parameters and 
            the values are any default values and/or placeholders for the 
            catalog items.

            'c.<item_id>': obtains a single item.
            'c.[<item_id>, ..., <item_id>]': obtains multiple items.
        outputs : List[str], default=None
            Outputs of the task. The outputs must match the returns in 
            terms of length. If one output is expected, the return can be of 
            any type, however, in cases with more than one output, the returns 
            must be a sequence.
        tags : List[str], default=None
            Tags of the node to provide more context.

        Raises
        ------
        PipelineError
            Informs that the node_id was found in the _nodes.
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._check_existent_node_id(id)
        node = Node(id, task, inputs=inputs, outputs=outputs, tags=tags)

        self._graph[node.id] = []
        self._nodes[node.id] = node

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

        if node_id in self._nodes.keys():
            raise PipelineError(
                'node_id found in the _nodes', f'node_id == {node_id}'
            )

    def add_conn(
        self, 
        id: str, 
        src_node_id: str, 
        dst_node_id: str, 
        power: Any = None, 
        tags: List[str] = None
    ) -> None:
        """Adds a connection in the graph.

        Parameters
        ----------
        id : str
            ID of the connection.
        src_node_id : str
            ID of the source node.
        dst_node_id : str
            ID of the destination node.
        power : Any
            Power of the connection that indicates its strength.
        tags : List[str]
            Tags of the connection to provide more context.

        Raises
        ------
        PipelineError
            Informs that the conn_id was found in the _conns.
        PipelineError
            Informs that the node_id was not found in the _nodes.
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._check_existent_conn_id(id)
        self._check_inexistent_node_id(src_node_id)
        self._check_inexistent_node_id(dst_node_id)
        conn = Conn(id, src_node_id, dst_node_id, power=power, tags=tags)

        self._graph[conn.src_node_id].append(conn.dst_node_id)
        self._conns[conn.id] = conn

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

        if conn_id in self._conns.keys():
            raise PipelineError(
                'conn_id found in the _conns', f'conn_id == {conn_id}'
            )

    def _check_inexistent_node_id(self, node_id: str) -> None:
        """Checks if the node ID does not exist.

        Parameters
        ----------
        node_id : str
            ID of the node.

        Raises
        ------
        PipelineError
            Informs that the node_id was not found in the _nodes.
        """

        if node_id not in self._nodes.keys():
            raise PipelineError(
                'node_id not found in the _nodes', f'node_id == {node_id}'
            )
