import sys
from unittest import TestCase
from typing import List

from ipipeline.exceptions import InstanceError
from ipipeline.utils.instance import build_repr, get_inst


class MockClass1:
    def __init__(
        self, 
        arg1: int, 
        arg2: str, 
        arg3: List[int] = [3], 
        arg4: List[str] = ['4']
    ) -> None:
        self._arg1 = arg1
        self._arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4


class MockClass2:
    def __init__(
        self, 
        arg1: int, 
        arg2: str, 
        arg3: List[int] = [3], 
        arg4: List[str] = ['4']
    ) -> None:
        pass


class MockClass3:
    def __init__(self) -> None:
        self._arg1 = 1
        self._arg2 = '2'
        self.arg3 = [3]
        self.arg4 = ['4']


class MockClass4:
    def __init__(self) -> None:
        pass


class TestBuildRepr(TestCase):
    def test_build_repr__inst_eq_mock_wi_args_wi_attrs(self) -> None:
        repr = build_repr(MockClass1(1, '2'))

        self.assertEqual(
            repr, 
            'MockClass1(arg1=1, arg2=\'2\', arg3=[3], arg4=[\'4\'])'
        )

    def test_build_repr__inst_eq_mock_wi_args_wo_attrs(self) -> None:
        repr = build_repr(MockClass2(1, '2'))

        self.assertEqual(
            repr, 
            'MockClass2(arg1=None, arg2=None, arg3=None, arg4=None)'
        )

    def test_build_repr__inst_eq_mock_wo_args_wi_attrs(self) -> None:
        repr = build_repr(MockClass3())

        self.assertEqual(repr, 'MockClass3()')

    def test_build_repr__inst_eq_mock_wo_args_wo_attrs(self) -> None:
        repr = build_repr(MockClass4())

        self.assertEqual(repr, 'MockClass4()')


class TestGetInst(TestCase):
    def test_get_inst__mod_name_eq_mod__inst_name_eq_inst(self) -> None:
        inst = get_inst('tests.utils.test_instance', 'MockClass1')

        self.assertEqual(inst.__name__, 'MockClass1')
        self.assertIn('ipipeline/tests', sys.path[-1])

    def test_get_inst__mod_name_ne_mod__inst_name_eq_inst(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'mod_name was not found in the package: '
            r'mod_name == tests.utils.test_instance'
        ):
            _ = get_inst('tests.utils.test_instances', 'MockClass1')

    def test_get_inst__mod_name_eq_mod__inst_name_ne_inst(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'inst_name was not found in the module: inst_name == MockClass0'
        ):
            _ = get_inst('tests.utils.test_instance', 'MockClass0')
