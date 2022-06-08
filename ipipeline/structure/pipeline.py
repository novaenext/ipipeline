"""Class related to the pipeline procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.exceptions import PipelineError
from ipipeline.structure.info import Info
from ipipeline.structure.link import Link
from ipipeline.structure.node import Node
from ipipeline.utils.checking import check_none


class Pipeline(Info):
    """Stores a pipeline composed of nodes and links.

    The pipeline represents the graph that must be directed and acyclic in 
    order to obtain the topological order.

    Attributes
    ----------
    _id : str
        ID of the pipeline.
    _graph : Dict[str, list]
        Graph of the pipeline. The keys are the source node IDs and the 
        values are a list of destination node IDs.
    _nodes : Dict[str, Node]
        Nodes of the graph. The keys are the node IDs and the values are 
        the nodes.
    _links : Dict[str, Link]
        Links of the graph. The keys are the link IDs and the values are 
        the links.
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
            Graph of the pipeline. The keys are the source node IDs and the 
            values are a list of destination node IDs.
        nodes : Dict[str, Node], optional
            Nodes of the graph. The keys are the node IDs and the values are 
            the nodes.
        links : Dict[str, Link], optional
            Links of the graph. The keys are the link IDs and the values are 
            the links.
        tags : List[str], optional
            Tags of the pipeline to provide more context.

        Raises
        ------
        InfoError
            Informs that the id did not match the pattern.
        """

        super().__init__(id, tags=tags)

        self._graph = check_none(graph, {})
        self._nodes = check_none(nodes, {})
        self._links = check_none(links, {})

    @property
    def graph(self) -> Dict[str, list]:
        """Gets the _graph attribute.

        Returns
        -------
        graph : Dict[str, list]
            Graph of the pipeline. The keys are the source node IDs and the 
            values are a list of destination node IDs.
        """

        return self._graph

    @graph.setter
    def graph(self, graph: Dict[str, list]) -> None:
        """Sets the _graph attribute.

        Parameters
        ----------
        graph : Dict[str, list]
            Graph of the pipeline. The keys are the source node IDs and the 
            values are a list of destination node IDs.
        """

        self._graph = graph

    @property
    def nodes(self) -> Dict[str, Node]:
        """Gets the _nodes attribute.

        Returns
        -------
        nodes : Dict[str, Node]
            Nodes of the graph. The keys are the node IDs and the values are 
            the nodes.
        """

        return self._nodes

    @nodes.setter
    def nodes(self, nodes: Dict[str, Node]) -> None:
        """Sets the _nodes attribute.

        Parameters
        ----------
        nodes : Dict[str, Node]
            Nodes of the graph. The keys are the node IDs and the values are 
            the nodes.
        """

        self._nodes = nodes

    @property
    def links(self) -> Dict[str, Link]:
        """Gets the _links attribute.

        Returns
        -------
        links : Dict[str, Link]
            Links of the graph. The keys are the link IDs and the values are 
            the links.
        """

        return self._links

    @links.setter
    def links(self, links: Dict[str, Link]) -> None:
        """Sets the _links attribute.

        Parameters
        ----------
        links : Dict[str, Link]
            Links of the graph. The keys are the link IDs and the values are 
            the links.
        """

        self._links = links

    def check_node(self, id: str) -> bool:
        """Checks if a node exists.

        Parameters
        ----------
        id : str
            ID of the node.

        Returns
        -------
        checked : bool
            Flag that indicates if a node exists.
        """

        checked = id in self._nodes.keys()

        return checked

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
            Task of the node.
        inputs : Dict[str, Any], optional
            Inputs of the task. The keys are the callable parameters and the 
            values are the data required for the parameters. The values can 
            also be placeholders for the catalog items.

            Placeholders:
                'c.<item_id>': gets an item.
                'c.[<item_id>, ..., <item_id>]': gets a list of items.
        outputs : List[str], optional
            Outputs of the task. The outputs must match the returns in terms 
            of size.
        tags : List[str], optional
            Tags of the node to provide more context.

        Raises
        ------
        InfoError
            Informs that the id did not match the pattern.
        PipelineError
            Informs that the id was found in the _nodes.
        """

        node = Node(id, task, inputs=inputs, outputs=outputs, tags=tags)

        if self.check_node(node.id):
            raise PipelineError('id was found in the _nodes', [f'id == {id}'])

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

    def check_link(self, id: str) -> bool:
        """Checks if a link exists.

        Parameters
        ----------
        id : str
            ID of the link.

        Returns
        -------
        checked : bool
            Flag that indicates if a link exists.
        """

        checked = id in self._links.keys()

        return checked

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
