"""Classes and functions related to the instance procedures."""

import re
import sys
from importlib import import_module
from inspect import signature
from pathlib import Path
from typing import List

from ipipeline.exception import InstanceError


class Identification:
    """Stores the identification of an instance.

    This class must be used as a base class to provide identification 
    properties for instances of a class that derive from it.

    Attributes
    ----------
    _id : str
        ID of the instance.
    _tags : List[str]
        Tags of the instance to provide more context.
    """

    def __init__(self, id: str, tags: List[str] = []) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the instance.
        tags : List[str], default=[]
            Tags of the instance to provide more context.

        Raises
        ------
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        self._id = self._check_valid_id(id)
        self._tags = tags

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
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        if re.fullmatch(r'[\w-]+', id):
            return id
        else:
            raise InstanceError(
                'id not validated according to the pattern '
                '(letters, digits, underscores and/or dashes)', 
                f'id == {id}'
            )

    def __repr__(self) -> str:
        """Obtains the instance representation.

        Returns
        -------
        instance_repr : str
            Instance representation.
        """

        return build_repr(self)


def build_repr(instance: object) -> str:
    """Builds the representation of an instance.

    The class name and the parameters in the initializer signature are 
    used to create the representation.

    Parameters
    ----------
    instance : object
        Instance of a class.

    Returns
    -------
    repr : str
        Representation of an instance.
    """

    repr = f'{instance.__class__.__name__}('

    for param in signature(instance.__init__).parameters.values():
        value = None

        for attr in [f'_{param.name}', param.name]:
            if attr in instance.__dict__:
                value = getattr(instance, attr)

                if isinstance(value, str):
                    value = f'\'{value}\''

                break

        repr += f'{param.name}={value}, '

    return f'{repr})'.replace(', )', ')')


def obtain_instance(mod_name: str, inst_name: str) -> object:
    """Obtains an instance declared in a module.

    Parameters
    ----------
    mod_name : str
        Name of the module in absolute terms (pkg.mod).
    inst_name : str
        Name of the instance declared in the module.

    Returns
    -------
    instance : object
        Instance of a class.

    Raises
    ------
    InstanceError
        Informs that the inst_name was not found in the module.
    """

    sys.path.append(str(Path(mod_name.split('.')[0]).resolve()))

    try:
        return getattr(import_module(mod_name), inst_name)
    except (ModuleNotFoundError, AttributeError) as error:
        raise InstanceError(
            'inst_name not found in the module', f'inst_name == {inst_name}'
        ) from error
