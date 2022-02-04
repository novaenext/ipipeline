"""Function related to the execution procedures."""

import sys
from typing import List

from ipipeline.cli.commands import cmds
from ipipeline.cli.parsing import create_parser


def execute_cli(args: List[str]) -> None:
    """Executes a CLI.

    Parameters
    ----------
    args : List[str]
        Arguments of the CLI.

    Raises
    ------
    SystemExit
        Informs an exit code about the execution.

        0: success.
        1: failure due to an action error.
        2: failure due to a syntax error.
    """

    try:
        if len(args) == 0:
            args.append('--help')

        parser = create_parser(
            cmds['root'], [cmds['project'], cmds['execution']]
        )
        parsed_args = vars(parser.parse_args(args=args))
        parsed_args.pop('execute_action')(**parsed_args)

        sys.exit(0)
    except Exception as error:
        print('error:', ': '.join(error.args), file=sys.stderr)
        sys.exit(1)
