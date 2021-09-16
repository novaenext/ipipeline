import sys

from ipipeline.cli.commands import execute_cli_cmds
from ipipeline.cli.parsing import parse_cli_args


def main() -> None:
    try:
        if len(sys.argv) > 1:
            args = parse_cli_args(sys.argv[1:])
            execute_cli_cmds(sys.argv[1], args)
        else:
            parse_cli_args(['--help'])
    except Exception as error:
        print('error:', ': '.join(error.args), file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
