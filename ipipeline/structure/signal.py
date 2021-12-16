"""Class related to the signal procedures."""

from typing import List

from ipipeline.structure.info import Info


class Signal(Info):
    """Stores the instructions of a node.

    The instructions signal that a certain action must be triggered.

    Attributes
    ----------
    _id : str
        ID of the signal.
    _node_id : str
        ID of the node.
    _type : str
        Type of the signal used to trigger an action.
    _status : bool
        Indicates if the signal is enable or disable.
    _tags : List[str]
        Tags of the signal to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        node_id: str, 
        type: str, 
        status: bool = True, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the signal.
        node_id : str
            ID of the node.
        type : str
            Type of the signal used to trigger an action.
        status : bool, default=True
            Indicates if the signal is enable or disable.
        tags : List[str], default=None
            Tags of the signal to provide more context.

        Raises
        ------
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._node_id = node_id
        self._type = type
        self._status = status

        super().__init__(id, tags=tags)

    @property
    def node_id(self) -> str:
        """Obtains the _node_id attribute.

        Returns
        -------
        node_id : str
            ID of the node.
        """

        return self._node_id

    @property
    def type(self) -> str:
        """Obtains the _type attribute.

        Returns
        -------
        type : str
            Type of the signal used to trigger an action.
        """

        return self._type

    @property
    def status(self) -> bool:
        """Obtains the _status attribute.

        Returns
        -------
        status : bool
            Indicates if the signal is enable or disable.
        """

        return self._status
