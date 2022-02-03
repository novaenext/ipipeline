from unittest import TestCase

from ipipeline.exceptions import InstanceError
from ipipeline.utils.instance import (
    check_none_arg, build_inst_repr, obtain_mod_inst
)


class TestCheckNoneArg(TestCase):
    def test_none_arg(self) -> None:
        arg = check_none_arg(None, 'a1')

        self.assertEqual(arg, 'a1')

    def test_str_arg(self) -> None:
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


class TestBuildInstRepr(TestCase):
    def test_inst_with_params_with_attrs(self) -> None:
        repr = build_inst_repr(MockClass1(1))

        self.assertEqual(repr, 'MockClass1(param1=1, param2=\'2\')')

    def test_inst_with_params_without_attrs(self) -> None:
        repr = build_inst_repr(MockClass2(1))

        self.assertEqual(repr, 'MockClass2(param1=None, param2=None)')

    def test_inst_without_params_with_attrs(self) -> None:
        repr = build_inst_repr(MockClass3())

        self.assertEqual(repr, 'MockClass3()')

    def test_inst_without_params_without_attrs(self) -> None:
        repr = build_inst_repr(MockClass4())

        self.assertEqual(repr, 'MockClass4()')


class TestObtainModInst(TestCase):
    def test_valid_names(self) -> None:
        instance = obtain_mod_inst('tests.utils.test_instance', 'MockClass1')

        self.assertEqual(instance.__name__, 'MockClass1')

    def test_invalid_mod_name(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'inst_name not found in the module: inst_name == MockClass1'
        ):
            _ = obtain_mod_inst('tests.utils.test_instances', 'MockClass1')

    def test_invalid_inst_name(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'inst_name not found in the module: inst_name == MockClass11'
        ):
            _ = obtain_mod_inst('tests.utils.test_instance', 'MockClass11')
