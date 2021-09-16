from argparse import Namespace
from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from ipipeline.cli.commands import execute_cli_cmds, _execute_project_cmd
from ipipeline.exceptions import SystemError


class TestExecuteCliCmds(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock'

    def test_project_cmd(self) -> None:
        execute_cli_cmds(
            'project', Namespace(path=str(self._path.parents[0]), name='mock')
        )

        self.assertTrue(self._path.exists())
        rmtree(self._path)

    def test_invalid_cmd(self) -> None:
        execute_cli_cmds('invalid', Namespace())

        self.assertTrue(True)


class TestExecuteProjectCmd(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock'
        self._args = Namespace(path=str(self._path.parents[0]), name='mock')

    def tearDown(self) -> None:
        rmtree(self._path)

    def test_inexistent_project_dir(self) -> None:
        _execute_project_cmd(self._args)

        self.assertTrue(self._path.exists())

    def test_inexistent_root_dirs(self) -> None:
        _execute_project_cmd(self._args)

        for root_dir in ['mock', 'io', 'tests']:
            self.assertTrue((self._path / root_dir).exists())

    def test_inexistent_root_files(self) -> None:
        _execute_project_cmd(self._args)

        for root_file in [
            '.gitignore', 
            'CONTRIBUTING.md', 
            'LICENSE.md', 
            'README.md', 
            'requirements.txt', 
            'setup.py'
        ]:
            self.assertTrue((self._path / root_file).exists())

    def test_inexistent_package_files(self) -> None:
        _execute_project_cmd(self._args)

        for package_file in ['__init__.py', 'exceptions.py']:
            self.assertTrue((self._path / 'mock' / package_file).exists())

    def test_inexistent_subpackage_dirs(self) -> None:
        _execute_project_cmd(self._args)

        for subpackage_dir in ['configs', 'groups', 'tasks']:
            self.assertTrue((self._path / 'mock' / subpackage_dir).exists())

    def test_inexistent_subpackage_files(self) -> None:
        _execute_project_cmd(self._args)

        for subpackage_dir in ['configs', 'groups', 'tasks']:
            for subpackage_file in ['__init__.py']:
                self.assertTrue((
                    self._path / 'mock' / subpackage_dir / subpackage_file
                ).exists())

    def test_existent_project_dir(self) -> None:
        _execute_project_cmd(self._args)

        with self.assertRaisesRegex(
            SystemError, r'directory not created: path == *'
        ):
            _execute_project_cmd(self._args)
