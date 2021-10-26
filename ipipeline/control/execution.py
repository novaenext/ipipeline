"""Classes related to the execution procedures."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ipipeline.control.building import build_func_inputs, build_func_outputs
from ipipeline.control.catalog import BaseCatalog, Catalog
from ipipeline.control.sorting import sort_graph_topo
from ipipeline.exception import ExecutionError
from ipipeline.structure.pipeline import BasePipeline


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC):
    """Provides an interface to the executor classes.

    Attributes
    ----------
    _pipeline : BasePipeline
        Pipeline that stores the graph structure.
    _catalog : BaseCatalog
        Catalog that stores the items from the execution.
    _flags : Dict[str, dict]
        Flags linked to the nodes. The keys are the node IDs and values are 
        the flags and their status.
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
        self._flags = {}

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

        if catalog:
            return catalog
        else:
            return Catalog()

    def flag_node(self, node_id: str, flag: str, status: bool) -> None:
        """Flags a node.

        Parameters
        ----------
        node_id : str
            ID of the node.
        flag : {'skip'}
            Flag that acts as a signal to take some action during execution. 

            skip: skips the node execution.
        status : bool
            Indicates if the flag is enable (True) or disable (False).

        Raises
        ------
        ExecutionError
            Informs that the node was not flagged in the _flags.
        """

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
        """Checks if the flag is invalid.

        Parameters
        ----------
        flag : {'skip'}
            Flag that acts as a signal to take some action during execution. 

            skip: skips the node execution.

        Raises
        ------
        ExecutionError
            Informs that the flag was not found in the valid_flags.
        """

        valid_flags = ['skip']

        if flag not in valid_flags:
            raise ExecutionError(
                'flag not found in the valid_flags', f'flag == {flag}'
            )

    def execute_node(self, node_id: str) -> Dict[str, Any]:
        """Executes a node.

        Parameters
        ----------
        node_id : str
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
    _flags : Dict[str, dict]
        Flags linked to the nodes. The keys are the node IDs and values are 
        the flags and their status.
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
                if not self._flags.get(node_id, {}).get('skip', False):
                    func_outputs = self.execute_node(node_id)

                    for id, item in func_outputs.items():
                        self._catalog.add_item(id, item)
