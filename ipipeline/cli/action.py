from importlib import import_module

from ipipeline.exception import ActionError
from ipipeline.util.system import create_directory, create_file


def create_project(path: str, name: str) -> None:
    try:
        proj_path = f'{path}/{name}'
        pkg_path = f'{proj_path}/{name}'
        create_directory(proj_path)

        for proj_dir in ['io', 'test', name]:
            create_directory(f'{proj_path}/{proj_dir}')

        for proj_file in [
            '.gitignore', 
            'CONTRIBUTING.md', 
            'LICENSE.md', 
            'README.md', 
            'requirement.txt', 
            'setup.py'
        ]:
            create_file(f'{proj_path}/{proj_file}')

        for pkg_dir in ['config', 'group', 'task']:
            create_directory(f'{pkg_path}/{pkg_dir}')

            for sub_file in ['__init__.py']:
                create_file(f'{pkg_path}/{pkg_dir}/{sub_file}')

        for pkg_file in ['exception.py', '__init__.py', '__main__.py']:
            create_file(f'{pkg_path}/{pkg_file}')
    except Exception as error:
        raise ActionError(
            'project not created in the file system', f'path == {path}'
        ) from error


def execute_pipeline(mod_name: str, func_name: str, exe_type: str) -> None:
    try:
        pipeline = getattr(import_module(mod_name), func_name)()
    except (ModuleNotFoundError, AttributeError) as error:
        raise ActionError(
            'func not found in the module', f'func_name == {func_name}'
        ) from error

    try:
        executor = getattr(
            import_module('ipipeline.control.execution'), 
            f'{exe_type.capitalize()}Executor'
        )(pipeline)
        executor.execute_pipeline(executor.obtain_exe_order())
    except AttributeError as error:
        raise ActionError(
            'executor not found in the module', f'exe_type == {exe_type}'
        ) from error
