from unittest import TestCase

from ipipeline.utils.checking import check_none


class TestCheckNone(TestCase):
    def test_check_none__item_eq_none(self) -> None:
        item = check_none(None, 'i1')

        self.assertEqual(item, 'i1')

    def test_check_none__item_ne_none(self) -> None:
        item = check_none('i1', 'i2')

        self.assertEqual(item, 'i1')
