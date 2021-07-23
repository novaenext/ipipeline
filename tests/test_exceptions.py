from unittest import TestCase

from ipipeline.exceptions import BaseError


class TestBaseError(TestCase):
    def test_valid_instance(self) -> None:
        error = BaseError('error found', 'error == value')

        self.assertEqual(error._descr, 'error found')
        self.assertEqual(error._detail, 'error == value')

    def test_str_repr(self) -> None:
        error = BaseError('error found', 'error == value')

        self.assertEqual(error.__str__(), 'error found: error == value')
