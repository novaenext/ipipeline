from abc import ABC
from typing import Any, Callable, Dict, List

from ipipeline.utils.instance import InstanceIdentifier


class BaseNode(ABC, InstanceIdentifier):
    def __init__(
        self, 
        id_: str, 
        func: Callable, 
        inputs: Dict[str, Any] = {}, 
        outputs: List[str] = [], 
        tags: List[str] = []
    ) -> None:
        self._func = func
        self._inputs = inputs
        self._outputs = outputs

        super().__init__(id_, tags=tags)

    @property
    def func(self) -> Callable:
        return self._func

    @property
    def inputs(self) -> Dict[str, Any]:
        return self._inputs

    @property
    def outputs(self) -> List[str]:
        return self._outputs


class Node(BaseNode):
    pass
