from pathlib import Path
from unittest import TestCase

from ipipeline.exceptions import SystemError
from ipipeline.utils.system import create_directory, create_file


class TestCreateDirectory(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).parents[0] / 'mock_dir'

    def test_inexistent_directory(self) -> None:
        create_directory(str(self._path))

        self.assertTrue(self._path.exists())
        self._path.rmdir()

    def test_existent_directory(self) -> None:
        create_directory(str(self._path))

        with self.assertRaisesRegex(
            SystemError, r'directory not created: path == *'
        ):
            create_directory(str(self._path))
        self._path.rmdir()


class TestCreateFile(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).parents[0] / 'mock_file'

    def test_inexistent_file(self) -> None:
        create_file(str(self._path))

        self.assertTrue(self._path.exists())
        self._path.unlink()

    def test_existent_file(self) -> None:
        create_file(str(self._path))

        with self.assertRaisesRegex(
            SystemError, r'file not created: path == *'
        ):
            create_file(str(self._path))
        self._path.unlink()
