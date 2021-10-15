from argparse import ArgumentParser
from unittest import TestCase
from unittest.mock import Mock

from ipipeline.cli.parsing import create_parser, _add_pos_args, _add_opt_args


class TestCreateParser(TestCase):
    def setUp(self) -> None:
        help_arg = Mock(spec=['name', 'descr', 'action', 'type', 'key_args'])
        help_arg.name = 'help'
        help_arg.descr = 'help descr'
        help_arg.action = 'help'
        help_arg.type = None
        help_arg.key_args = {}
        self._mock_cmds = []

        for name, descr, action, pos_args, opt_args, key_args in [
            ['root_cmd', 'root_cmd descr', None, [], [help_arg], {}], 
            ['sub_cmd', 'sub_cmd descr', None, [], [help_arg], {}]
        ]:
            mock_cmd = Mock(spec=[
                'name', 'descr', 'action', 'pos_args', 'opt_args', 'key_args'
            ])
            mock_cmd.name = name
            mock_cmd.descr = descr
            mock_cmd.action = action
            mock_cmd.pos_args = pos_args
            mock_cmd.opt_args = opt_args
            mock_cmd.key_args = key_args
            self._mock_cmds.append(mock_cmd)

    def test_valid_cmds(self) -> None:
        parser = create_parser(*self._mock_cmds)

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['sub_cmd', '-h'])

    def test_invalid_cmds(self) -> None:
        parser = create_parser(*self._mock_cmds)

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['sub_cmd', '-i'])


class TestAddPosArgs(TestCase):
    def setUp(self) -> None:
        self._mock_pos_args = []

        for name, descr, action, type, key_args in [
            ['arg1', 'arg1 descr', 'store', str, {}], 
            ['arg2', 'arg2 descr', 'store', int, {}]
        ]:
            mock_pos_arg = Mock(
                spec=['name', 'descr', 'action', 'type', 'key_args']
            )
            mock_pos_arg.name = name
            mock_pos_arg.descr = descr
            mock_pos_arg.action = action
            mock_pos_arg.type = type
            mock_pos_arg.key_args = key_args
            self._mock_pos_args.append(mock_pos_arg)

    def test_valid_args(self) -> None:
        parser = ArgumentParser()
        _add_pos_args(parser, self._mock_pos_args)
        args = parser.parse_args(args=['7', '3'])

        self.assertEqual(args.arg1, '7')
        self.assertEqual(args.arg2, 3)

    def test_invalid_args(self) -> None:
        parser = ArgumentParser()
        _add_pos_args(parser, self._mock_pos_args)

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(args=['7', '3', '0'])


class TestAddOptArgs(TestCase):
    def setUp(self) -> None:
        self._mock_opt_args = []

        for name, descr, action, type, key_args in [
            ['help', 'help descr', 'help', None, {}]
        ]:
            mock_opt_arg = Mock(
                spec=['name', 'descr', 'action', 'type', 'key_args']
            )
            mock_opt_arg.name = name
            mock_opt_arg.descr = descr
            mock_opt_arg.action = action
            mock_opt_arg.type = type
            mock_opt_arg.key_args = key_args
            self._mock_opt_args.append(mock_opt_arg)

    def test_valid_args(self) -> None:
        parser = ArgumentParser(add_help=False)
        _add_opt_args(parser, self._mock_opt_args)

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['-h'])

        with self.assertRaisesRegex(SystemExit, r'0'):
            _ = parser.parse_args(['--help'])

    def test_invalid_args(self) -> None:
        parser = ArgumentParser(add_help=False)
        _add_opt_args(parser, self._mock_opt_args)

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['-i'])

        with self.assertRaisesRegex(SystemExit, r'2'):
            _ = parser.parse_args(['--invalid'])
