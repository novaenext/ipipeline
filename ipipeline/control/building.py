"""Functions related to the building procedures."""

from typing import Any, Dict, List

from ipipeline.exceptions import BuildingError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.pipeline import Pipeline


def build_graph(pipeline: Pipeline) -> Dict[str, list]:
    """Builds a graph.

    Parameters
    ----------
    pipeline : Pipeline
        Pipeline that stores a flow of tasks.

    Returns
    -------
    graph : Dict[str, list]
        Graph of the pipeline. The keys are the source node IDs and the 
        values are the lists of destination node IDs.

    Raises
    ------
    BuildingError
        Informs that the src_id was not found in the pipeline._nodes.
    BuildingError
        Informs that the dst_id was not found in the pipeline._nodes.
    BuildingError
        Informs that the dst_id was found in the graph[link.src_id].
    """

    graph = {}

    for node in pipeline.nodes.values():
        graph[node.id] = []

    for link in pipeline.links.values():
        if not pipeline.check_node(link.src_id):
            raise BuildingError(
                'src_id was not found in the pipeline._nodes', 
                [f'src_id == {link.src_id}']
            )

        if not pipeline.check_node(link.dst_id):
            raise BuildingError(
                'dst_id was not found in the pipeline._nodes', 
                [f'dst_id == {link.dst_id}']
            )

        if link.dst_id in graph[link.src_id]:
            raise BuildingError(
                'dst_id was found in the graph[link.src_id]', 
                [f'dst_id == {link.dst_id}']
            )

        graph[link.src_id].append(link.dst_id)

    return graph


def build_pos_args(pos_inputs: List[str], catalog: Catalog) -> List[Any]:
    """Builds the positional arguments of a task.

    Parameters
    ----------
    pos_inputs : List[str]
        Positional inputs of the task. The elements are the IDs of the 
        catalog items.
    catalog : Catalog
        Catalog that stores the items of an execution.

    Returns
    -------
    pos_args : List[Any]
        Positional arguments of a task.
    """

    pos_args = []

    for item_id in pos_inputs:
        pos_args.append(catalog.get_item(item_id))

    return pos_args


def build_key_args(
    key_inputs: Dict[str, str], catalog: Catalog
) -> Dict[str, Any]:
    """Builds the keyword arguments of a task.

    Parameters
    ----------
    key_inputs : Dict[str, str]
        Keyword inputs of the task. The keys are the task parameters and 
        the values are the IDs of the catalog items.
    catalog : Catalog
        Catalog that stores the items of an execution.

    Returns
    -------
    key_args : Dict[str, Any]
        Keyword arguments of a task.
    """

    key_args = {}

    for param, item_id in key_inputs.items():
        key_args[param] = catalog.get_item(item_id)

    return key_args


def build_items(outputs: List[str], returns: Any) -> Dict[str, Any]:
    """Builds the items of an execution.

    Parameters
    ----------
    outputs : List[str]
        Outputs of the task. The outputs must match the returns in terms 
        of size when more than one output is expected.
    returns : Any
        Returns of the executed task.

    Returns
    -------
    items : Dict[str, Any]
        Items of an execution. The keys are the item IDs and the values 
        are the arguments required by the tasks.

    Raises
    ------
    BuildingError
        Informs that an invalid type was found for the returns.
    BuildingError
        Informs that the outputs did not match the returns in terms of size.
    """

    items = {}

    if len(outputs) > 0:
        if len(outputs) == 1:
            returns = [returns]

        if not isinstance(returns, (list, tuple)):
            raise BuildingError(
                'invalid type was found for the returns', 
                [f'type == {type(returns)}']
            )

        if len(outputs) != len(returns):
            raise BuildingError(
                'outputs did not match the returns in terms of size', 
                [f'{len(outputs)} != {len(returns)}']
            )

        items = dict(zip(outputs, returns))

    return items
