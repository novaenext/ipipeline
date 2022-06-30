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

    def get_ordering(self, pipeline: Pipeline) -> List[list]:
        """Gets the ordering of a graph.

        Parameters
        ----------
        pipeline : Pipeline
            Pipeline that stores a flow of tasks.

        Returns
        -------
        ordering : List[list]
            Ordering of the graph. The inner lists represent groups of nodes 
            that must be executed sequentially and the nodes within these 
            groups can be executed simultaneously.

        Raises
        ------
        BuildingError
            Informs that the src_id was not found in the pipeline._nodes.
        BuildingError
            Informs that the dst_id was not found in the pipeline._nodes.
        BuildingError
            Informs that the dst_id was found in the graph[link.src_id].
        SortingError
            Informs that the dst_id was not set as a src_id.
        SortingError
            Informs that a circular dependency was found in the graph.
        """

        graph = build_graph(pipeline)
        ordering = sort_topology(graph)
        logger.info(f'ordering: {ordering}')

        return ordering

    def execute_node(
        self, pipeline: Pipeline, catalog: Catalog, id: str
    ) -> Dict[str, Any]:
        """Executes a node.

        Parameters
        ----------
        pipeline : Pipeline
            Pipeline that stores a flow of tasks.
        catalog : Catalog
            Catalog that stores the items of an execution.
        id : str
            ID of the node.

        Returns
        -------
        items : Dict[str, Any]
            Items of an execution. The keys are the item IDs and the values 
            are the arguments required by the tasks.

        Raises
        ------
        PipelineError
            Informs that the id was not found in the _nodes.
        """

        node = pipeline.get_node(id)
        logger.info(f'node.id: {node.id}, node.tags: {node.tags}')

        pos_args = build_pos_args(node.pos_inputs, catalog)
        key_args = build_key_args(node.key_inputs, catalog)
        returns = node.task(*pos_args, **key_args)
        items = build_items(node.outputs, returns)

        return items

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
