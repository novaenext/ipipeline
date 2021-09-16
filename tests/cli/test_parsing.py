from argparse import ArgumentParser
from unittest import TestCase

from ipipeline.cli.parsing import (
    _build_parsers, _build_root_args, _build_project_args
)


class TestBuildParsers(TestCase):
    def test_root_parser(self) -> None:
        root_parser, _ = _build_parsers()

        self.assertEqual(root_parser.prog, 'ipipeline')
        self.assertEqual(root_parser.usage, 'ipipeline <command> [options]')
        self.assertEqual(root_parser.description, 'ipipeline cli')
        self.assertEqual(root_parser.add_help, False)

    def test_project_parser(self) -> None:
        _, project_parser = _build_parsers()

        self.assertEqual(
            project_parser.prog, 'ipipeline project'
        )
        self.assertEqual(
            project_parser.usage, 'ipipeline project <arguments> [options]'
        )
        self.assertEqual(
            project_parser.description, 'create the standard project structure'
        )
        self.assertEqual(
            project_parser.add_help, False
        )


class TestBuildRootArgs(TestCase):
    def test_optional_help_arg(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_root_args(parser)

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['--help'])

    def test_optional_version_arg(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_root_args(parser)

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['-v'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['--version'])

    def test_invalid_arg(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_root_args(parser)

        with self.assertRaisesRegex(SystemExit, r'2'):
            parser.parse_args(['--invalid'])


class TestBuildProjectArgs(TestCase):
    def test_positional_args(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_project_args(parser)
        args = parser.parse_args(['mock_path', 'mock_name'])

        self.assertEqual(args.path, 'mock_path')
        self.assertEqual(args.name, 'mock_name')

    def test_optional_help_arg(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_project_args(parser)

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['--help'])

    def test_invalid_arg(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_project_args(parser)

        with self.assertRaisesRegex(SystemExit, r'2'):
            parser.parse_args(['--invalid'])
