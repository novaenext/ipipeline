"""Classes related to the execution procedures."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ipipeline.control.building import build_func_inputs, build_func_outputs
from ipipeline.control.sorting import sort_graph_topo
from ipipeline.exception import ExecutionError
from ipipeline.structure.catalog import BaseCatalog, Catalog
from ipipeline.structure.pipeline import BasePipeline
from ipipeline.structure.signal import BaseSignal, Signal


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC):
    """Provides an interface to the executor classes.

    Attributes
    ----------
    _pipeline : BasePipeline
        Pipeline that stores the graph structure.
    _catalog : BaseCatalog
        Catalog that stores the items from the execution.
    _signals : Dict[str, BaseSignal]
        Signals of the execution. The keys are the element (node) IDs and 
        the values are the signal objects where the IDs were obtained.
    """

    def __init__(
        self, pipeline: BasePipeline, catalog: BaseCatalog = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        pipeline : BasePipeline
            Pipeline that stores the graph structure.
        catalog : BaseCatalog, default=None
            Catalog that stores the items from the execution.
        """

        self._pipeline = pipeline
        self._catalog = self._check_inexistent_catalog(catalog)
        self._signals = {}

    @property
    def pipeline(self) -> BasePipeline:
        """Obtains the _pipeline attribute.

        Returns
        -------
        pipeline : BasePipeline
            Pipeline that stores the graph structure.
        """

        return self._pipeline

    @property
    def catalog(self) -> BaseCatalog:
        """Obtains the _catalog attribute.

        Returns
        -------
        catalog : BaseCatalog
            Catalog that stores the items from the execution.
        """

        return self._catalog

    @property
    def signals(self) -> Dict[str, BaseSignal]:
        """Obtains the _signals attribute.

        Returns
        -------
        signals : Dict[str, BaseSignal]
            Signals of the execution. The keys are the element (node) IDs and 
            the values are the signal objects where the IDs were obtained.
        """

        return self._signals

    def _check_inexistent_catalog(self, catalog: BaseCatalog) -> BaseCatalog:
        """Checks if the catalog does not exist.

        A default catalog is provided for convenience.

        Parameters
        ----------
        catalog : BaseCatalog
            Catalog that stores the items from the execution.

        Returns
        -------
        catalog : BaseCatalog
            Catalog that stores the items from the execution.
        """

        if not catalog:
            catalog = Catalog(self._pipeline.id, tags=self._pipeline.tags)

        return catalog

    def add_signal(
        self, 
        id: str, 
        elem_id: str, 
        type: str, 
        status: bool, 
        tags: List[str] = []
    ) -> None:
        """Adds a signal in the execution.

        Parameters
        ----------
        id : str
            ID of the signal.
        elem_id : str
            ID of the element (node).
        type : {'skip'}
            Type of the signal that triggers an action.

            skip: skips the node execution.
        status : bool
            Indicates if the signal is enable or disable.
        tags : List[str]
            Tags of the signal to provide more context.

        Raises
        ------
        ExecutionError
            Informs that the elem_id was not found in the _pipeline.nodes.
        ExecutionError
            Informs that the type was not found in the valid_types.
        """

        self._check_inexistent_elem_id(elem_id)
        self._check_invalid_type(type)
        signal = Signal(id, elem_id, type, status, tags)

        self._signals[signal.elem_id] = signal

    def _check_inexistent_elem_id(self, elem_id: str) -> None:
        """Checks if the element ID does not exist.

        Parameters
        ----------
        elem_id : str
            ID of the element (node).

        Raises
        ------
        ExecutionError
            Informs that the elem_id was not found in the _pipeline.nodes.
        """

        if elem_id not in self._pipeline.nodes.keys():
            raise ExecutionError(
                'elem_id not found in the _pipeline.nodes', 
                f'elem_id == {elem_id}'
            )

    def _check_invalid_type(self, type: str) -> None:
        """Checks if the type is invalid.

        Parameters
        ----------
        type : {'skip'}
            Type of the signal that triggers an action.

            skip: skips the node execution.

        Raises
        ------
        ExecutionError
            Informs that the type was not found in the valid_types.
        """

        valid_types = ['skip']

        if type not in valid_types:
            raise ExecutionError(
                'type not found in the valid_types', f'type == {type}'
            )

    def execute_node(self, id: str) -> Dict[str, Any]:
        """Executes a node.

        Parameters
        ----------
        id : str
            ID of the node.

        Returns
        -------
        func_outputs : Dict[str, Any]
            Outputs of the function built according to the combination of the 
            outputs and returns. The keys are the outputs and the values are 
            the returns.

        Raises
        ------
        ExecutionError
            Informs that the node was not executed by the executor.
        """

        try:
            node = self._pipeline.nodes[id]
            logger.info(f'node.id: {node.id}, node.tags: {node.tags}')

            func_inputs = build_func_inputs(node.inputs, self._catalog)
            returns = node.func(**func_inputs)
            func_outputs = build_func_outputs(node.outputs, returns)

            return func_outputs
        except Exception as error:
            raise ExecutionError(
                'node not executed by the executor', f'id == {id}'
            ) from error

    def obtain_topo_order(self) -> List[list]:
        """Obtains the topological order of the graph.

        Returns
        -------
        topo_order : List[list]
            Topological order of the graph. The inner lists represent groups 
            of nodes where the groups must be executed in order and the nodes 
            within them can be processed simultaneously.

        Raises
        ------
        SortingError
            Informs that the dst_node_id was not specified as src_node_id.
        SortingError
            Informs that a circular dependency was found in the graph.
        """

        topo_order = sort_graph_topo(self._pipeline.graph)
        logger.info(f'topo_order: {topo_order}')

        return topo_order

    @abstractmethod
    def execute_pipeline(self, topo_order: List[list]) -> None:
        """Provides an interface to execute a pipeline.

        Parameters
        ----------
        topo_order : List[list]
            Topological order of the graph. The inner lists represent groups 
            of nodes where the groups must be executed in order and the nodes 
            within them can be processed simultaneously.
        """

        pass


class SequentialExecutor(BaseExecutor):
    """Executes a pipeline sequentially.

    Attributes
    ----------
    _pipeline : BasePipeline
        Pipeline that stores the graph structure.
    _catalog : BaseCatalog
        Catalog that stores the items from the execution.
    _signals : Dict[str, BaseSignal]
        Signals of the execution. The keys are the element IDs and the 
        values are the signal objects where the IDs were obtained.
    """

    def execute_pipeline(self, topo_order: List[list]) -> None:
        """Executes a pipeline.

        Parameters
        ----------
        topo_order : List[list]
            Topological order of the graph. The inner lists represent groups 
            of nodes where the groups must be executed in order and the nodes 
            within them can be processed simultaneously.

        Raises
        ------
        ExecutionError
            Informs that the node was not executed by the executor.
        """

        for group in topo_order:
            for node_id in group:
                signal = self._signals.get(
                    node_id, Signal('s0', node_id, 'default', False)
                )

                if signal.type == 'skip' and signal.status == True:
                    continue
                else:
                    func_outputs = self.execute_node(node_id)

                    for id, item in func_outputs.items():
                        self._catalog.add_item(id, item)
