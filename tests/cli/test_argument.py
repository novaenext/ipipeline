from unittest import TestCase

from ipipeline.cli.argument import Argument


class TestArgument(TestCase):
    def test_init(self) -> None:
        arg = Argument('a1', 'arg descr', 'store', str, param1=7)

        self.assertEqual(arg.name, 'a1')
        self.assertEqual(arg.descr, 'arg descr')
        self.assertEqual(arg.action, 'store')
        self.assertEqual(arg.type, str)
        self.assertDictEqual(arg.key_args, {'param1': 7})
