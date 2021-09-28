from pathlib import Path

from ipipeline.exceptions import SystemError


def create_directory(
    path: str, missing: bool = False, suppressed: bool = False
) -> None:
    try:
        path = Path(path).resolve()
        path.mkdir(parents=missing, exist_ok=suppressed)
    except (FileExistsError, FileNotFoundError) as error:
        raise SystemError(
            'directory not created in the file system', f'path == {path}'
        ) from error


def create_file(path: str, suppressed: bool = False) -> None:
    try:
        path = Path(path).resolve()
        path.touch(exist_ok=suppressed)
    except (FileExistsError, FileNotFoundError) as error:
        raise SystemError(
            'file not created in the file system', f'path == {path}'
        ) from error
