from pathlib import Path
from unittest import TestCase

from ipipeline.exceptions import SystemError
from ipipeline.utils.system import build_directory, build_file


class TestBuildDirectory(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_dir'

    def tearDown(self) -> None:
        if self._path.exists():
            self._path.rmdir()

    def test_build_directory__path_eq_dir_wi_comps(self) -> None:
        build_directory(str(self._path))

        with self.assertRaisesRegex(
            SystemError, r'path found in the file system: path == *'
        ):
            build_directory(str(self._path))

    def test_build_directory__path_ne_dir_wi_comps(self) -> None:
        build_directory(str(self._path))

        self.assertTrue(self._path.exists())

    def test_build_directory__path_ne_dir_wo_comps(self) -> None:
        with self.assertRaisesRegex(
            SystemError, r'path not found in the file system: path == *'
        ):
            build_directory(str(self._path / 'mock_dir'))


class TestBuildFile(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_file'

    def tearDown(self) -> None:
        self._path.unlink()

    def test_inexistent_file(self) -> None:
        build_file(str(self._path), suppressed=False)

        self.assertTrue(self._path.exists())

    def test_existent_file(self) -> None:
        build_file(str(self._path), suppressed=False)

        with self.assertRaisesRegex(
            SystemError, r'file not created in the file system: path == *'
        ):
            build_file(str(self._path), suppressed=False)
