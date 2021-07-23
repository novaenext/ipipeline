from unittest import TestCase

from ipipeline.exceptions import InstanceError
from ipipeline.utils.instance import InstanceIdentifier


class TestInstanceIdentifier(TestCase):
    def test_valid_instance(self) -> None:
        identifier = InstanceIdentifier('i1', tags=['t1', 't2'])

        self.assertEqual(identifier.id, 'i1')
        self.assertEqual(identifier.tags, ['t1', 't2'])

    def test_invalid_instance(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == i1,'
        ):
            _ = InstanceIdentifier('i1,', tags=['t1', 't2'])

    def test_check_id_valid_pattern(self) -> None:
        identifier = InstanceIdentifier('i1')
        id_ = identifier._check_id('i1')

        self.assertEqual(id_, 'i1')

    def test_check_id_invalid_pattern(self) -> None:
        identifier = InstanceIdentifier('i1')

        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == i1\.'
        ):
            _ = identifier._check_id('i1.')

    def test_check_id_empty_pattern(self) -> None:
        identifier = InstanceIdentifier('i1')

        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == '
        ):
            _ = identifier._check_id('')