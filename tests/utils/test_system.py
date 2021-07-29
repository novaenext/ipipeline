from pathlib import Path
from unittest import TestCase

from ipipeline.exceptions import SystemError
from ipipeline.utils.system import check_inexistent_path, create_directory


class TestCheckInexistentPath(TestCase):
    def test_inexistent_path(self) -> None:
        with self.assertRaisesRegex(
            SystemError, r'inexistent path found: path == *'
        ):
            check_inexistent_path('./mock_dir')

    def test_existent_path(self) -> None:
        check_inexistent_path('./ipipeline')

        self.assertTrue(True)


class TestCreateDirectory(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).parents[0] / 'mock_dir'

    def test_inexistent_path(self) -> None:
        create_directory(str(self._path))

        self.assertTrue(self._path.exists())
        self._path.rmdir()

    def test_existent_path(self) -> None:
        create_directory(str(self._path))

        with self.assertRaisesRegex(
            SystemError, r'directory not created: path == *'
        ):
            create_directory(str(self._path))
        self._path.rmdir()