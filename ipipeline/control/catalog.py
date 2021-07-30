from abc import ABC, abstractmethod
from typing import Any, Dict

from ..exceptions import CatalogError


class BaseCatalog(ABC):
    def __init__(self) -> None:
        self._items = {}

    @property
    def items(self) -> Dict[str, dict]:
        return self._items

    @abstractmethod
    def add_item(self, id_: str, item: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def update_item(self, id_: str, item: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def check_item(self, id_: str) -> bool:
        pass
   
    @abstractmethod
    def obtain_item(self, id_: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def remove_item(self, id_: str) -> None:
        pass


class Catalog(BaseCatalog):
    def add_item(self, id_: str, item: Dict[str, Any]) -> None:
        self._items[id_] = item

    def update_item(self, id_: str, item: Dict[str, Any]) -> None:
        try:
            self._items[id_].update(item)
        except KeyError as error:
            raise CatalogError('id_ not found', f'id_ == {id_}') from error

    def check_item(self, id_: str) -> bool:
        return id_ in self._items

    def obtain_item(self, id_: str) -> Dict[str, Any]:
        try:
            return self._items[id_]
        except KeyError as error:
            raise CatalogError('id_ not found', f'id_ == {id_}') from error

    def remove_item(self, id_: str) -> None:
        try:
            del self._items[id_]
        except KeyError as error:
            raise CatalogError('id_ not found', f'id_ == {id_}') from error
