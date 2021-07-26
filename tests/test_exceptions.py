from unittest import TestCase

from ipipeline.exceptions import BaseError


class TestBaseError(TestCase):
    def test_init_valid_args(self) -> None:
        error = BaseError('error found', 'error == value')

        self.assertEqual(error._descr, 'error found')
        self.assertEqual(error._detail, 'error == value')

    def test_str(self) -> None:
        error = BaseError('error found', 'error == value')
        error_str = error.__str__()

        self.assertEqual(error_str, 'error found: error == value')
