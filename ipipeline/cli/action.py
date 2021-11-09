"""Functions related to the action procedures."""

import sys
from importlib import import_module
from pathlib import Path

from ipipeline.exception import ActionError
from ipipeline.util.system import create_directory, create_file


def create_project(path: str, name: str) -> None:
    """Creates a project in the file system.

    The project provides a standard structure for organizing the tasks that 
    interact with the package.

    Parameters
    ----------
    path : str
        Path of the project.
    name : str
        Name of the project.

    Raises
    ------
    ActionError
        Informs that the project was not created in the file system.
    """

    try:
        proj_path = f'{path}/{name}'
        pkg_path = f'{proj_path}/{name}'
        create_directory(proj_path, missing=True, suppressed=True)

        for proj_dir in ['io', 'requirements', 'tests', name]:
            create_directory(f'{proj_path}/{proj_dir}')

        for proj_file in [
            '.gitignore', 
            'CONTRIBUTING.md', 
            'LICENSE.md', 
            'MANIFEST.in', 
            'README.md', 
            'setup.py'
        ]:
            create_file(f'{proj_path}/{proj_file}')

        for pkg_dir in ['config', 'group', 'task']:
            create_directory(f'{pkg_path}/{pkg_dir}')

        for pkg_file in ['exception.py', '__init__.py', '__main__.py']:
            create_file(f'{pkg_path}/{pkg_file}')
    except Exception as error:
        raise ActionError(
            'project not created in the file system', f'path == {path}'
        ) from error


def execute_pipeline(mod_name: str, func_name: str, exe_type: str) -> None:
    """Executes a pipeline according to an executor.

    The pipeline is obtained from the return of a function declared in 
    a module.

    Parameters
    ----------
    mod_name : str
        Name of the module.
    func_name : str
        Name of the function.
    exe_type : {'sequential'}
        Type of the executor.

        sequential: executes a pipeline sequentially.

    Raises
    ------
    ActionError
        Informs that the func_name was not found in the module.
    ActionError
        Informs that the exe_type was not found in the module.
    """

    sys.path.append(str(Path(f'./{mod_name.split(".")[0]}').resolve()))

    try:
        pipeline = getattr(import_module(mod_name), func_name)()
    except (ModuleNotFoundError, AttributeError) as error:
        raise ActionError(
            'func_name not found in the module', f'func_name == {func_name}'
        ) from error

    try:
        executor = getattr(
            import_module('ipipeline.control.execution'), 
            f'{exe_type.capitalize()}Executor'
        )(pipeline)
        executor.execute_pipeline(executor.obtain_topo_order())
    except AttributeError as error:
        raise ActionError(
            'exe_type not found in the module', f'exe_type == {exe_type}'
        ) from error
