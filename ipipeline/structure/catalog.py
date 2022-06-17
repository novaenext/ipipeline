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
            ID of the item obtained from the node outputs.

        Returns
        -------
        checked : bool
            Indicates if an item exists or not.
        """

        return id in self._items.keys()

    def obtain_item(self, id: str) -> Any:
        """Obtains an item.

        Parameters
        ----------
        id : str
            ID of the item obtained from the node outputs.

        Returns
        -------
        item : Any
            Item obtained from the node returns.

        Raises
        ------
        CatalogError
            Informs that the id was not found in the _items.
        """

        try:
            return self._items[id]
        except KeyError as error:
            raise CatalogError(
                'id not found in the _items', [f'id == {id}']
            ) from error

    def add_item(self, id: str, item: Any) -> None:
        """Adds an item.

        If the item does not exist, a new one is added, otherwise the existing 
        one is updated.

        Parameters
        ----------
        id : str
            ID of the item obtained from the node outputs.
        item : Any
            Item obtained from the node returns.
        """

        self._items[id] = item

    def remove_item(self, id: str) -> None:
        """Removes an item.

        Parameters
        ----------
        id : str
            ID of the item obtained from the node outputs.

        Raises
        ------
        CatalogError
            Informs that the id was not found in the _items.
        """

        try:
            del self._items[id]
        except KeyError as error:
            raise CatalogError(
                'id not found in the _items', [f'id == {id}']
            ) from error

    def remove_items(self) -> None:
        """Remove the items."""

        self._items.clear()
