"""Class related to the connection procedures."""

from typing import Any, List

from ipipeline.structure.info import Info


class Conn(Info):
    """Stores a relation between two nodes.

    The relation defines the dependency between the nodes, therefore the 
    destination node depends on the source node.

    Attributes
    ----------
    _id : str
        ID of the connection.
    _src_node_id : str
        ID of the source node.
    _dst_node_id : str
        ID of the destination node.
    _power : Any
        Power of the connection that indicates its strength.
    _tags : List[str]
        Tags of the connection to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        src_node_id: str, 
        dst_node_id: str, 
        power: Any = None, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

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
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._src_node_id = src_node_id
        self._dst_node_id = dst_node_id
        self._power = power

        super().__init__(id, tags=tags)

    @property
    def src_node_id(self) -> str:
        """Obtains the _src_node_id attribute.

        Returns
        -------
        src_node_id : str
            ID of the source node.
        """

        return self._src_node_id

    @property
    def dst_node_id(self) -> str:
        """Obtains the _dst_node_id attribute.

        Returns
        -------
        dst_node_id : str
            ID of the destination node.
        """

        return self._dst_node_id

    @property
    def power(self) -> Any:
        """Obtains the _power attribute.

        Returns
        -------
        power : Any
            Power of the connection that indicates its strength.
        """

        return self._power
