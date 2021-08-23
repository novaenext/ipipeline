import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from ipipeline.control.building import Builder
from ipipeline.control.catalog import Catalog
from ipipeline.exceptions import ExecutionError
from ipipeline.structure.pipeline import BasePipeline
from ipipeline.utils.instance import InstanceIdentifier


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC, InstanceIdentifier):
    @abstractmethod
    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: List[Any]
    ) -> Any:
        pass


class SequentialExecutor(BaseExecutor):
    def __init__(self, id_: str, tags: List[str] = []) -> None:
        self._builder = Builder()
        self._catalog = Catalog()

        super().__init__(id_, tags)

    @property
    def catalog(self) -> Catalog:
        return self._catalog

    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: List[str]
    ) -> Dict[str, Any]:
        for node_id in topo_order:
            node = pipeline.nodes[node_id]
            logger.info(f'node.id: {node.id}')

            func_inputs = self._builder.build_func_inputs(
                node.inputs, self._catalog
            )
            results = self._execute_func(node.id, node.func, func_inputs)
            func_outputs = self._builder.build_func_outputs(
                node.outputs, results
            )

            if func_outputs:
                self._catalog_outputs(func_outputs)

        return self._catalog.items

    def _execute_func(
        self, id_: str, func: Callable, inputs: Dict[str, Any]
    ) -> Any:
        try:
            return func(**inputs)
        except Exception as error:
            raise ExecutionError(
                'func not executed', f'id == {id_}'
            ) from error

    def _catalog_outputs(self, outputs: Dict[str, Any]) -> None:
        for out_key, out_value in outputs.items():
            self._catalog.add_item(out_key, out_value)
