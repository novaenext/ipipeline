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


logger = logging.getLogger(name=__name__)


class BaseExecutor(ABC):
    """Provides an interface to the executor classes."""

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
        ExecutorError
            Informs that the node was not executed by the executor.
        """

        node = pipeline.get_node(id)
        logger.info(f'node.id: {node.id}, node.tags: {node.tags}')

        pos_args = build_pos_args(node.pos_inputs, catalog)
        key_args = build_key_args(node.key_inputs, catalog)

        try:
            returns = node.task(*pos_args, **key_args)
        except Exception as error:
            raise ExecutorError(
                'node was not executed by the executor', [f'id == {node.id}']
            ) from error

        items = build_items(node.outputs, returns)

        return items

    @abstractmethod
    def execute_pipeline(
        self, pipeline: Pipeline, catalog: Catalog, ordering: List[list]
    ) -> Catalog:
        """Provides an interface to execute a pipeline.

        Parameters
        ----------
        pipeline : Pipeline
            Pipeline that stores a flow of tasks.
        catalog : Catalog
            Catalog that stores the items of an execution.
        ordering : List[list]
            Ordering of the graph. The inner lists represent groups of nodes 
            that must be executed sequentially and the nodes within these 
            groups can be executed simultaneously.

        Returns
        -------
        catalog : Catalog
            Catalog that stores the items of an execution.

        Raises
        ------
        ExecutorError
            Informs that the node was not executed by the executor.
        """

        pass


class SequentialExecutor(BaseExecutor):
    """Executes a pipeline sequentially."""

    def execute_pipeline(
        self, pipeline: Pipeline, catalog: Catalog, ordering: List[list]
    ) -> Catalog:
        """Executes a pipeline.

        Parameters
        ----------
        pipeline : Pipeline
            Pipeline that stores a flow of tasks.
        catalog : Catalog
            Catalog that stores the items of an execution.
        ordering : List[list]
            Ordering of the graph. The inner lists represent groups of nodes 
            that must be executed sequentially and the nodes within these 
            groups can be executed simultaneously.

        Returns
        -------
        catalog : Catalog
            Catalog that stores the items of an execution.

        Raises
        ------
        ExecutorError
            Informs that the node was not executed by the executor.
        """

        logger.info(
            f'pipeline.id: {pipeline.id}, pipeline.tags: {pipeline.tags}'
        )
        logger.info(
            f'catalog.id: {catalog.id}, catalog.tags: {catalog.tags}'
        )

        for group in ordering:
            for node_id in group:
                items = self.execute_node(pipeline, catalog, node_id)

                for item_id, item in items.items():
                    catalog.set_item(item_id, item)

        return catalog
