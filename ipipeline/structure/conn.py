"""Classes related to the connection procedures."""

from abc import ABC
from typing import Any, List

from ipipeline.util.instance import Identification


class BaseConn(ABC, Identification):
    """Provides an interface to the connection classes.

    Attributes
    ----------
    _id : str
        ID of the connection.
    _src_id : str
        ID of the source element.
    _dst_id : str
        ID of the destination element.
    _value : Any
        Value of the connection that indicates its strength.
    _tags : List[str]
        Tags of the connection to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        value: Any = None, 
        tags: List[str] = []
    ) -> None:
        """Initializes the attributes.

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
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        self._src_id = src_id
        self._dst_id = dst_id
        self._value = value

        super().__init__(id, tags=tags)

    @property
    def src_id(self) -> str:
        """Obtains the _src_id attribute.

        Returns
        -------
        src_id : str
            ID of the source element.
        """

        return self._src_id

    @property
    def dst_id(self) -> str:
        """Obtains the _dst_id attribute.

        Returns
        -------
        dst_id : str
            ID of the destination element.
        """

        return self._dst_id

    @property
    def value(self) -> Any:
        """Obtains the _value attribute.

        Returns
        -------
        value : Any
            Value of the connection that indicates its strength.
        """

        return self._value


class Conn(BaseConn):
    """Stores a reference between two elements.

    Attributes
    ----------
    _id : str
        ID of the connection.
    _src_id : str
        ID of the source element.
    _dst_id : str
        ID of the destination element.
    _value : Any
        Value of the connection that indicates its strength.
    _tags : List[str]
        Tags of the connection to provide more context.
    """

    pass
