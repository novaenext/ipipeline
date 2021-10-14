from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from ipipeline.cli.action import create_project
from ipipeline.exception import ActionError


class TestCreateProject(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_proj'

    def tearDown(self) -> None:
        rmtree(self._path)

    def test_inexistent_project(self) -> None:
        create_project(str(self._path.parents[0]), 'mock_proj')
        proj_items = [
            '.gitignore', 
            'CONTRIBUTING.md', 
            'io', 
            'LICENSE.md', 
            'mock_proj', 
            'README.md', 
            'requirement.txt', 
            'setup.py', 
            'test'
        ]
        pkg_items = [
            'config', 
            'exception.py', 
            'group', 
            'task', 
            '__init__.py', 
            '__main__.py'
        ]

        for proj_item in proj_items:
            self.assertTrue((self._path / proj_item).exists())

        for pkg_item in pkg_items:
            self.assertTrue((self._path / 'mock_proj' / pkg_item).exists())

        for pkg_dir in ['config', 'group', 'task']:
            self.assertTrue(
                (self._path / 'mock_proj' / pkg_dir / '__init__.py').exists()
            )

    def test_existent_project(self) -> None:
        create_project(str(self._path.parents[0]), 'mock_proj')

        with self.assertRaisesRegex(
            ActionError, r'project not created in the file system: path == *'
        ):
            create_project(str(self._path.parents[0]), 'mock_proj')
