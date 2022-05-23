from unittest import TestCase
from typing import List

from ipipeline.exceptions import InstanceError
from ipipeline.utils.instance import build_repr, obtain_mod_inst


class MockClass1:
    def __init__(
        self, 
        param1: int, 
        param2: str, 
        param3: List[int] = [3], 
        param4: List[str] = ['4']
    ) -> None:
        self._param1 = param1
        self._param2 = param2
        self.param3 = param3
        self.param4 = param4


class MockClass2:
    def __init__(
        self, 
        param1: int, 
        param2: str, 
        param3: List[int] = [3], 
        param4: List[str] = ['4']
    ) -> None:
        pass


class MockClass3:
    def __init__(self) -> None:
        self._param1 = 1
        self._param2 = '2'
        self.param3 = [3]
        self.param4 = ['4']


class MockClass4:
    def __init__(self) -> None:
        pass


class TestBuildRepr(TestCase):
    def test_build_repr__inst_wi_params_wi_attrs(self) -> None:
        repr = build_repr(MockClass1(1, '2'))

        self.assertEqual(
            repr, 
            'MockClass1(param1=1, param2=\'2\', param3=[3], param4=[\'4\'])'
        )

    def test_build_repr__inst_wi_params_wo_attrs(self) -> None:
        repr = build_repr(MockClass2(1, '2'))

        self.assertEqual(
            repr, 
            'MockClass2(param1=None, param2=None, param3=None, param4=None)'
        )

    def test_build_repr__inst_wo_params_wi_attrs(self) -> None:
        repr = build_repr(MockClass3())

        self.assertEqual(repr, 'MockClass3()')

    def test_build_repr__inst_wo_params_wo_attrs(self) -> None:
        repr = build_repr(MockClass4())

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
