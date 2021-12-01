"""Functions related to the action procedures."""

from ipipeline.control.execution import obtain_executor_class
from ipipeline.structure.pipeline import obtain_pipeline
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
    SystemError
        Informs that the directory was not created in the file system.
    SystemError
        Informs that the file was not created in the file system.
    """

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


def execute_pipeline(mod_name: str, func_name: str, exe_type: str) -> None:
    """Executes a pipeline according to an executor.

    The pipeline is obtained from the return of a function declared in 
    a module.

    Parameters
    ----------
    mod_name : str
        Name of the module in absolute terms (pkg.mod).
    func_name : str
        Name of the function.
    exe_type : {'sequential'}
        Type of the executor class.

        sequential: executes a pipeline sequentially.

    Raises
    ------
    PipelineError
        Informs that the func_name was not found in the module.
    ExecutionError
        Informs that the type was not found in the executors.
    ExecutionError
        Informs that the node was not executed by the executor.
    """

    pipeline = obtain_pipeline(mod_name, func_name)
    executor = obtain_executor_class(exe_type)(pipeline)
    executor.execute_pipeline(executor.obtain_topo_order())
