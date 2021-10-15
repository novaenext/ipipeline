from abc import ABC
from typing import Callable, List

from ipipeline.cli.action import create_project, execute_pipeline
from ipipeline.cli.argument import (
    Argument, 
    path_arg, 
    name_arg, 
    mod_name_arg, 
    func_name_arg, 
    exe_type_arg, 
    help_arg, 
    version_arg
)


class BaseCommand(ABC):
    def __init__(
        self, 
        name: str, 
        descr: str, 
        action: Callable, 
        pos_args: List[Argument], 
        opt_args: List[Argument], 
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
        return self._name

    @property
    def descr(self) -> str:
        return self._descr

    @property
    def action(self) -> Callable:
        return self._action

    @property
    def pos_args(self) -> List[Argument]:
        return self._pos_args

    @property
    def opt_args(self) -> List[Argument]:
        return self._opt_args

    @property
    def key_args(self) -> dict:
        return self._key_args


class Command(BaseCommand):
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
    'execute a pipeline according to an executor type', 
    execute_pipeline, 
    [mod_name_arg, func_name_arg, exe_type_arg], 
    [help_arg]
)
