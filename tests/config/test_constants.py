from unittest import TestCase

from ipipeline.config.constants import BASE_PATH


class TestConstants(TestCase):
    def test_base_path(self) -> None:
        self.assertEqual('ipipeline', BASE_PATH[-9:])
