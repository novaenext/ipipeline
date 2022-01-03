"""Class and dictionary related to the argument procedures."""

from typing import Callable

from ipipeline import __version__


class Argument:
    """Stores the specifications of an argument.

    The instances of this class are added as an argument to a parser. The 
    values for the parameters must be consulted in the argparse package 
    documentation. 

    Attributes
    ----------
    _name : str
        Name of the argument.
    _descr : str
        Description of the argument.
    _action : str
        Action applied to the argument.
    _type : Callable
        Type to cast the argument.
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
            Action applied to the argument.
        type : Callable
            Type to cast the argument.
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
            Action applied to the argument.
        """

        return self._action

    @property
    def type(self) -> Callable:
        """Obtains the _type attribute.

        Returns
        -------
        type : Callable
            Type to cast the argument.
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


args = {
    'path': Argument(
        'path', 
        'path of the project.', 
        'store', 
        str
    ), 
    'name': Argument(
        'name', 
        'name of the project.', 
        'store', 
        str
    ), 
    'mod_name': Argument(
        'mod_name', 
        'name of the module in absolute terms (package.module).', 
        'store', 
        str
    ), 
    'func_name': Argument(
        'func_name', 
        'name of the function that returns a pipeline.', 
        'store', 
        str
    ), 
    'exe_type': Argument(
        'exe_type', 
        'type of the executor.\n\n'
        'sequential: executes a pipeline sequentially.', 
        'store', 
        str
    ), 
    'help': Argument(
        'help', 
        'shows the available arguments.', 
        'help', 
        None
    ), 
    'version': Argument(
        'version', 
        'shows the version of the package.', 
        'version', 
        None, 
        version=__version__
    )
}
