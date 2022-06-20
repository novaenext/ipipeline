"""Class related to the pipeline procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.exceptions import PipelineError
from ipipeline.structure.info import Info
from ipipeline.structure.link import Link
from ipipeline.structure.node import Node
from ipipeline.utils.checking import check_none


class Pipeline(Info):
    """Stores a flow of executable units.

    The link between the nodes must compose a directed acyclic graph.

    Attributes
    ----------
    _id : str
        ID of the pipeline.
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
        nodes: Dict[str, Node] = None, 
        links: Dict[str, Link] = None, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the pipeline.
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

        self._nodes = check_none(nodes, {})
        self._links = check_none(links, {})

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

    def get_node(self, id: str) -> Node:
        """Gets a node.

        Parameters
        ----------
        id : str
            ID of the node.

        Returns
        -------
        node : Node
            Node that stores an executable unit of the graph.

        Raises
        ------
        PipelineError
            Informs that the id was not found in the _nodes.
        """

        try:
            node = self._nodes[id]

            return node
        except KeyError as error:
            raise PipelineError(
                'id was not found in the _nodes', [f'id == {id}']
            ) from error

    def set_node(self, node: Node) -> None:
        """Sets a node.

        Parameters
        ----------
        node : Node
            Node that stores an executable unit of the graph.

        Raises
        ------
        PipelineError
            Informs that the id was found in the _nodes.
        """

        if self.check_node(node.id):
            raise PipelineError(
                'id was found in the _nodes', [f'id == {node.id}']
            )

        self._nodes[node.id] = node

    def delete_node(self, id: str) -> None:
        """Deletes a node.

        Parameters
        ----------
        id : str
            ID of the node.

        Raises
        ------
        PipelineError
            Informs that the id was not found in the _nodes.
        """

        try:
            del self._nodes[id]
        except KeyError as error:
            raise PipelineError(
                'id was not found in the _nodes', [f'id == {id}']
            ) from error

    def add_node(
        self, 
        id: str, 
        task: Callable, 
        inputs: Dict[str, Any] = None, 
        outputs: List[str] = None, 
        tags: List[str] = None
    ) -> None:
        """Adds a node through its settings.

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
        self.set_node(node)

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

    def get_link(self, id: str) -> Link:
        """Gets a link.

        Parameters
        ----------
        id : str
            ID of the link.

        Returns
        -------
        link : Link
            Link that stores a dependency between the nodes of the graph.

        Raises
        ------
        PipelineError
            Informs that the id was not found in the _links.
        """

        try:
            link = self._links[id]

            return link
        except KeyError as error:
            raise PipelineError(
                'id was not found in the _links', [f'id == {id}']
            ) from error

    def set_link(self, link: Link) -> None:
        """Sets a link.

        Parameters
        ----------
        link : Link
            Link that stores a dependency between the nodes of the graph.

        Raises
        ------
        PipelineError
            Informs that the id was found in the _links.
        """

        if self.check_link(link.id):
            raise PipelineError(
                'id was found in the _links', [f'id == {link.id}']
            )

        self._links[link.id] = link

    def delete_link(self, id: str) -> None:
        """Deletes a link.

        Parameters
        ----------
        id : str
            ID of the link.

        Raises
        ------
        PipelineError
            Informs that the id was not found in the _links.
        """

        try:
            del self._links[id]
        except KeyError as error:
            raise PipelineError(
                'id was not found in the _links', [f'id == {id}']
            ) from error

    def add_link(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        tags: List[str] = None
    ) -> None:
        """Adds a link through its settings.

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
        InfoError
            Informs that the id did not match the pattern.
        PipelineError
            Informs that the id was found in the _links.
        """

        link = Link(id, src_id, dst_id, tags=tags)
        self.set_link(link)
