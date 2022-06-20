"""Class related to the catalog procedures."""

from typing import Any, Dict, List

from ipipeline.exceptions import CatalogError
from ipipeline.structure.info import Info
from ipipeline.utils.checking import check_none


class Catalog(Info):
    """Stores the items of an execution.

    Attributes
    ----------
    _id : str
        ID of the catalog.
    _items : Dict[str, Any]
        Items of an execution. The keys are the task outputs and the 
        values are the task returns.
    _tags : List[str]
        Tags of the catalog to provide more context.
    """

    def __init__(
        self, id: str, items: Dict[str, Any] = None, tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the catalog.
        items : Dict[str, Any], optional
            Items of an execution. The keys are the task outputs and the 
            values are the task returns.
        tags : List[str], optional
            Tags of the catalog to provide more context.

        Raises
        ------
        InfoError
            Informs that the id did not match the pattern.
        """

        super().__init__(id, tags=tags)

        self._items = check_none(items, {})

    @property
    def items(self) -> Dict[str, Any]:
        """Gets the _items attribute.

        Returns
        -------
        items : Dict[str, Any]
            Items of an execution. The keys are the task outputs and the 
            values are the task returns.
        """

        return self._items

    @items.setter
    def items(self, items: Dict[str, Any]) -> None:
        """Sets the _items attribute.

        Parameters
        ----------
        items : Dict[str, Any]
            Items of an execution. The keys are the task outputs and the 
            values are the task returns.
        """

        self._items = items

    def check_item(self, id: str) -> bool:
        """Checks if an item exists.

        Parameters
        ----------
        id : str
            ID of the item.

        Returns
        -------
        checked : bool
            Flag that indicates if an item exists.
        """

        checked = id in self._items.keys()

        return checked

    def get_item(self, id: str) -> Any:
        """Gets an item.

        Parameters
        ----------
        id : str
            ID of the item.

        Returns
        -------
        item : Any
            Item of an execution.

        Raises
        ------
        CatalogError
            Informs that the id was not found in the _items.
        """

        try:
            item = self._items[id]

            return item
        except KeyError as error:
            raise CatalogError(
                'id was not found in the _items', [f'id == {id}']
            ) from error

    def set_item(self, id: str, item: Any) -> None:
        """Sets an item.

        Parameters
        ----------
        id : str
            ID of the item.
        item : Any
            Item of an execution.
        """

        self._items[id] = item

    def delete_item(self, id: str) -> None:
        """Deletes an item.

        Parameters
        ----------
        id : str
            ID of the item.

        Raises
        ------
        CatalogError
            Informs that the id was not found in the _items.
        """

        try:
            del self._items[id]
        except KeyError as error:
            raise CatalogError(
                'id was not found in the _items', [f'id == {id}']
            ) from error
