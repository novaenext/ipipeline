"""Classes related to the execution procedures."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ipipeline.control.building import (
    build_graph, build_items, build_key_args, build_pos_args
)
from ipipeline.control.sorting import sort_topology
from ipipeline.exceptions import ExecutorError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline
from ipipeline.utils.checking import check_none


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
    """

    def __init__(
        self, pipeline: Pipeline = None, catalog: Catalog = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        pipeline : Pipeline
            Pipeline that stores a graph.
        catalog : Catalog
            Catalog that stores the items from an execution.
        """

        self.add_pipeline(pipeline)
        self.add_catalog(catalog)

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

        self._pipeline = check_none(
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

        self._catalog = check_none(
            catalog, Catalog('c0', tags=['default'])
        )

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

        graph = build_graph(self._pipeline)
        topo_order = sort_topology(graph)
        logger.info(f'topo_order: {topo_order}')

        return topo_order

    def execute_node(self, id: str) -> Dict[str, Any]:
        """Executes a node.

        Parameters
        ----------
        id : str
            ID of the node.

        Returns
        -------
        items : Dict[str, Any]
            Items of an execution. The keys are the item IDs and the values 
            are the arguments required by the tasks.

        Raises
        ------
        ExecutorError
            Informs that the node was not executed by the executor.
        """

        try:
            node = self._pipeline.nodes[id]
            logger.info(f'node.id: {node.id}, node.tags: {node.tags}')

            pos_args = build_pos_args(node.pos_inputs, self._catalog)
            key_args = build_key_args(node.key_inputs, self._catalog)
            returns = node.task(*pos_args, **key_args)
            items = build_items(node.outputs, returns)

            return items
        except Exception as error:
            raise ExecutorError(
                'node not executed by the executor', [f'id == {id}']
            ) from error

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
                task_outputs = self.execute_node(node_id)

                for out_key, out_value in task_outputs.items():
                    self._catalog.set_item(out_key, out_value)
