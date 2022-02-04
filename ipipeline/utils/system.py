"""Functions related to the system procedures.

These functions act as a wrapper for the pathlib package, exposing 
only the necessary parameters and performing some common operations.
"""

from pathlib import Path

from ipipeline.exceptions import SystemError


def create_directory(
    path: str, missing: bool = False, suppressed: bool = False
) -> None:
    """Creates a directory in the file system.

    The path format is handled according to the underlying operating system.

    Parameters
    ----------
    path : str
        Path of the directory.
    missing : bool, default=False
        Indicates if the missing parent directories should be created.
    suppressed : bool, default=False
        Indicates if the error should be suppressed or not.

    Raises
    ------
    SystemError
        Informs that the directory was not created in the file system.
    """

    try:
        path = Path(path).resolve()
        path.mkdir(parents=missing, exist_ok=suppressed)
    except (FileExistsError, FileNotFoundError) as error:
        raise SystemError(
            'directory not created in the file system', f'path == {path}'
        ) from error


def create_file(path: str, suppressed: bool = False) -> None:
    """Creates a file in the file system.

    The path format is handled according to the underlying operating system.

    Parameters
    ----------
    path : str
        Path of the file.
    suppressed : bool, default=False
        Indicates if the error should be suppressed or not.

    Raises
    ------
    SystemError
        Informs that the file was not created in the file system.
    """

    try:
        path = Path(path).resolve()
        path.touch(exist_ok=suppressed)
    except (FileExistsError, FileNotFoundError) as error:
        raise SystemError(
            'file not created in the file system', f'path == {path}'
        ) from error
