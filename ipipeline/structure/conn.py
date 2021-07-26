from abc import ABC
from typing import List

from ..utils.instance import InstanceIdentifier, create_instance_repr


class BaseConn(ABC, InstanceIdentifier):
    def __init__(
        self, 
        id_: str, 
        src_id: str, 
        dst_id: str, 
        weight: int = 0, 
        tags: List[str] = []
    ) -> None:
        self._src_id = src_id
        self._dst_id = dst_id
        self._weight = weight

        super().__init__(id_, tags)

    @property
    def src_id(self) -> str:
        return self._src_id

    @property
    def dst_id(self) -> str:
        return self._dst_id

    @property
    def weight(self) -> int:
        return self._weight

    def __repr__(self) -> str:
        return create_instance_repr(self)


class Conn(BaseConn):
    pass
