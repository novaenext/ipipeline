from pathlib import Path

from ..exceptions import SystemError


def check_inexistent_path(path: str) -> None:
    if not Path(path).exists():
        raise SystemError('inexistent path found', f'path == {path}')
