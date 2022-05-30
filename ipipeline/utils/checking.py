"""Functions related to the checking procedures."""

from typing import Any


def check_none(item: Any, default: Any) -> Any:
    """Checks if an item is None.

    Parameters
    ----------
    item : Any
        Item.
    default : Any
        Default to assign in case the item is None.

    Returns
    -------
    item : Any
        Item.
    """

    if item is None:
        item = default

    return item
