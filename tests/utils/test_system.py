from pathlib import Path
from unittest import TestCase

from ipipeline.exceptions import SystemError
from ipipeline.utils.system import build_directory, build_file


class TestBuildDirectory(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_dir'

    def tearDown(self) -> None:
        self._path.rmdir()

    def test_inexistent_directory(self) -> None:
        build_directory(str(self._path), missing=False, suppressed=False)

        self.assertTrue(self._path.exists())

    def test_existent_directory(self) -> None:
        build_directory(str(self._path), missing=False, suppressed=False)

        with self.assertRaisesRegex(
            SystemError, r'directory not created in the file system: path == *'
        ):
            build_directory(str(self._path), missing=False, suppressed=False)


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
