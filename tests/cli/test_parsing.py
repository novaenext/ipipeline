from argparse import ArgumentParser
from unittest import TestCase

from ipipeline.cli.argument import args
from ipipeline.cli.command import cmds
from ipipeline.cli.parsing import create_parser, _add_pos_args, _add_opt_args


class TestCreateParser(TestCase):
    def test_valid_cmds(self) -> None:
        parser = create_parser(
            cmds['root'], [cmds['project'], cmds['execution']]
        )

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['project', '-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['execution', '-h'])

    def test_invalid_cmds(self) -> None:
        parser = create_parser(
            cmds['root'], [cmds['project'], cmds['execution']]
        )

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['project', '-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['execution', '-i'])


class TestAddPosArgs(TestCase):
    def test_valid_args(self) -> None:
        parser = ArgumentParser()
        _add_pos_args(parser, [args['path']])
        parsed_args = parser.parse_args(args=['mock_path'])

        self.assertEqual(parsed_args.path, 'mock_path')

    def test_invalid_args(self) -> None:
        parser = ArgumentParser()
        _add_pos_args(parser, [args['path']])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(args=['mock_path', 'mock_name'])


class TestAddOptArgs(TestCase):
    def test_valid_args(self) -> None:
        parser = ArgumentParser(add_help=False)
        _add_opt_args(parser, [args['help']])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['--help'])

    def test_invalid_args(self) -> None:
        parser = ArgumentParser(add_help=False)
        _add_opt_args(parser, [args['help']])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['--invalid'])
