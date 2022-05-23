"""Functions related to the instance procedures."""

import sys
from importlib import import_module
from inspect import signature
from pathlib import Path

from ipipeline.exceptions import InstanceError


def build_repr(inst: object) -> str:
    """Builds the representation of an instance.

    The class name and the initializer parameters are used to create the 
    representation.

    Parameters
    ----------
    inst : object
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

    repr = f'{repr})'.replace(', )', ')')

    return repr


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
