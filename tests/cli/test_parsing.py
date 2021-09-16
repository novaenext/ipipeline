from argparse import ArgumentParser
from unittest import TestCase

from ipipeline.cli.parsing import _build_parsers, _build_root_args


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
    def test_help_option(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_root_args(parser)

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['--help'])

    def test_version_option(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_root_args(parser)

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['-v'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            parser.parse_args(['--version'])

    def test_invalid_option(self) -> None:
        parser = ArgumentParser(add_help=False)
        _build_root_args(parser)

        with self.assertRaisesRegex(SystemExit, r'2'):
            parser.parse_args(['--invalid'])
