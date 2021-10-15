from unittest import TestCase

from ipipeline.cli.command import BaseCommand, Command


class TestBaseCommand(TestCase):
    def test_init(self) -> None:
        base_cmd = BaseCommand('c1', 'cmd descr', None, [], [], param1=7)

        self.assertEqual(base_cmd.name, 'c1')
        self.assertEqual(base_cmd.descr, 'cmd descr')
        self.assertEqual(base_cmd.action, None)
        self.assertListEqual(base_cmd.pos_args, [])
        self.assertListEqual(base_cmd.opt_args, [])
        self.assertDictEqual(base_cmd.key_args, {'param1': 7})


class TestCommand(TestCase):
    def test_deriv(self) -> None:
        cmd = Command('c1', 'cmd descr', None, [], [])

        self.assertIsInstance(cmd, BaseCommand)
