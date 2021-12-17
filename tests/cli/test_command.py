from unittest import TestCase

from ipipeline.cli.command import Command


class TestCommand(TestCase):
    def test_init(self) -> None:
        cmd = Command('c1', 'cmd descr', None, [], [], param1=7)

        self.assertEqual(cmd.name, 'c1')
        self.assertEqual(cmd.descr, 'cmd descr')
        self.assertEqual(cmd.action, None)
        self.assertListEqual(cmd.pos_args, [])
        self.assertListEqual(cmd.opt_args, [])
        self.assertDictEqual(cmd.key_args, {'param1': 7})
