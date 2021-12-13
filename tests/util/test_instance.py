from unittest import TestCase

from ipipeline.exception import InstanceError
from ipipeline.util.instance import Identification, build_repr, obtain_instance


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
        repr = identifier.__repr__()

        self.assertEqual(
            repr, 'Identification(id=\'i1\', tags=[\'t1\', \'t2\'])'
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


class TestBuildRepr(TestCase):
    def test_instance_with_params_with_attrs(self) -> None:
        repr = build_repr(MockClass1(1))

        self.assertEqual(repr, 'MockClass1(param1=1, param2=\'2\')')

    def test_instance_with_params_without_attrs(self) -> None:
        repr = build_repr(MockClass2(1))

        self.assertEqual(repr, 'MockClass2(param1=None, param2=None)')

    def test_instance_without_params_with_attrs(self) -> None:
        repr = build_repr(MockClass3())

        self.assertEqual(repr, 'MockClass3()')

    def test_instance_without_params_without_attrs(self) -> None:
        repr = build_repr(MockClass4())

        self.assertEqual(repr, 'MockClass4()')


class TestObtainInstance(TestCase):
    def test_valid_names(self) -> None:
        mock_class = obtain_instance('tests.util.test_instance', 'MockClass1')

        self.assertEqual(mock_class.__name__, 'MockClass1')

    def test_invalid_mod_name(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'inst_name not found in the module: inst_name == MockClass1'
        ):
            _ = obtain_instance('tests.util.test_instances', 'MockClass1')

    def test_invalid_inst_name(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'inst_name not found in the module: inst_name == MockClass11'
        ):
            _ = obtain_instance('tests.util.test_instance', 'MockClass11')
