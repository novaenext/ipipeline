from abc import ABC
from typing import List

from ipipeline.util.instance import Identification


class BaseSignal(ABC, Identification):
    """Provides an interface to the signal classes.

    Attributes
    ----------
    _id : str
        ID of the signal.
    _elem_id : str
        ID of the element.
    _type : str
        Type of the signal that triggers an action.
    _status : bool
        Indicates if the signal is enable or disable.
    _tags : List[str]
        Tags of the signal to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        elem_id: str, 
        type: str, 
        status: bool, 
        tags: List[str] = []
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the signal.
        elem_id : str
            ID of the element.
        type : str
            Type of the signal that triggers an action.
        status : bool
            Indicates if the signal is enable or disable.
        tags : List[str]
            Tags of the signal to provide more context.

        Raises
        ------
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        self._elem_id = elem_id
        self._type = type
        self._status = status

        super().__init__(id, tags=tags)

    @property
    def elem_id(self) -> str:
        """Obtains the _elem_id attribute.

        Returns
        -------
        elem_id : str
            ID of the element.
        """

        return self._elem_id

    @property
    def type(self) -> str:
        """Obtains the _type attribute.

        Returns
        -------
        type : str
            Type of the signal that triggers an action.
        """

        return self._type

    @property
    def status(self) -> bool:
        """Obtains the _status attribute.

        Returns
        -------
        status : bool
            Indicates if the signal is enable (True) or disable (False).
        """

        return self._status


class Signal(BaseSignal):
    """Stores instructions of an element.

    Attributes
    ----------
    _id : str
        ID of the signal.
    _elem_id : str
        ID of the element.
    _type : str
        Type of the signal that triggers an action.
    _status : bool
        Indicates if the signal is enable or disable.
    _tags : List[str]
        Tags of the signal to provide more context.
    """

    pass
