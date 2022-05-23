from unittest import TestCase

from ipipeline.utils.checking import check_none


class TestCheckNone(TestCase):
    def test_check_none__data_eq_none(self) -> None:
        data = check_none(None, 'd1')

        self.assertEqual(data, 'd1')

    def test_check_none__data_ne_none(self) -> None:
        data = check_none('d1', 'd2')

        self.assertEqual(data, 'd1')
