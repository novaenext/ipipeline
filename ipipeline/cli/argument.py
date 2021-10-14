from abc import ABC
from typing import Callable

from ipipeline import __version__


class BaseArgument(ABC):
    def __init__(
        self, 
        name: str, 
        descr: str, 
        action: str, 
        type: Callable, 
        **key_args: dict
    ) -> None:
        self._name = name
        self._descr = descr
        self._action = action
        self._type = type
        self._key_args = key_args

    @property
    def name(self) -> str:
        return self._name

    @property
    def descr(self) -> str:
        return self._descr

    @property
    def action(self) -> str:
        return self._action

    @property
    def type(self) -> Callable:
        return self._type

    @property
    def key_args(self) -> dict:
        return self._key_args


class Argument(BaseArgument):
    pass


path_arg = Argument(
    'path', 
    'path where the project should be created', 
    'store', 
    str
)


name_arg = Argument(
    'name', 
    'name of the project directory', 
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
    'name of the function responsible for building a pipeline', 
    'store', 
    str
)


exe_type_arg = Argument(
    'exe_type', 
    'type of executor to execute the pipeline', 
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
