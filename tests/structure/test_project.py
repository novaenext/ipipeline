from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from ipipeline.exceptions import SystemError
from ipipeline.structure.project import create_project


class TestCreateProject(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_proj'

    def tearDown(self) -> None:
        rmtree(self._path)

    def test_inexistent_project(self) -> None:
        create_project(str(self._path.parents[0]), 'mock_proj', 'mock_pkg')
        proj_items = [
            '.gitignore', 
            'CONTRIBUTING.md', 
            'io', 
            'LICENSE.md', 
            'mock_pkg', 
            'README.md', 
            'requirements.txt', 
            'setup.py', 
            'tests'
        ]
        pkg_items = [
            'configs', 
            'exceptions.py', 
            'groups', 
            'tasks', 
            '__init__.py', 
            '__main__.py'
        ]

        for proj_item in proj_items:
            self.assertTrue((self._path / proj_item).exists())

        for pkg_item in pkg_items:
            self.assertTrue((self._path / 'mock_pkg' / pkg_item).exists())

        for pkg_dir in ['configs', 'groups', 'tasks']:
            self.assertTrue(
                (self._path / 'mock_pkg' / pkg_dir / '__init__.py').exists()
            )

    def test_existent_project(self) -> None:
        create_project(str(self._path.parents[0]), 'mock_proj', 'mock_pkg')

        with self.assertRaisesRegex(
            SystemError, r'directory not created in the file system: path == *'
        ):
            create_project(str(self._path.parents[0]), 'mock_proj', 'mock_pkg')
