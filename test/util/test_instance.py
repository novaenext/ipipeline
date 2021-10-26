from unittest import TestCase

from ipipeline.exception import InstanceError
from ipipeline.util.instance import Identification, build_instance_repr


class TestIdentification(TestCase):
    def test_init(self) -> None:
        identifier = Identification('i1', tags=['t1', 't2'])

        self.assertEqual(identifier.id, 'i1')
        self.assertListEqual(identifier.tags, ['t1', 't2'])

    def test_check_valid_id(self) -> None:
        id = Identification._check_valid_id(None, 'i1')

        self.assertEqual(id, 'i1')

    def test_check_invalid_id(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id not validated according to the pattern \(letters, '
            r'digits, underscores and/or dashes\): id == i\.1'
        ):
            _ = Identification._check_valid_id(None, 'i.1')

    def test_repr(self) -> None:
        identifier = Identification('i1', tags=['t1', 't2'])
        instance_repr = identifier.__repr__()

        self.assertEqual(
            instance_repr, 
            'Identification(id=\'i1\', tags=[\'t1\', \'t2\'])'
        )


class MockClass1:
    def __init__(self, param1: int, param2: str = '2') -> None:
        self._param1 = param1
        self.param2 = param2


class MockClass2:
    def __init__(self, param1: int, param2: str = '2') -> None:
        pass


class MockClass3:
    def __init__(self) -> None:
        self._param1 = 1
        self.param2 = '2'


class MockClass4:
    def __init__(self) -> None:
        pass


class TestBuildInstanceRepr(TestCase):
    def test_instance_with_params_with_attrs(self) -> None:
        instance_repr = build_instance_repr(MockClass1(1))

        self.assertEqual(instance_repr, 'MockClass1(param1=1, param2=\'2\')')

    def test_instance_with_params_without_attrs(self) -> None:
        instance_repr = build_instance_repr(MockClass2(1))

        self.assertEqual(instance_repr, 'MockClass2(param1=None, param2=None)')

    def test_instance_without_params_with_attrs(self) -> None:
        instance_repr = build_instance_repr(MockClass3())

        self.assertEqual(instance_repr, 'MockClass3()')

    def test_instance_without_params_without_attrs(self) -> None:
        instance_repr = build_instance_repr(MockClass4())

        self.assertEqual(instance_repr, 'MockClass4()')
