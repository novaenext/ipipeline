"""Classes related to the execution procedures."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ipipeline.execution.building import build_task_inputs, build_task_outputs
from ipipeline.execution.sorting import sort_graph_topo
from ipipeline.exceptions import ExecutorError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline
from ipipeline.structure.signal import Signal
from ipipeline.utils.instance import check_none_arg


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC):
    """Provides an interface to the executor classes.

    The execution of the graph stored in the pipeline is according to its 
    topological order. The returns from each executed node are stored in 
    the catalog to provide access to subsequent nodes.

    Attributes
    ----------
    _pipeline : Pipeline
        Pipeline that stores a graph.
    _catalog : Catalog
        Catalog that stores the items from an execution.
    _signals : Dict[str, Signal]
        Signals of the execution. The keys are the node IDs and the values 
        are the signals where the IDs are obtained.
    """

    def __init__(
        self, 
        pipeline: Pipeline = None, 
        catalog: Catalog = None, 
        signals: Dict[str, Signal] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        pipeline : Pipeline
            Pipeline that stores a graph.
        catalog : Catalog
            Catalog that stores the items from an execution.
        signals : Dict[str, Signal]
            Signals of the execution. The keys are the node IDs and the values 
            are the signal instances.
        """

        self.add_pipeline(pipeline)
        self.add_catalog(catalog)
        self._signals = check_none_arg(signals, {})

    @property
    def pipeline(self) -> Pipeline:
        """Obtains the _pipeline attribute.

        Returns
        -------
        pipeline : Pipeline
            Pipeline that stores a graph.
        """

        return self._pipeline

    @property
    def catalog(self) -> Catalog:
        """Obtains the _catalog attribute.

        Returns
        -------
        catalog : Catalog
            Catalog that stores the items from an execution.
        """

        return self._catalog

    @property
    def signals(self) -> Dict[str, Signal]:
        """Obtains the _signals attribute.

        Returns
        -------
        signals : Dict[str, Signal]
            Signals of the execution. The keys are the node IDs and the values 
            are the signal instances.
        """

        return self._signals

    def add_pipeline(self, pipeline: Pipeline) -> None:
        """Adds a pipeline in the executor.

        Parameters
        ----------
        pipeline : Pipeline
            Pipeline that stores a graph.

        Raises
        ------
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._pipeline = check_none_arg(
            pipeline, Pipeline('p0', tags=['default'])
        )

    def add_catalog(self, catalog: Catalog) -> None:
        """Adds a catalog in the executor.

        Parameters
        ----------
        catalog : Catalog
            Catalog that stores the items from an execution.

        Raises
        ------
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._catalog = check_none_arg(
            catalog, Catalog('c0', tags=['default'])
        )

    def add_signal(
        self, 
        id: str, 
        node_id: str, 
        type: str, 
        status: bool = True, 
        tags: List[str] = None
    ) -> None:
        """Adds a signal to a node.

        Parameters
        ----------
        id : str
            ID of the signal.
        node_id : str
            ID of the node.
        type : str
            Type of the signal used to trigger an action.
        status : bool, default=True
            Indicates if the signal is enable or disable.
        tags : List[str], default=None
            Tags of the signal to provide more context.

        Raises
        ------
        PipelineError
            Informs that the node_id was not found in the _nodes.
        ExecutorError
            Informs that the type was not found in the valid_types.
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._pipeline._check_inexistent_node_id(node_id)
        self._check_invalid_type(type)
        signal = Signal(id, node_id, type, status, tags)

        self._signals[signal.node_id] = signal

    def _check_invalid_type(self, type: str) -> None:
        """Checks if the type is invalid.

        Parameters
        ----------
        type : {'skip'}
            Type of the signal that triggers an action.

            skip: skips the node execution.

        Raises
        ------
        ExecutorError
            Informs that the type was not found in the valid_types.
        """

        valid_types = ['skip']

        if type not in valid_types:
            raise ExecutorError(
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
        task_outputs : Dict[str, Any]
            Outputs of the task. The keys are the outputs and the values 
            are the returns obtained from the execution.

        Raises
        ------
        ExecutorError
            Informs that the node was not executed by the executor.
        """

        try:
            node = self._pipeline.nodes[id]
            logger.info(f'node.id: {node.id}, node.tags: {node.tags}')

            task_inputs = build_task_inputs(node.inputs, self._catalog)
            returns = node.task(**task_inputs)
            task_outputs = build_task_outputs(node.outputs, returns)

            return task_outputs
        except Exception as error:
            raise ExecutorError(
                'node not executed by the executor', f'id == {id}'
            ) from error

    def obtain_topo_order(self) -> List[list]:
        """Obtains the topological order of the graph.

        Returns
        -------
        topo_order : List[list]
            Topological order of the graph. The inner lists represent groups 
            of nodes that must be executed in order and the nodes within these 
            groups can be executed simultaneously.

        Raises
        ------
        SortingError
            Informs that the dst_node_id was not specified as a src_node_id.
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
            of nodes that must be executed in order and the nodes within these 
            groups can be executed simultaneously.
        """

        pass


class SequentialExecutor(BaseExecutor):
    """Executes a pipeline sequentially.

    The execution of the graph stored in the pipeline is according to its 
    topological order. The returns from each executed node are stored in 
    the catalog to provide access to subsequent nodes.

    Attributes
    ----------
    _pipeline : Pipeline
        Pipeline that stores a graph.
    _catalog : Catalog
        Catalog that stores the items from an execution.
    _signals : Dict[str, Signal]
        Signals of the execution. The keys are the node IDs and the values 
        are the signals where the IDs are obtained.
    """

    def execute_pipeline(self, topo_order: List[list]) -> None:
        """Executes a pipeline.

        Parameters
        ----------
        topo_order : List[list]
            Topological order of the graph. The inner lists represent groups 
            of nodes that must be executed in order and the nodes within these 
            groups can be executed simultaneously.

        Raises
        ------
        ExecutorError
            Informs that the node was not executed by the executor.
        """

        for group in topo_order:
            for node_id in group:
                signal = self._signals.get(
                    node_id, Signal('s0', node_id, 'default')
                )

                if signal.type == 'skip' and signal.status == True:
                    continue
                else:
                    task_outputs = self.execute_node(node_id)

                    for out_key, out_value in task_outputs.items():
                        self._catalog.add_item(out_key, out_value)
