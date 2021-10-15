from argparse import ArgumentParser
from typing import List

from ipipeline.cli.argument import Argument
from ipipeline.cli.command import Command


def create_parser(
    root_cmd: Command, *sub_cmds: List[Command]
) -> ArgumentParser:
    root_parser = ArgumentParser(
        prog=root_cmd.name, 
        usage=f'{root_cmd.name} <command> [options]', 
        description=root_cmd.descr, 
        add_help=False
    )
    subparsers = root_parser.add_subparsers(metavar='commands')
    _add_pos_args(root_parser, root_cmd.pos_args)
    _add_opt_args(root_parser, root_cmd.opt_args)

    for sub_cmd in sub_cmds:
        sub_parser = subparsers.add_parser(
            sub_cmd.name, 
            prog=f'{root_cmd.name} {sub_cmd.name}', 
            usage=f'{root_cmd.name} {sub_cmd.name} <arguments> [options]', 
            description=sub_cmd.descr, 
            help=sub_cmd.descr, 
            add_help=False
        )
        sub_parser.set_defaults(execute_action=sub_cmd.action)
        _add_pos_args(sub_parser, sub_cmd.pos_args)
        _add_opt_args(sub_parser, sub_cmd.opt_args)

    return root_parser


def _add_pos_args(parser: ArgumentParser, pos_args: List[Argument]) -> None:
    for pos_arg in pos_args:
        parser.add_argument(
            pos_arg.name, 
            help=pos_arg.descr, 
            action=pos_arg.action, 
            type=pos_arg.type, 
            **pos_arg.key_args
        )


def _add_opt_args(parser: ArgumentParser, opt_args: List[Argument]) -> None:
    for opt_arg in opt_args:
        parser.add_argument(
            f'-{opt_arg.name[0]}', 
            f'--{opt_arg.name}', 
            help=opt_arg.descr, 
            action=opt_arg.action, 
            **opt_arg.key_args
        )
