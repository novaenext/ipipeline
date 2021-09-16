from pathlib import Path

from ipipeline.exceptions import SystemError


def create_directory(
    path: str, missing: bool = False, suppressed: bool = False
) -> None:
    try:
        Path(path).resolve().mkdir(parents=missing, exist_ok=suppressed)
    except (FileNotFoundError, FileExistsError) as error:
        raise SystemError(
            'directory not created', f'path == {path}'
        ) from error
