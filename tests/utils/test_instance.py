from unittest import TestCase

from ipipeline.exceptions import InstanceError
from ipipeline.utils.instance import create_instance_repr, InstanceIdentifier


class MockClass1:
    def __init__(
        self, 
        param1_: int, 
        param2_: str, 
        param3_: int = 3, 
        param4_: str = '4'
    ) -> None:
        self._param1_ = param1_
        self.param2_ = param2_
        self._param3 = param3_
        self.param4 = param4_


class MockClass2:
    def __init__(self, param1: int, param2: str) -> None:
        pass


class MockClass3:
    def __init__(self) -> None:
        self._param1 = 1
        self._param2 = '2'


class MockClass4:
    def __init__(self) -> None:
        pass


class TestCreateInstanceRepr(TestCase):
    def test_instance_with_params_with_attrs(self) -> None:
        instance_repr = create_instance_repr(MockClass1(1, '2'))

        self.assertEqual(
            instance_repr, 
            'MockClass1(param1_=1, param2_=\'2\', param3_=3, param4_=\'4\')'
        )

    def test_instance_with_params_without_attrs(self) -> None:
        instance_repr = create_instance_repr(MockClass2(1, '2'))

        self.assertEqual(instance_repr, 'MockClass2(param1=None, param2=None)')

    def test_instance_without_params_with_attrs(self) -> None:
        instance_repr = create_instance_repr(MockClass3())

        self.assertEqual(instance_repr, 'MockClass3()')

    def test_instance_without_params_without_attrs(self) -> None:
        instance_repr = create_instance_repr(MockClass4())

        self.assertEqual(instance_repr, 'MockClass4()')


class TestInstanceIdentifier(TestCase):
    def test_init(self) -> None:
        identifier = InstanceIdentifier('i1', tags=['t1', 't2'])

        self.assertEqual(identifier.id, 'i1')
        self.assertListEqual(identifier.tags, ['t1', 't2'])

    def test_check_valid_id_valid_id(self) -> None:
        id_ = InstanceIdentifier._check_valid_id(None, 'i1')

        self.assertEqual(id_, 'i1')

    def test_check_valid_id_invalid_id(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(letters, digits, underscore '
            r'and/or dash\): id_ == i\.1'
        ):
            _ = InstanceIdentifier._check_valid_id(None, 'i.1')
