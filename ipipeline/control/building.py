from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ipipeline.control.catalog import BaseCatalog
from ipipeline.exceptions import BuildingError


class BaseBuilder(ABC):
    @abstractmethod
    def build_func_inputs(
        self, inputs: Dict[str, Any], catalog: BaseCatalog
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def build_func_outputs(
        self, outputs: List[str], returns: Any
    ) -> Dict[str, Any]:
        pass


class Builder(BaseBuilder):
    def build_func_inputs(
        self, inputs: Dict[str, Any], catalog: BaseCatalog
    ) -> Dict[str, Any]:
        func_inputs = {}

        for in_key, in_value in inputs.items():
            if isinstance(in_value, str) and in_value.startswith('c.'):
                func_inputs[in_key] = catalog.obtain_item(
                    in_value.replace('c.', '')
                )
            else:
                func_inputs[in_key] = in_value

        return func_inputs

    def build_func_outputs(
        self, outputs: List[str], returns: Any
    ) -> Dict[str, Any]:
        outputs_qty = len(outputs)

        if outputs_qty > 0:
            if outputs_qty == 1:
                returns = [returns]

            try:
                returns_qty = len(returns)
            except TypeError:
                returns_qty = 1

            self._check_diff_outputs_qty(outputs_qty, returns_qty)

            return dict(zip(outputs, returns))
        else:
            return {}

    def _check_diff_outputs_qty(
        self, outputs_qty: int, returns_qty: int
    ) -> None:
        if outputs_qty != returns_qty:
            raise BuildingError(
                'outputs did not match', f'{outputs_qty} != {returns_qty}'
            )
