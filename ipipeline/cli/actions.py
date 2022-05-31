"""Functions related to the action procedure."""

from ipipeline.utils.instance import get_inst
from ipipeline.utils.system import build_directory, build_file


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
    build_directory(proj_path, parents=True)

    for proj_dir in ['io', 'requirements', 'tests', name]:
        build_directory(f'{proj_path}/{proj_dir}')

    for proj_file in [
        '.gitignore', 
        'CONTRIBUTING.md', 
        'LICENSE.md', 
        'MANIFEST.in', 
        'README.md', 
        'setup.py'
    ]:
        build_file(f'{proj_path}/{proj_file}')

    for pkg_dir in ['configs', 'pipelines', 'tasks']:
        build_directory(f'{pkg_path}/{pkg_dir}')

    for pkg_file in ['exceptions.py', '__init__.py', '__main__.py']:
        build_file(f'{pkg_path}/{pkg_file}')


def execute_pipeline(mod_name: str, func_name: str, exe_type: str) -> None:
    """Executes a pipeline according to an executor.

    Parameters
    ----------
    mod_name : str
        Name of the module in absolute terms (package.module).
    func_name : str
        Name of the function that returns a pipeline.
    exe_type : {'sequential'}
        Type of the executor.

        sequential: executes a pipeline sequentially.

    Raises
    ------
    InstanceError
        Informs that the inst_name was not found in the module.
    SortingError
        Informs that the dst_node_id was not specified as a src_node_id.
    SortingError
        Informs that a circular dependency was found in the graph.
    ExecutorError
        Informs that the node was not executed by the executor.
    """

    pipeline = get_inst(mod_name, func_name)()
    executor = get_inst(
        'ipipeline.execution.executors', f'{exe_type.capitalize()}Executor'
    )()
    executor.add_pipeline(pipeline)
    topo_order = executor.obtain_topo_order()
    executor.execute_pipeline(topo_order)
