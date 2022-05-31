"""Functions related to the system procedures.

These functions act as a wrapper for the pathlib package, exposing 
only the necessary parameters and performing some common operations.
"""

from pathlib import Path

from ipipeline.exceptions import SystemError


def build_directory(path: str, **key_args: dict) -> None:
    """Builds a directory in the file system.

    The path is handled according to the underlying operating system.

    Parameters
    ----------
    path : str
        Path of the directory.
    key_args : dict
        Key arguments of the mkdir method.

    Raises
    ------
    SystemError
        Informs that the path was found in the file system.
    SystemError
        Informs that the path was not found in the file system.
    """

    try:
        path = Path(path).resolve()
        path.mkdir(**key_args)
    except FileExistsError as error:
        raise SystemError(
            'path found in the file system', [f'path == {path}']
        ) from error
    except FileNotFoundError as error:
        raise SystemError(
            'path not found in the file system', [f'path == {path}']
        ) from error


def build_file(path: str, **key_args: dict) -> None:
    """Builds a file in the file system.

    The path is handled according to the underlying operating system.

    Parameters
    ----------
    path : str
        Path of the file.
    key_args : dict
        Key arguments of the touch method.

    Raises
    ------
    SystemError
        Informs that the path was found in the file system.
    SystemError
        Informs that the path was not found in the file system.
    """

    try:
        path = Path(path).resolve()
        path.touch(**key_args)
    except FileExistsError as error:
        raise SystemError(
            'path found in the file system', [f'path == {path}']
        ) from error
    except FileNotFoundError as error:
        raise SystemError(
            'path not found in the file system', [f'path == {path}']
        ) from error
