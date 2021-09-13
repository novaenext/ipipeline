import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ipipeline.control.building import build_func_inputs, build_func_outputs
from ipipeline.control.catalog import Catalog
from ipipeline.exceptions import ExecutionError
from ipipeline.structure.pipeline import BasePipeline
from ipipeline.utils.instance import InstanceIdentifier


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC, InstanceIdentifier):
    @abstractmethod
    def flag_node(self, node_id: str, flag: str, status: bool) -> None:
        pass

    @abstractmethod
    def execute_node(
        self, pipeline: BasePipeline, node_id: str
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: list
    ) -> None:
        pass


class SequentialExecutor(BaseExecutor):
    def __init__(self, id_: str, tags: List[str] = []) -> None:
        self._catalog = Catalog()
        self._flagged = {}

        super().__init__(id_, tags)

    @property
    def catalog(self) -> Catalog:
        return self._catalog

    def flag_node(self, node_id: str, flag: str, status: bool) -> None:
        self._check_invalid_flag(flag)

        if node_id not in self._flagged:
            self._flagged[node_id] = {}
        self._flagged[node_id][flag] = status

    def _check_invalid_flag(self, flag: str) -> None:
        valid_flags = ['skip']

        if flag not in valid_flags:
            raise ExecutionError(
                'flag not found in the valid_flags', f'flag == {flag}'
            )

    def execute_node(
        self, pipeline: BasePipeline, node_id: str
    ) -> Dict[str, Any]:
        try:
            node = pipeline.nodes[node_id]
            logger.info(f'node - id: {node.id}, tags: {node.tags}')

            func_inputs = build_func_inputs(node.inputs, self._catalog.items)
            returns = node.func(**func_inputs)
            func_outputs = build_func_outputs(node.outputs, returns)

            return func_outputs
        except Exception as error:
            raise ExecutionError(
                'node not executed', f'node_id == {node_id}'
            ) from error

    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: List[str]
    ) -> None:
        for node_id in topo_order:
            if not self._flagged.get(node_id, {}).get('skip', False):
                outputs = self.execute_node(pipeline, node_id)

                if outputs:
                    for out_key, out_value in outputs.items():
                        self._catalog.add_item(out_key, out_value)
