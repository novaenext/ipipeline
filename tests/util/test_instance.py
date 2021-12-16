from unittest import TestCase

from ipipeline.exception import InstanceError
from ipipeline.util.instance import check_none_arg, build_repr, obtain_instance


class TestCheckNoneArg(TestCase):
    def test_arg_with_none(self) -> None:
        arg = check_none_arg(None, 'a1')

        self.assertEqual(arg, 'a1')

    def test_arg_without_none(self) -> None:
        arg = check_none_arg('a1', 'a2')

        self.assertEqual(arg, 'a1')


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
    def test_with_params_with_attrs(self) -> None:
        repr = build_repr(MockClass1(1))

        self.assertEqual(repr, 'MockClass1(param1=1, param2=\'2\')')

    def test_with_params_without_attrs(self) -> None:
        repr = build_repr(MockClass2(1))

        self.assertEqual(repr, 'MockClass2(param1=None, param2=None)')

    def test_without_params_with_attrs(self) -> None:
        repr = build_repr(MockClass3())

        self.assertEqual(repr, 'MockClass3()')

    def test_without_params_without_attrs(self) -> None:
        repr = build_repr(MockClass4())

        self.assertEqual(repr, 'MockClass4()')


class TestObtainInstance(TestCase):
    def test_valid_names(self) -> None:
        instance = obtain_instance('tests.util.test_instance', 'MockClass1')

        self.assertEqual(instance.__name__, 'MockClass1')

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
