import json
from logging.config import dictConfig
from pathlib import Path

from .system import check_inexistent_path
from ..exceptions import RecordError


def config_log_json(
    config_path: str, config_name: str, log_path: str = '', log_name: str = ''
) -> None:
    check_inexistent_path(f'{config_path}/{config_name}')

    with open(Path(f'{config_path}/{config_name}')) as json_file:
        try:
            config = json.load(json_file)

            for handler_config in config.get('handlers', {}).values():
                if 'FileHandler' in handler_config.get('class', ''):
                    handler_config['filename'] = Path(f'{log_path}/{log_name}')

            dictConfig(config)
        except Exception as error:
            raise RecordError(
                'logging not configured', f'config_name == {config_name}'
            ) from error
