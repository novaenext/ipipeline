"""Class related to the information procedures."""

import re
from typing import List

from ipipeline.exceptions import InfoError
from ipipeline.utils.checking import check_none
from ipipeline.utils.instance import build_repr


class Info:
    """Stores the information of an instance.

    The information is used for identification purposes during the life 
    cycle of the instance.

    Attributes
    ----------
    _id : str
        ID of the instance.
    _tags : List[str]
        Tags of the instance to provide more context.
    """

    def __init__(self, id: str, tags: List[str] = None) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the instance.
        tags : List[str], optional
            Tags of the instance to provide more context.

        Raises
        ------
        InfoError
            Informs that the id did not match the pattern.
        """

        self._id = self._check_id(id)
        self._tags = check_none(tags, [])

    @property
    def id(self) -> str:
        """Gets the _id attribute.

        Returns
        -------
        id : str
            ID of the instance.
        """

        return self._id

    @id.setter
    def id(self, id: str) -> None:
        """Sets the _id attribute.

        Parameters
        ----------
        id : str
            ID of the instance.
        """

        self._id = id

    @property
    def tags(self) -> List[str]:
        """Gets the _tags attribute.

        Returns
        -------
        tags : List[str]
            Tags of the instance to provide more context.
        """

        return self._tags

    @tags.setter
    def tags(self, tags: List[str]) -> None:
        """Sets the _tags attribute.

        Parameters
        ----------
        tags : List[str]
            Tags of the instance to provide more context.
        """

        self._tags = tags

    def _check_id(self, id: str) -> str:
        """Checks if the ID matches a pattern.

        The pattern consists of a combination of letters, digits, underscores, 
        dashes, and/or points.

        Parameters
        ----------
        id : str
            ID of the instance.

        Returns
        -------
        id : str
            ID of the instance.

        Raises
        ------
        InfoError
            Informs that the id did not match the pattern.
        """

        if id is not None and re.fullmatch(r'[\w.-]+', id) is not None:
            return id
        else:
            raise InfoError('id did not match the pattern', [f'id == {id}'])

    def __repr__(self) -> str:
        """Builds the representation of an instance.

        Returns
        -------
        repr : str
            Representation of an instance.
        """

        repr = build_repr(self)

        return repr
