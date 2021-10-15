from unittest import TestCase

from ipipeline.cli.argument import BaseArgument, Argument


class TestBaseArgument(TestCase):
    def test_init(self) -> None:
        base_arg = BaseArgument('a1', 'arg descr', 'store', str, param1=7)

        self.assertEqual(base_arg.name, 'a1')
        self.assertEqual(base_arg.descr, 'arg descr')
        self.assertEqual(base_arg.action, 'store')
        self.assertEqual(base_arg.type, str)
        self.assertDictEqual(base_arg.key_args, {'param1': 7})


class TestArgument(TestCase):
    def test_deriv(self) -> None:
        arg = Argument('a1', 'arg descr', 'store', str)

        self.assertIsInstance(arg, BaseArgument)
