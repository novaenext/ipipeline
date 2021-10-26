from pathlib import Path
from shutil import rmtree
from unittest import TestCase
from unittest.mock import Mock

from ipipeline.cli.action import create_project, execute_pipeline
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


def mock_build_pipeline() -> Mock:
    mock_node = Mock(
        spec=['id', 'func', 'inputs', 'outputs', 'tags']
    )
    mock_node.id = 'n1'
    mock_node.func = lambda param1, param2: param1 + param2
    mock_node.inputs = {'param1': 7, 'param2': 3}
    mock_node.outputs = ['sum']
    mock_node.tags = ['math']

    mock_pipeline = Mock(
        spec=['id', 'nodes', 'conns', 'graph', 'tags']
    )
    mock_pipeline.nodes = {'n1': mock_node}
    mock_pipeline.graph = {'n1': []}

    return mock_pipeline


class TestExecutePipeline(TestCase):
    def test_valid_func_name(self) -> None:
        execute_pipeline(
            'test.cli.test_action', 'mock_build_pipeline', 'sequential'
        )

        self.assertTrue(True)

    def test_invalid_func_name(self) -> None:
        with self.assertRaisesRegex(
            ActionError, 
            r'func_name not found in the module: func_name == '
            r'mock_build_pipelines'
        ):
            execute_pipeline(
                'test.cli.test_action', 'mock_build_pipelines', 'sequential'
            )

    def test_invalid_mod_name(self) -> None:
        with self.assertRaisesRegex(
            ActionError, 
            r'func_name not found in the module: func_name == '
            r'mock_build_pipeline'
        ):
            execute_pipeline(
                'test.cli.test_actions', 'mock_build_pipeline', 'sequential'
            )

    def test_invalid_exe_type(self) -> None:
        with self.assertRaisesRegex(
            ActionError, 
            r'exe_type not found in the module: exe_type == sequentials'
        ):
            execute_pipeline(
                'test.cli.test_action', 'mock_build_pipeline', 'sequentials'
            )
