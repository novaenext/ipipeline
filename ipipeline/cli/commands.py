"""Class and dictionary related to the command procedures."""

from typing import Callable, List

from ipipeline.cli.actions import build_project, execute_pipeline
from ipipeline.cli.arguments import Argument, args


class Command:
    """Stores the specifications of a command.

    The instances of this class are added as a parser. The values for the 
    parameters must be consulted in the argparse package documentation. 

    Attributes
    ----------
    _name : str
        Name of the command.
    _descr : str
        Description of the command.
    _action : Callable
        Action applied to the command.
    _pos_args : List[Argument]
        Positional arguments of the command.
    _opt_args : List[Argument]
        Optional arguments of the command.
    _key_args : dict
        Keyword arguments of the add_parser method.
    """

    def __init__(
        self, 
        name: str, 
        descr: str, 
        action: Callable, 
        pos_args: List[Argument], 
        opt_args: List[Argument], 
        **key_args: dict
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        name : str
            Name of the command.
        descr : str
            Description of the command.
        action : Callable
            Action applied to the command.
        pos_args : List[Argument]
            Positional arguments of the command.
        opt_args : List[Argument]
            Optional arguments of the command.
        key_args : dict
            Keyword arguments of the add_parser method.
        """

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
            Action applied to the command.
        """

        return self._action

    @property
    def pos_args(self) -> List[Argument]:
        """Obtains the _pos_args attribute.

        Returns
        -------
        pos_args : List[Argument]
            Positional arguments of the command.
        """

        return self._pos_args

    @property
    def opt_args(self) -> List[Argument]:
        """Obtains the _opt_args attribute.

        Returns
        -------
        opt_args : List[Argument]
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


cmds = {
    'root': Command(
        'ipipeline', 
        'cli of the ipipeline package.', 
        None, 
        [], 
        [args['help'], args['version']]
    ), 
    'project': Command(
        'project', 
        'builds a project in the file system.', 
        build_project, 
        [args['path'], args['name']], 
        [args['help']]
    ), 
    'execution': Command(
        'execution', 
        'executes a pipeline.', 
        execute_pipeline, 
        [
            args['executor_class_name'], 
            args['pipeline_mod_name'], 
            args['catalog_mod_name'], 
            args['pipeline_func_name'], 
            args['catalog_func_name']
        ], 
        [args['help']]
    )
}
