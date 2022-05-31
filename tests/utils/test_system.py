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
            SystemError, r'path was found in the file system: path == *'
        ):
            build_directory(str(self._path), exist_ok=False)

    def test_build_directory__path_ne_dir_wi_comps(self) -> None:
        build_directory(str(self._path))

        self.assertTrue(self._path.exists())

    def test_build_directory__path_ne_dir_wo_comps(self) -> None:
        with self.assertRaisesRegex(
            SystemError, r'path was not found in the file system: path == *'
        ):
            build_directory(str(self._path / 'mock_dir'))


class TestBuildFile(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_file'

    def tearDown(self) -> None:
        if self._path.exists():
            self._path.unlink()

    def test_build_file__path_eq_file_wi_comps(self) -> None:
        build_file(str(self._path))

        with self.assertRaisesRegex(
            SystemError, r'path was found in the file system: path == *'
        ):
            build_file(str(self._path), exist_ok=False)

    def test_build_file__path_ne_file_wi_comps(self) -> None:
        build_file(str(self._path))

        self.assertTrue(self._path.exists())

    def test_build_file__path_ne_file_wo_comps(self) -> None:
        with self.assertRaisesRegex(
            SystemError, r'path was not found in the file system: path == *'
        ):
            build_file(str(self._path / 'mock_file'))
