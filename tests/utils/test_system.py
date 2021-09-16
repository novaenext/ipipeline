from pathlib import Path
from unittest import TestCase

from ipipeline.exceptions import SystemError
from ipipeline.utils.system import create_directory


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
