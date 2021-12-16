"""Class related to the connection procedures."""

from typing import Any, List

from ipipeline.structure.info import Info


class Conn(Info):
    """Stores a reference between two nodes.

    The connection is used to define dependencies between nodes, therefore 
    the destination node is dependent on the source node.

    Attributes
    ----------
    _id : str
        ID of the connection.
    _src_id : str
        ID of the source node.
    _dst_id : str
        ID of the destination node.
    _power : Any
        Power of the connection that indicates its strength.
    _tags : List[str]
        Tags of the connection to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        power: Any = None, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the connection.
        src_id : str
            ID of the source node.
        dst_id : str
            ID of the destination node.
        power : Any
            Power of the connection that indicates its strength.
        tags : List[str]
            Tags of the connection to provide more context.

        Raises
        ------
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        self._src_id = src_id
        self._dst_id = dst_id
        self._power = power

        super().__init__(id, tags=tags)

    @property
    def src_id(self) -> str:
        """Obtains the _src_id attribute.

        Returns
        -------
        src_id : str
            ID of the source node.
        """

        return self._src_id

    @property
    def dst_id(self) -> str:
        """Obtains the _dst_id attribute.

        Returns
        -------
        dst_id : str
            ID of the destination node.
        """

        return self._dst_id

    @property
    def power(self) -> Any:
        """Obtains the _power attribute.

        Returns
        -------
        power : Any
            Power of the connection that indicates its strength.
        """

        return self._power
