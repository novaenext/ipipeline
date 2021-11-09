from argparse import ArgumentParser
from unittest import TestCase

from ipipeline.cli.argument import path_arg, help_arg
from ipipeline.cli.command import root_cmd, project_cmd, execution_cmd
from ipipeline.cli.parsing import create_parser, _add_pos_args, _add_opt_args


class TestCreateCliParser(TestCase):
    def test_valid_cmds(self) -> None:
        parser = create_parser(root_cmd, project_cmd, execution_cmd)

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['project', '-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['execution', '-h'])

    def test_invalid_cmds(self) -> None:
        parser = create_parser(root_cmd, project_cmd, execution_cmd)

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['project', '-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['execution', '-i'])


class TestAddPosArgs(TestCase):
    def test_valid_args(self) -> None:
        parser = ArgumentParser()
        _add_pos_args(parser, [path_arg])
        args = parser.parse_args(args=['mock_path'])

        self.assertEqual(args.path, 'mock_path')

    def test_invalid_args(self) -> None:
        parser = ArgumentParser()
        _add_pos_args(parser, [path_arg])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(args=['mock_path', 'mock_name'])


class TestAddOptArgs(TestCase):
    def test_valid_args(self) -> None:
        parser = ArgumentParser(add_help=False)
        _add_opt_args(parser, [help_arg])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['--help'])

    def test_invalid_args(self) -> None:
        parser = ArgumentParser(add_help=False)
        _add_opt_args(parser, [help_arg])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['--invalid'])
