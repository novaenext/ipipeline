"""Class related to the pipeline procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.exceptions import PipelineError
from ipipeline.structure.info import Info
from ipipeline.structure.link import Link
from ipipeline.structure.node import Node
from ipipeline.utils.checking import check_none


class Pipeline(Info):
    """Stores a graph formed by nodes and their links.

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
    _links : Dict[str, Link]
        Links of the graph. The keys are the link IDs and the values are 
        the link instances.
    _tags : List[str]
        Tags of the pipeline to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        graph: Dict[str, list] = None,
        nodes: Dict[str, Node] = None, 
        links: Dict[str, Link] = None, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the pipeline.
        graph : Dict[str, list], optional
            Graph of the pipeline. The keys are the IDs of the source nodes 
            and the values are the dependencies formed by the IDs of the 
            destination nodes.
        nodes : Dict[str, Node], optional
            Nodes of the graph. The keys are the node IDs and the values are 
            the node instances.
        links : Dict[str, Link], optional
            Links of the graph. The keys are the link IDs and the values are 
            the link instances.
        tags : List[str], optional
            Tags of the pipeline to provide more context.

        Raises
        ------
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        super().__init__(id, tags=tags)

        self._graph = check_none(graph, {})
        self._nodes = check_none(nodes, {})
        self._links = check_none(links, {})

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
    def links(self) -> Dict[str, Link]:
        """Obtains the _links attribute.

        Returns
        -------
        links : Dict[str, Link], optional
            Links of the graph. The keys are the link IDs and the values are 
            the link instances.
        """

        return self._links

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
        inputs : Dict[str, Any], optional
            Inputs of the task. The keys are the function parameters and 
            the values are any default values and/or placeholders for the 
            catalog items.

            'c.<item_id>': obtains a single item.
            'c.[<item_id>, ..., <item_id>]': obtains multiple items.
        outputs : List[str], optional
            Outputs of the task. The outputs must match the returns in 
            terms of length. If one output is expected, the return can be of 
            any type, however, in cases with more than one output, the returns 
            must be a sequence.
        tags : List[str], optional
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
                'node_id found in the _nodes', [f'node_id == {node_id}']
            )

    def add_link(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        tags: List[str] = None
    ) -> None:
        """Adds a link in the graph.

        Parameters
        ----------
        id : str
            ID of the link.
        src_id : str
            ID of the source node.
        dst_id : str
            ID of the destination node.
        tags : List[str], optional
            Tags of the link to provide more context.

        Raises
        ------
        PipelineError
            Informs that the link_id was found in the _link.
        PipelineError
            Informs that the node_id was not found in the _nodes.
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._check_existent_link_id(id)
        self._check_inexistent_node_id(src_id)
        self._check_inexistent_node_id(dst_id)
        link = Link(id, src_id, dst_id, tags=tags)

        self._graph[link.src_id].append(link.dst_id)
        self._links[link.id] = link

    def _check_existent_link_id(self, link_id: str) -> None:
        """Checks if the link ID exists.

        Parameters
        ----------
        link_id : str
            ID of the link.

        Raises
        ------
        PipelineError
            Informs that the link_id was found in the _links.
        """

        if link_id in self._links.keys():
            raise PipelineError(
                'link_id found in the _links', [f'link_id == {link_id}']
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
                'node_id not found in the _nodes', [f'node_id == {node_id}']
            )
