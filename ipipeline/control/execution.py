import logging
from abc import ABC, abstractmethod
from itertools import chain
from typing import Any, Dict, List

from ipipeline.control.building import build_func_inputs, build_func_outputs
from ipipeline.control.catalog import BaseCatalog, Catalog
from ipipeline.control.sorting import sort_graph_topo
from ipipeline.exception import ExecutionError
from ipipeline.structure.pipeline import BasePipeline


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC):
    def __init__(
        self, pipeline: BasePipeline, catalog: BaseCatalog = None
    ) -> None:
        self._pipeline = pipeline
        self._catalog = self._check_empty_catalog(catalog)
        self._flags = {}

    @property
    def pipeline(self) -> BasePipeline:
        return self._pipeline

    @property
    def catalog(self) -> BaseCatalog:
        return self._catalog

    def _check_empty_catalog(self, catalog: BaseCatalog) -> BaseCatalog:
        if catalog:
            return catalog
        else:
            return Catalog()

    def flag_node(self, node_id: str, flag: str, status: bool) -> None:
        try:
            self._check_invalid_flag(flag)
            node = self._pipeline.nodes[node_id]

            if node.id not in self._flags:
                self._flags[node.id] = {}
            self._flags[node.id][flag] = status
        except Exception as error:
            raise ExecutionError(
                'node not flagged in the _flags', f'node_id == {node_id}'
            ) from error

    def _check_invalid_flag(self, flag: str) -> None:
        valid_flags = ['skip']

        if flag not in valid_flags:
            raise ExecutionError(
                'flag not found in the valid_flags', f'flag == {flag}'
            )

    def execute_node(self, node_id: str) -> Dict[str, Any]:
        try:
            node = self._pipeline.nodes[node_id]
            logger.info(f'node - id: {node.id}, tags: {node.tags}')

            func_inputs = build_func_inputs(node.inputs, self._catalog.items)
            returns = node.func(**func_inputs)
            func_outputs = build_func_outputs(node.outputs, returns)

            return func_outputs
        except Exception as error:
            raise ExecutionError(
                'node not executed by the executor', f'node_id == {node_id}'
            ) from error

    def obtain_exe_order(self) -> List[list]:
        exe_order = sort_graph_topo(self._pipeline.graph)
        logger.info(f'exe_order: {exe_order}')

        return exe_order

    @abstractmethod
    def execute_pipeline(self, exe_order: list) -> None:
        pass


class SequentialExecutor(BaseExecutor):
    def obtain_exe_order(self) -> List[str]:
        exe_order = super().obtain_exe_order()

        return list(chain(*exe_order))

    def execute_pipeline(self, exe_order: List[str]) -> None:
        for node_id in exe_order:
            if not self._flags.get(node_id, {}).get('skip', False):
                func_outputs = self.execute_node(node_id)

                for id, item in func_outputs.items():
                    self._catalog.add_item(id, item)
