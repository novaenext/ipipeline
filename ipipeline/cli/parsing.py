from argparse import ArgumentParser
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
