"""Functions related to the instance procedures."""

import sys
from importlib import import_module
from inspect import signature
from pathlib import Path
from typing import Any

from ipipeline.exceptions import InstanceError


def check_none_arg(arg: Any, default: Any) -> Any:
    """Checks if the arg is None.

    Parameters
    ----------
    arg : Any
        Argument of a callable.
    default : Any
        Default value to assign to the arg if it is None.

    Returns
    -------
    arg : Any
        Argument of a callable with its original or default value.
    """

    if arg is None:
        arg = default

    return arg


def build_inst_repr(inst: object) -> str:
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

    repr = f'{inst.__class__.__name__}('

    for param in signature(inst.__init__).parameters.values():
        value = None

        for attr in [f'_{param.name}', param.name]:
            if attr in inst.__dict__:
                value = getattr(inst, attr)

                if isinstance(value, str):
                    value = f'\'{value}\''

                break

        repr += f'{param.name}={value}, '

    return f'{repr})'.replace(', )', ')')


def obtain_mod_inst(mod_name: str, inst_name: str) -> object:
    """Obtains an instance declared in a module.

    Parameters
    ----------
    mod_name : str
        Name of the module in absolute terms (package.module).
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
