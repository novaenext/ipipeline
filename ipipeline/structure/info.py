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
        tags : List[str], default=None
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

    @property
    def tags(self) -> List[str]:
        """Gets the _tags attribute.

        Returns
        -------
        tags : List[str]
            Tags of the instance to provide more context.
        """

        return self._tags

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

        if re.fullmatch(r'[\w.-]+', id) is not None:
            return id
        else:
            raise InfoError('id did not match the pattern', [f'id == {id}'])

    def __repr__(self) -> str:
        """Obtains the representation of the instance.

        Returns
        -------
        repr : str
            Representation of the instance.
        """

        return build_repr(self)
