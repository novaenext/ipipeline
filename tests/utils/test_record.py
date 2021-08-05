import logging
from pathlib import Path
from unittest import TestCase

from ipipeline.exceptions import RecordError
from ipipeline.utils.record import config_log_json


class TestConfigLogJson(TestCase):
    def setUp(self) -> None:
        self._path = Path(__file__).parents[0] / 'data'

    def test_config_with_file_handler(self) -> None:
        config_log_json(
            str(self._path), 
            'logging_with_file_handler.json',
            str(self._path),
            'test.log'
        )
        logging.info('test_valid_config_with_file_handler')
        log_path = self._path / 'test.log'

        self.assertTrue(log_path.exists())
        log_path.unlink()

    def test_config_with_stream_handler(self) -> None:
        config_log_json(str(self._path), 'logging_with_stream_handler.json')
        logging.info('test_valid_config_with_stream_handler')

        self.assertTrue(True)

    def test_config_without_version(self) -> None:
        with self.assertRaisesRegex(
            RecordError, 
            r'logging not configured: config_name == '
            r'logging_without_version\.json'
        ):
            config_log_json(str(self._path), 'logging_without_version.json')
