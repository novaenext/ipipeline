from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from ipipeline.cli.actions import create_project, execute_pipeline
from ipipeline.exceptions import InstanceError, SystemError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline


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
            'MANIFEST.in', 
            'mock_proj', 
            'README.md', 
            'requirements', 
            'setup.py', 
            'tests'
        ]
        pkg_items = [
            'configs', 
            'exceptions.py', 
            'pipelines', 
            'tasks', 
            '__init__.py', 
            '__main__.py'
        ]

        for proj_item in proj_items:
            self.assertTrue((self._path / proj_item).exists())

        for pkg_item in pkg_items:
            self.assertTrue((self._path / 'mock_proj' / pkg_item).exists())

    def test_existent_project(self) -> None:
        create_project(str(self._path.parents[0]), 'mock_proj')

        with self.assertRaisesRegex(
            SystemError, r'path was found in the file system: path == *'
        ):
            create_project(str(self._path.parents[0]), 'mock_proj')


class TestExecutePipeline(TestCase):
    def test_execute_pipeline__mod_name_eq_mod(self) -> None:
        execute_pipeline(
            'SequentialExecutor', 
            'tests.cli.test_actions', 
            'tests.cli.test_actions', 
            'build_pipeline', 
            'build_catalog'
        )

        self.assertTrue(True)

    def test_execute_pipeline__mod_name_ne_mod(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'mod_name was not found in the package: '
            r'mod_name == tests.cli.test_'
        ):
            execute_pipeline(
                'SequentialExecutor', 
                'tests.cli.test_', 
                'tests.cli.test_actions', 
                'build_pipeline', 
                'build_catalog'
            )

    def test_execute_pipeline__func_name_ne_func(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'inst_name was not found in the module: '
            r'inst_name == build_'
        ):
            execute_pipeline(
                'SequentialExecutor', 
                'tests.cli.test_actions', 
                'tests.cli.test_actions', 
                'build_', 
                'build_catalog'
            )


def build_pipeline() -> Pipeline:
    pipeline = Pipeline('p1')
    pipeline.add_node('n1', lambda p1: print(f'p1: {p1}'), pos_inputs=['i1'])

    return pipeline


def build_catalog() -> Catalog:
    catalog = Catalog('c1')
    catalog.set_item('i1', 2)

    return catalog
