"""Class related to the information procedures."""

import re
from typing import List

from ipipeline.exception import InfoError
from ipipeline.util.instance import build_repr, check_none_arg


class Info:
    """Stores the information of an instance.

    This class must be used as a base class to provide information for 
    instances of a class that derive from it.

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
            Informs that the id was not validated according to the pattern.
        """

        self._id = self._check_valid_id(id)
        self._tags = check_none_arg(tags, [])

    @property
    def id(self) -> str:
        """Obtains the _id attribute.

        Returns
        -------
        id : str
            ID of the instance.
        """

        return self._id

    @property
    def tags(self) -> List[str]:
        """Obtains the _tags attribute.

        Returns
        -------
        tags : List[str]
            Tags of the instance to provide more context.
        """

        return self._tags

    def _check_valid_id(self, id: str) -> str:
        """Checks if the ID is valid.

        A valid ID consists of a combination of letters, digits, underscores 
        and/or dashes.

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
            Informs that the id was not validated according to the pattern.
        """

        if re.fullmatch(r'[\w-]+', id):
            return id
        else:
            raise InfoError(
                'id not validated according to the pattern '
                '(letters, digits, underscores and/or dashes)', 
                f'id == {id}'
            )

    def __repr__(self) -> str:
        """Obtains the representation of the instance.

        Returns
        -------
        repr : str
            Representation of the instance.
        """

        return build_repr(self)