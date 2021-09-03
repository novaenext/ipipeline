from unittest import TestCase

from ipipeline.exceptions import BaseError


class TestBaseError(TestCase):
    def test_init(self) -> None:
        error = BaseError('error msg', 'error == value')

        self.assertEqual(error._descr, 'error msg')
        self.assertEqual(error._detail, 'error == value')

    def test_str(self) -> None:
        error = BaseError('error msg', 'error == value')
        error_str = error.__str__()

        self.assertEqual(error_str, 'error msg: error == value')
