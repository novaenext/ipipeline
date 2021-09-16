from unittest import TestCase

from ipipeline.cli.parsing import _build_parsers


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
