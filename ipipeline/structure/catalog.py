"""Classes related to the catalog procedures."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ipipeline.exception import CatalogError
from ipipeline.util.instance import Identification


class BaseCatalog(ABC, Identification):
    """Provides an interface to the catalog classes.

    Attributes
    ----------
    _id : str
        ID of the catalog.
    _items : Dict[str, Any]
        Items obtained from the executions. The keys are the item IDs 
        obtained from the outputs and the values are the items obtained 
        from the returns.
    _tags : List[str]
        Tags of the catalog to provide more context.
    """

    def __init__(self, id: str, tags: List[str] = []) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the catalog.
        tags : List[str], default=[]
            Tags of the catalog to provide more context.

        Raises
        ------
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        self._items = {}

        super().__init__(id, tags=tags)

    @property
    def items(self) -> Dict[str, Any]:
        """Obtains the _items attribute.

        Returns
        -------
        items : Dict[str, Any]
            Items obtained from the executions. The keys are the item IDs 
            obtained from the outputs and the values are the items obtained 
            from the returns.
        """

        return self._items

    @abstractmethod
    def add_item(self, id: str, item: Any) -> None:
        """Provides an interface to add an item.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.
        item : Any
            Item obtained from the returns.
        """

        pass

    @abstractmethod
    def check_item(self, id: str) -> bool:
        """Provides an interface to check if an item exists.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.

        Returns
        -------
        checked : bool
            Indicates if an item exists.
        """

        pass

    @abstractmethod
    def obtain_item(self, id: str) -> Any:
        """Provides an interface to obtain an item.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.

        Returns
        -------
        item : Any
            Item obtained from the returns.
        """

        pass

    @abstractmethod
    def remove_item(self, id: str) -> None:
        """Provides an interface to remove an item.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.
        """

        pass

    @abstractmethod
    def clean_items(self) -> None:
        """Provides an interface to clean the items."""

        pass


class Catalog(BaseCatalog):
    """Stores the items from an execution.

    Attributes
    ----------
    _id : str
        ID of the catalog.
    _items : Dict[str, Any]
        Items obtained from the executions. The keys are the item IDs 
        obtained from the outputs and the values are the items obtained 
        from the returns.
    _tags : List[str]
        Tags of the catalog to provide more context.
    """

    def add_item(self, id: str, item: Any) -> None:
        """Adds an item.

        If the item does not exist, a new one is added, otherwise the existing 
        one is updated.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.
        item : Any
            Item obtained from the returns.
        """

        self._items[id] = item

    def check_item(self, id: str) -> bool:
        """Checks if an item exists.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.

        Returns
        -------
        checked : bool
            Indicates if an item exists.
        """

        return id in self._items.keys()

    def obtain_item(self, id: str) -> Any:
        """Obtains an item.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.

        Returns
        -------
        item : Any
            Item obtained from the returns.

        Raises
        ------
        CatalogError
            Informs that the id was not found in the _items.
        """

        try:
            return self._items[id]
        except KeyError as error:
            raise CatalogError(
                'id not found in the _items', f'id == {id}'
            ) from error

    def remove_item(self, id: str) -> None:
        """Removes an item.

        Parameters
        ----------
        id : str
            ID of the item obtained from the outputs.

        Raises
        ------
        CatalogError
            Informs that the id was not found in the _items.
        """

        try:
            del self._items[id]
        except KeyError as error:
            raise CatalogError(
                'id not found in the _items', f'id == {id}'
            ) from error

    def clean_items(self) -> None:
        """Cleans the items."""

        self._items.clear()
