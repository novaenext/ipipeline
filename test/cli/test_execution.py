from unittest import TestCase

from ipipeline.cli.execution import execute_cli


class TestExecuteCli(TestCase):
    def test_valid_arg(self) -> None:
        with self.assertRaisesRegex(SystemExit, r'0'):
            execute_cli(['--version'])

    def test_empty_arg(self) -> None:
        with self.assertRaisesRegex(SystemExit, r'0'):
            execute_cli([])

    def test_failed_arg(self) -> None:
        with self.assertRaisesRegex(SystemExit, r'1'):
            execute_cli(['execution', 'module', 'func', 'executor'])

    def test_invalid_arg(self) -> None:
        with self.assertRaisesRegex(SystemExit, r'2'):
            execute_cli(['--invalid'])
