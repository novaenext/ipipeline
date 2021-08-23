from abc import ABC
from typing import Any, Callable, Dict, List

from ipipeline.utils.instance import InstanceIdentifier, create_instance_repr


class BaseNode(ABC, InstanceIdentifier):
    def __init__(
        self, 
        id_: str, 
        func: Callable, 
        inputs: Dict[str, Any] = {}, 
        outputs: List[str] = [], 
        props: Dict[str, Any] = {}, 
        tags: List[str] = []
    ) -> None:
        self._func = func
        self._inputs = inputs
        self._outputs = outputs
        self._props = props

        super().__init__(id_, tags)

    @property
    def func(self) -> Callable:
        return self._func

    @property
    def inputs(self) -> Dict[str, Any]:
        return self._inputs

    @property
    def outputs(self) -> List[str]:
        return self._outputs

    @property
    def props(self) -> Dict[str, Any]:
        return self._props

    def __repr__(self) -> str:
        return create_instance_repr(self)


class Node(BaseNode):
    pass
