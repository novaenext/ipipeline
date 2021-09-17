from argparse import Namespace

from ipipeline.utils.system import create_directory, create_file


def _execute_project_cmd(parsed_args: Namespace) -> None:
    project_path = f'{parsed_args.path}/{parsed_args.name}'
    create_directory(project_path)

    for root_dir in [parsed_args.name, 'io', 'tests']:
        create_directory(f'{project_path}/{root_dir}')

    for root_file in [
        '.gitignore', 
        'CONTRIBUTING.md', 
        'LICENSE.md', 
        'README.md', 
        'requirements.txt', 
        'setup.py'
    ]:
        create_file(f'{project_path}/{root_file}')

    for package_file in ['__init__.py', '__main__.py', 'exceptions.py']:
        create_file(f'{project_path}/{parsed_args.name}/{package_file}')

    for subpackage_dir in ['configs', 'groups', 'tasks']:
        create_directory(f'{project_path}/{parsed_args.name}/{subpackage_dir}')

        for subpackage_file in ['__init__.py']:
            create_directory(
                f'{project_path}/{parsed_args.name}/'
                f'{subpackage_dir}/{subpackage_file}'
            )
