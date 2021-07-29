from pathlib import Path

from ..exceptions import SystemError


def check_inexistent_path(path: str) -> None:
    if not Path(path).exists():
        raise SystemError('inexistent path found', f'path == {path}')


def create_directory(
    path: str, parents: bool = False, suppressed: bool = False
) -> None:
    try:
        Path(path).mkdir(parents=parents, exist_ok=suppressed)
    except FileExistsError as error:
        raise SystemError(
            'directory not created', f'path == {path}'
        ) from error
