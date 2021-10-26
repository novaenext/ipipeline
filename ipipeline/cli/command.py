"""Classes and variables related to the command procedures.

The commands are designed to work with the argparse package, 
therefore, the possible values for some of the parameters must be 
consulted in its documentation.
"""

from abc import ABC
from typing import Callable, List

from ipipeline.cli.action import create_project, execute_pipeline
from ipipeline.cli.argument import (
    BaseArgument, 
    path_arg, 
    name_arg, 
    mod_name_arg, 
    func_name_arg, 
    exe_type_arg, 
    help_arg, 
    version_arg
)


class BaseCommand(ABC):
    """Provides an interface to the command classes.

    Attributes
    ----------
    _name : str
        Name of the command.
    _descr : str
        Description of the command.
    _action : Callable
        Action to be applied to the command.
    _pos_args : List[BaseArgument]
        Positional arguments of the command.
    _opt_args : List[BaseArgument]
        Optional arguments of the command.
    _key_args : dict
        Keyword arguments of the add_parser method.
    """

    def __init__(
        self, 
        name: str, 
        descr: str, 
        action: Callable, 
        pos_args: List[BaseArgument], 
        opt_args: List[BaseArgument], 
        **key_args: dict
    ) -> None:
        self._name = name
        self._descr = descr
        self._action = action
        self._pos_args = pos_args
        self._opt_args = opt_args
        self._key_args = key_args

    @property
    def name(self) -> str:
        """Obtains the _name attribute.

        Returns
        -------
        name : str
            Name of the command.
        """

        return self._name

    @property
    def descr(self) -> str:
        """Obtains the _descr attribute.

        Returns
        -------
        descr : str
            Description of the command.
        """

        return self._descr

    @property
    def action(self) -> Callable:
        """Obtains the _action attribute.

        Returns
        -------
        action : Callable
            Action to be applied to the command.
        """

        return self._action

    @property
    def pos_args(self) -> List[BaseArgument]:
        """Obtains the _pos_args attribute.

        Returns
        -------
        pos_args : List[BaseArgument]
            Positional arguments of the command.
        """

        return self._pos_args

    @property
    def opt_args(self) -> List[BaseArgument]:
        """Obtains the _opt_args attribute.

        Returns
        -------
        opt_args : List[BaseArgument]
            Optional arguments of the command.
        """

        return self._opt_args

    @property
    def key_args(self) -> dict:
        """Obtains the _key_args attribute.

        Returns
        -------
        key_args : dict
            Keyword arguments of the add_parser method.
        """

        return self._key_args


class Command(BaseCommand):
    """Stores the specification of a command.

    The instances of this class are added as a parser.

    Attributes
    ----------
    _name : str
        Name of the command.
    _descr : str
        Description of the command.
    _action : Callable
        Action to be applied to the command.
    _pos_args : List[BaseArgument]
        Positional arguments of the command.
    _opt_args : List[BaseArgument]
        Optional arguments of the command.
    _key_args : dict
        Keyword arguments of the add_parser method.
    """

    pass


root_cmd = Command(
    'ipipeline', 
    'ipipeline cli', 
    None, 
    [], 
    [help_arg, version_arg]
)


project_cmd = Command(
    'project', 
    'create the standard project structure', 
    create_project, 
    [path_arg, name_arg], 
    [help_arg]
)


execution_cmd = Command(
    'execution', 
    'execute a pipeline according to an executor', 
    execute_pipeline, 
    [mod_name_arg, func_name_arg, exe_type_arg], 
    [help_arg]
)
