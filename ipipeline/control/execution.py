import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from ipipeline.control.catalog import Catalog
from ipipeline.exceptions import ExecutionError
from ipipeline.structure.pipeline import BasePipeline
from ipipeline.utils.instance import InstanceIdentifier, create_instance_repr


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC, InstanceIdentifier):
    def __init__(self, id_: str, tags: List[str] = []) -> None:
        self._catalog = Catalog()

        super().__init__(id_, tags)

    @abstractmethod
    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: list
    ) -> Dict[str, dict]:
        pass

    def __repr__(self) -> str:
        return create_instance_repr(self)


class SequentialExecutor(BaseExecutor):
    def execute_pipeline(
        self, pipeline: BasePipeline, topo_order: List[str]
    ) -> Dict[str, dict]:
        for node_id in topo_order:
            node = pipeline.nodes[node_id]
            logger.info(f'executing node: node.id == {node.id}')

            func_inputs = self._create_func_inputs(node.inputs)
            unn_outputs = self._execute_func(node.id, node.func, func_inputs)
            func_outputs = self._create_func_outputs(node.outputs, unn_outputs)

            if func_outputs:
                self._catalog.add_item(node.id, func_outputs)

        return self._catalog.items

    def _create_func_inputs(
        self, node_inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        func_inputs = {}

        for input_key, input_value in node_inputs.items():
            if self._catalog.check_item(input_key):
                func_outputs = self._catalog.obtain_item(input_key)

                for output_key in input_value:
                    try:
                        func_inputs[output_key] = func_outputs[output_key]
                    except KeyError as error:
                        raise ExecutionError(
                            'output_key not found', 
                            f'input_key == {input_key} '
                            f'and output_key == {output_key}'
                        ) from error
            else:
                func_inputs[input_key] = input_value

        return func_inputs

    def _execute_func(
        self, node_id: str, node_func: Callable, func_inputs: Dict[str, Any]
    ) -> Any:
        try:
            return node_func(**func_inputs)
        except Exception as error:
            raise ExecutionError(
                'node_func not executed', f'node_id == {node_id}'
            ) from error

    def _create_func_outputs(
        self, node_outputs: List[str], unn_outputs: Any
    ) -> Dict[str, Any]:
        node_outputs_qty = len(node_outputs)

        if node_outputs_qty == 1:
            return {node_outputs[0]: unn_outputs}
        elif node_outputs_qty > 1:
            unn_outputs_qty = getattr(unn_outputs, '__len__', lambda: 1)()
 
            if node_outputs_qty == unn_outputs_qty:
                return dict(zip(node_outputs, unn_outputs))
            else:
                raise ExecutionError(
                    'outputs not matched', 
                    f'node_outputs_qty == {node_outputs_qty} '
                    f'and unn_outputs_qty == {unn_outputs_qty}'
                )
        else:
            return {}
