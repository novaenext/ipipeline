from unittest import TestCase

from ipipeline.exceptions import BaseError


class TestBaseError(TestCase):
    def test_init__args_eq_types(self) -> None:
        error = BaseError('error text', ['cause == item'])

        self.assertEqual(error._text, 'error text')
        self.assertListEqual(error._causes, ['cause == item'])

    def test_str__text_eq_str__causes_eq_empty_cause(self) -> None:
        error = BaseError('error text', [])
        msg = error.__str__()

        self.assertEqual(msg, 'error text: ')

    def test_str__text_eq_str__causes_eq_single_cause(self) -> None:
        error = BaseError('error text', ['cause == item'])
        msg = error.__str__()

        self.assertEqual(msg, 'error text: cause == item')

    def test_str__text_eq_str__causes_eq_multiple_causes(self) -> None:
        error = BaseError('error text', ['cause1 == item1', 'cause2 == item2'])
        msg = error.__str__()

        self.assertEqual(msg, 'error text: cause1 == item1, cause2 == item2')
