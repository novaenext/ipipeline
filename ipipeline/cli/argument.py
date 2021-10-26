"""Classes and variables related to the argument procedures.

The arguments are designed to work with the argparse package, 
therefore, the possible values for some of the parameters must be 
consulted in its documentation.
"""

from abc import ABC
from typing import Callable

from ipipeline import __version__


class BaseArgument(ABC):
    """Provides an interface to the argument classes.

    Attributes
    ----------
    _name : str
        Name of the argument.
    _descr : str
        Description of the argument.
    _action : str
        Action to be applied to the argument.
    _type : Callable
        The type to which the argument must be converted.
    _key_args : dict
        Keyword arguments of the add_argument method.
    """

    def __init__(
        self, 
        name: str, 
        descr: str, 
        action: str, 
        type: Callable, 
        **key_args: dict
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        name : str
            Name of the argument.
        descr : str
            Description of the argument.
        action : str
            Action to be applied to the argument.
        type : Callable
            The type to which the argument must be converted.
        key_args : dict
            Keyword arguments of the add_argument method.
        """

        self._name = name
        self._descr = descr
        self._action = action
        self._type = type
        self._key_args = key_args

    @property
    def name(self) -> str:
        """Obtains the _name attribute.

        Returns
        -------
        name : str
            Name of the argument.
        """

        return self._name

    @property
    def descr(self) -> str:
        """Obtains the _descr attribute.

        Returns
        -------
        descr : str
            Description of the argument.
        """

        return self._descr

    @property
    def action(self) -> str:
        """Obtains the _action attribute.

        Returns
        -------
        action : str
            Action to be applied to the argument.
        """

        return self._action

    @property
    def type(self) -> Callable:
        """Obtains the _type attribute.

        Returns
        -------
        type : Callable
            The type to which the argument must be converted.
        """

        return self._type

    @property
    def key_args(self) -> dict:
        """Obtains the _key_args attribute.

        Returns
        -------
        key_args : dict
            Keyword arguments of the add_argument method.
        """

        return self._key_args


class Argument(BaseArgument):
    """Stores the specification of an argument.

    The instances of this class are added as an argument to a parser.

    Attributes
    ----------
    _name : str
        Name of the argument.
    _descr : str
        Description of the argument.
    _action : str
        Action to be applied to the argument.
    _type : Callable
        The type to which the argument must be converted.
    _key_args : dict
        Keyword arguments of the add_argument method.
    """

    pass


path_arg = Argument(
    'path', 
    'path of the project', 
    'store', 
    str
)


name_arg = Argument(
    'name', 
    'name of the project', 
    'store', 
    str
)


mod_name_arg = Argument(
    'mod_name', 
    'name of the module where the function is declared', 
    'store', 
    str
)


func_name_arg = Argument(
    'func_name', 
    'name of the function responsible for returning a pipeline', 
    'store', 
    str
)


exe_type_arg = Argument(
    'exe_type', 
    'type of the executor to execute the pipeline', 
    'store', 
    str
)


help_arg = Argument(
    'help', 
    'show the available arguments', 
    'help', 
    None
)


version_arg = Argument(
    'version', 
    'show the version of the package', 
    'version', 
    None, 
    version=f'ipipeline v{__version__}'
)
