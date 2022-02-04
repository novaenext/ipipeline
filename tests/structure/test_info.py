from unittest import TestCase

from ipipeline.exceptions import InfoError
from ipipeline.structure.info import Info


class TestInfo(TestCase):
    def test_init(self) -> None:
        info = Info('i1', tags=['t1', 't2'])

        self.assertEqual(info.id, 'i1')
        self.assertListEqual(info.tags, ['t1', 't2'])

    def test_defaults(self) -> None:
        info1 = Info('i1')
        info2 = Info('i2')

        self.assertIsNot(info1.tags, info2.tags)

    def test_check_valid_id(self) -> None:
        info = Info('i1', tags=None)
        id = info._check_valid_id('i1')

        self.assertEqual(id, 'i1')

    def test_check_invalid_id(self) -> None:
        info = Info('i1', tags=None)

        with self.assertRaisesRegex(
            InfoError, 
            r'id not validated according to the pattern \(letters, '
            r'digits, underscores and/or dashes\): id == i\.1'
        ):
            _ = info._check_valid_id('i.1')

    def test_repr(self) -> None:
        info = Info('i1', tags=['t1', 't2'])
        repr = info.__repr__()

        self.assertEqual(
            repr, 'Info(id=\'i1\', tags=[\'t1\', \'t2\'])'
        )
