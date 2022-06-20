"""Class related to the link procedures."""

from typing import List

from ipipeline.structure.info import Info


class Link(Info):
    """Stores a dependency between the nodes of the graph.

    Attributes
    ----------
    _id : str
        ID of the link.
    _src_id : str
        ID of the source node.
    _dst_id : str
        ID of the destination node.
    _tags : List[str]
        Tags of the link to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

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
        """

        super().__init__(id, tags=tags)

        self._src_id = src_id
        self._dst_id = dst_id

    @property
    def src_id(self) -> str:
        """Gets the _src_id attribute.

        Returns
        -------
        src_id : str
            ID of the source node.
        """

        return self._src_id

    @src_id.setter
    def src_id(self, src_id: str) -> None:
        """Sets the _src_id attribute.

        Parameters
        ----------
        src_id : str
            ID of the source node.
        """

        self._src_id = src_id

    @property
    def dst_id(self) -> str:
        """Gets the _dst_id attribute.

        Returns
        -------
        dst_id : str
            ID of the destination node.
        """

        return self._dst_id

    @dst_id.setter
    def dst_id(self, dst_id: str) -> None:
        """Sets the _dst_id attribute.

        Parameters
        ----------
        dst_id : str
            ID of the destination node.
        """

        self._dst_id = dst_id
