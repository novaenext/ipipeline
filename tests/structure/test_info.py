from unittest import TestCase

from ipipeline.exceptions import InfoError
from ipipeline.structure.info import Info


class TestInfo(TestCase):
    def test_init__args_eq_types(self) -> None:
        info = Info('i1', tags=['t1', 't2'])

        self.assertEqual(info._id, 'i1')
        self.assertListEqual(info._tags, ['t1', 't2'])

    def test_get__args_eq_types(self) -> None:
        info = Info('i1', tags=['t1', 't2'])

        self.assertEqual(info.id, 'i1')
        self.assertListEqual(info.tags, ['t1', 't2'])

    def test_set__args_eq_types(self) -> None:
        info = Info('i1', tags=['t1', 't2'])
        info.id = 'i2'
        info.tags = ['t3', 't4']

        self.assertEqual(info.id, 'i2')
        self.assertListEqual(info.tags, ['t3', 't4'])

    def test_check_id__id_eq_pattern(self) -> None:
        info = Info('i1')
        id = info._check_id('i1_-.')

        self.assertEqual(id, 'i1_-.')

    def test_check_id__id_ne_pattern(self) -> None:
        info = Info('i1')

        with self.assertRaisesRegex(
            InfoError, r'id did not match the pattern: id == i1!'
        ):
            _ = info._check_id('i1!')

    def test_check_id__id_eq_empty(self) -> None:
        info = Info('i1')

        with self.assertRaisesRegex(
            InfoError, r'id did not match the pattern: id == '
        ):
            _ = info._check_id('')

    def test_check_id__id_eq_none(self) -> None:
        info = Info('i1')

        with self.assertRaisesRegex(
            InfoError, r'id did not match the pattern: id == None'
        ):
            _ = info._check_id(None)

    def test_repr(self) -> None:
        info = Info('i1', tags=['t1', 't2'])
        repr = info.__repr__()

        self.assertEqual(repr, 'Info(id=\'i1\', tags=[\'t1\', \'t2\'])')
