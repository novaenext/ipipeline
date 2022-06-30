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


def execute_pipeline(
    executor_class_name: str, 
    pipeline_mod_name: str, 
    catalog_mod_name: str, 
    pipeline_func_name: str, 
    catalog_func_name: str
) -> None:
    """Executes a pipeline.

    Parameters
    ----------
    executor_class_name : str
        Name of the executor class.
    pipeline_mod_name : str
        Name of the module where a pipeline function is declared.
    catalog_mod_name : str
        Name of the module where a catalog function is declared.
    pipeline_func_name : str
        Name of the function that returns a pipeline.
    catalog_func_name : str
        Name of the function that returns a catalog.
    """

    executor_mod_name = 'ipipeline.control.executors'
    executor = get_inst(executor_mod_name, executor_class_name)()
    pipeline = get_inst(pipeline_mod_name, pipeline_func_name)()
    catalog = get_inst(catalog_mod_name, catalog_func_name)()

    ordering = executor.get_ordering(pipeline)
    _ = executor.execute_pipeline(pipeline, catalog, ordering)
