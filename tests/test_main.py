import sys
from pathlib import Path
from unittest import TestCase

from ipipeline.__main__ import main


class TestMain(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).resolve().parents[0] / 'mock'

    def test_exit_code0(self) -> None:
        sys.argv = ['__main__']

        with self.assertRaisesRegex(SystemExit, r'0'):
            main()

    def test_exit_code1(self) -> None:
        sys.argv = ['__main__', 'project', str(self._path.parents[0]), 'mock']
        self._path.mkdir()

        with self.assertRaisesRegex(SystemExit, r'1'):
            main()

        self._path.rmdir()

    def test_exit_code2(self) -> None:
        sys.argv = ['__main__', '--invalid']

        with self.assertRaisesRegex(SystemExit, r'2'):
            main()
