"""Package execution procedures."""

import sys

from ipipeline.cli.execution import execute_cli


if __name__ == '__main__':
    execute_cli(sys.argv[1:])
