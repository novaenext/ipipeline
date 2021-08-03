from unittest import TestCase

from ipipeline.config.reference import BASE_PATH


class TestConstants(TestCase):
    def test_base_path(self) -> None:
        self.assertIn('ipipeline', BASE_PATH)
