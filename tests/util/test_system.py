from pathlib import Path
from unittest import TestCase

from ipipeline.exception import SystemError
from ipipeline.util.system import create_directory, create_file


class TestCreateDirectory(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_dir'

    def tearDown(self) -> None:
        self._path.rmdir()

    def test_inexistent_directory(self) -> None:
        create_directory(str(self._path))

        self.assertTrue(self._path.exists())

    def test_existent_directory(self) -> None:
        create_directory(str(self._path))

        with self.assertRaisesRegex(
            SystemError, r'directory not created in the file system: path == *'
        ):
            create_directory(str(self._path))


class TestCreateFile(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock_file'

    def tearDown(self) -> None:
        self._path.unlink()

    def test_inexistent_file(self) -> None:
        create_file(str(self._path))

        self.assertTrue(self._path.exists())

    def test_existent_file(self) -> None:
        create_file(str(self._path))

        with self.assertRaisesRegex(
            SystemError, r'file not created in the file system: path == *'
        ):
            create_file(str(self._path))