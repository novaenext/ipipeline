from argparse import Namespace

from ipipeline.utils.system import create_directory, create_file


def execute_cli_cmds(cmd: str, args: Namespace) -> None:
    if cmd == 'project':
        _execute_project_cmd(args)


def _execute_project_cmd(args: Namespace) -> None:
    project_path = f'{args.path}/{args.name}'
    create_directory(project_path)

    for root_dir in [args.name, 'io', 'tests']:
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

    for package_file in ['__init__.py', 'exceptions.py']:
        create_file(f'{project_path}/{args.name}/{package_file}')

    for subpackage_dir in ['configs', 'groups', 'tasks']:
        create_directory(f'{project_path}/{args.name}/{subpackage_dir}')

        for subpackage_file in ['__init__.py']:
            create_directory(
                f'{project_path}/{args.name}/'
                f'{subpackage_dir}/{subpackage_file}'
            )
