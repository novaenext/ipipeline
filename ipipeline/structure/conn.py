from abc import ABC
from typing import Any, List

from ipipeline.util.instance import Identification


class BaseConn(ABC, Identification):
    def __init__(
        self, 
        id: str, 
        src_id: str, 
        dst_id: str, 
        value: Any = None, 
        tags: List[str] = []
    ) -> None:
        self._src_id = src_id
        self._dst_id = dst_id
        self._value = value

        super().__init__(id, tags=tags)

    @property
    def src_id(self) -> str:
        return self._src_id

    @property
    def dst_id(self) -> str:
        return self._dst_id

    @property
    def value(self) -> Any:
        return self._value


class Conn(BaseConn):
    pass
