"""Functions related to the parsing procedures.

These functions act as a wrapper for the argparse package, exposing 
only the necessary parameters and performing some common operations 
by default.
"""

from argparse import ArgumentParser
from typing import List

from ipipeline.cli.argument import BaseArgument
from ipipeline.cli.command import BaseCommand


def create_parser(
    root_cmd: BaseCommand, *sub_cmds: List[BaseCommand]
) -> ArgumentParser:
    """Creates a parser for the CLI.

    Parameters
    ----------
    root_cmd : BaseCommand
        Root command that defines the initial interface.
    sub_cmds : List[BaseCommand]
        Sub-commands available in the initial interface.

    Returns
    -------
    parser : ArgumentParser
        Parser for the CLI.

    Raises
    ------
    SystemExit
        Informs an exit code about the parsing.

        0: success.
        2: failure due to a syntax error.
    """

    parser = ArgumentParser(
        prog=root_cmd.name, 
        usage=f'{root_cmd.name} <command> [options]', 
        description=root_cmd.descr, 
        add_help=False, 
        **root_cmd.key_args
    )
    subparsers = parser.add_subparsers(metavar='commands')
    _add_pos_args(parser, root_cmd.pos_args)
    _add_opt_args(parser, root_cmd.opt_args)

    for sub_cmd in sub_cmds:
        sub_parser = subparsers.add_parser(
            sub_cmd.name, 
            prog=f'{root_cmd.name} {sub_cmd.name}', 
            usage=f'{root_cmd.name} {sub_cmd.name} <arguments> [options]', 
            description=sub_cmd.descr, 
            help=sub_cmd.descr, 
            add_help=False, 
            **sub_cmd.key_args
        )
        sub_parser.set_defaults(execute_action=sub_cmd.action)
        _add_pos_args(sub_parser, sub_cmd.pos_args)
        _add_opt_args(sub_parser, sub_cmd.opt_args)

    return parser


def _add_pos_args(
    parser: ArgumentParser, pos_args: List[BaseArgument]
) -> None:
    """Adds the positional arguments in a parser.

    Parameters
    ----------
    parser : ArgumentParser
        Parser of a command.
    pos_args : List[BaseArgument]
        Positional arguments of the parser.
    """

    for pos_arg in pos_args:
        parser.add_argument(
            pos_arg.name, 
            help=pos_arg.descr, 
            action=pos_arg.action, 
            type=pos_arg.type, 
            **pos_arg.key_args
        )


def _add_opt_args(
    parser: ArgumentParser, opt_args: List[BaseArgument]
) -> None:
    """Adds the optional arguments in a parser.

    Parameters
    ----------
    parser : ArgumentParser
        Parser of a command.
    opt_args : List[BaseArgument]
        Optional arguments of the parser.
    """

    for opt_arg in opt_args:
        parser.add_argument(
            f'-{opt_arg.name[0]}', 
            f'--{opt_arg.name}', 
            help=opt_arg.descr, 
            action=opt_arg.action, 
            **opt_arg.key_args
        )
