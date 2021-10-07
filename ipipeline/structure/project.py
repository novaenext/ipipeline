from ipipeline.utils.system import create_directory, create_file


def create_project(path: str, proj_name: str, pkg_name: str) -> None:
    proj_path = f'{path}/{proj_name}'
    pkg_path = f'{proj_path}/{pkg_name}'
    create_directory(proj_path)

    for proj_dir in ['io', 'tests', pkg_name]:
        create_directory(f'{proj_path}/{proj_dir}')

    for proj_file in [
        '.gitignore', 
        'CONTRIBUTING.md', 
        'LICENSE.md', 
        'README.md', 
        'requirements.txt', 
        'setup.py'
    ]:
        create_file(f'{proj_path}/{proj_file}')

    for pkg_dir in ['configs', 'groups', 'tasks']:
        create_directory(f'{pkg_path}/{pkg_dir}')

        for sub_file in ['__init__.py']:
            create_directory(f'{pkg_path}/{pkg_dir}/{sub_file}')

    for pkg_file in ['exceptions.py', '__init__.py', '__main__.py']:
        create_file(f'{pkg_path}/{pkg_file}')
