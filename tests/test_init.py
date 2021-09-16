from unittest import TestCase

from ipipeline.__init__ import __version__


class TestVersion(TestCase):
    def test_parts_qty(self) -> None:
        parts = __version__.split('.')

        self.assertEqual(len(parts), 3)
