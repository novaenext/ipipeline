import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from ipipeline.control.building import Builder
from ipipeline.control.catalog import Catalog
from ipipeline.exceptions import ExecutionError
from ipipeline.structure.node import BaseNode
from ipipeline.structure.pipeline import BasePipeline
from ipipeline.utils.instance import InstanceIdentifier


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC, InstanceIdentifier):
    @abstractmethod
    def flag_node(self, node_id: str, flag: str) -> None:
        pass

    @abstractmethod
    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: list
    ) -> None:
        pass


class SequentialExecutor(BaseExecutor):
    def __init__(self, id_: str, tags: List[str] = []) -> None:
        self._flagged_nodes = {}
        self._builder = Builder()
        self._catalog = Catalog()

        super().__init__(id_, tags)

    @property
    def catalog(self) -> Catalog:
        return self._catalog

    def flag_node(self, node_id: str, flag: str) -> None:
        self._check_invalid_flag(flag)

        if node_id not in self._flagged_nodes:
            self._flagged_nodes[node_id] = {}
        self._flagged_nodes[node_id][flag] = True

    def _check_invalid_flag(self, flag: str) -> None:
        valid_flags = ['skip']

        if flag not in valid_flags:
            raise ExecutionError(
                'flag not found in the valid_flags', f'flag == {flag}'
            )

    def _check_inexistent_node_id(
        self, nodes: Dict[str, BaseNode], node_id: str
    ) -> None:
        if node_id not in nodes:
            raise ExecutionError(
                'node_id not found in the nodes', f'node_id == {node_id}'
            )

    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: List[str]
    ) -> None:
        for node_id in topo_order:
            if not self._flagged_nodes.get(node_id, {}).get('skip', False):
                node = pipeline.nodes[node_id]
                logger.info(f'node - id: {node.id}, tags: {node.tags}')

                func_inputs = self._builder.build_func_inputs(
                    node.inputs, self._catalog
                )
                results = self._execute_func(node.id, node.func, func_inputs)
                func_outputs = self._builder.build_func_outputs(
                    node.outputs, results
                )

                if func_outputs:
                    self._catalog_outputs(func_outputs)

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
