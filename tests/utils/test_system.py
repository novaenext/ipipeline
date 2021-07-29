from unittest import TestCase

from ipipeline.exceptions import SystemError
from ipipeline.utils.system import check_inexistent_path


class TestCheckInexistentPath(TestCase):
    def test_inexistent_path(self) -> None:
        with self.assertRaisesRegex(
            SystemError, r'inexistent path found: path == \./inexistent'
        ):
            check_inexistent_path('./inexistent')

    def test_existent_path(self) -> None:
        check_inexistent_path('./ipipeline')

        self.assertTrue(True)