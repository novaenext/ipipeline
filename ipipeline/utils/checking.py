"""Functions related to the checking procedures."""

from typing import Any


def check_none(data: Any, default: Any) -> Any:
    """Checks if the data is None.

    Parameters
    ----------
    data : Any
        Data.
    default : Any
        Default value to assign to the data in case it is None.

    Returns
    -------
    data : Any
        Data with its original or default value.
    """

    if data is None:
        data = default

    return data
