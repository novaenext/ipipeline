from argparse import ArgumentParser, Namespace
from typing import List

from ipipeline import __version__


def _build_parsers() -> List[ArgumentParser]:
    root_parser = ArgumentParser(
        prog='ipipeline', 
        usage='ipipeline <command> [options]', 
        description='ipipeline cli', 
        add_help=False
    )
    subparsers = root_parser.add_subparsers(metavar='commands')

    project_parser = subparsers.add_parser(
        'project', 
        prog='ipipeline project', 
        usage='ipipeline project <arguments> [options]', 
        description='create the standard project structure', 
        help='create the standard project structure', 
        add_help=False
    )

    return root_parser, project_parser


def _build_root_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        '-h', 
        '--help', 
        action='help', 
        help='show the available arguments'
    )
    parser.add_argument(
        '-v', 
        '--version', 
        action='version', 
        version=f'ipipeline v{__version__}', 
        help='show the version of the package'
    )


def _build_project_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        'path', 
        type=str, 
        action='store', 
        help='path where the project should be created'
    )
    parser.add_argument(
        'name', 
        type=str, 
        action='store', 
        help='name of the project directory'
    )
    parser.add_argument(
        '-h', 
        '--help', 
        action='help', 
        help='show the available arguments'
    )
