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
        values are a list of destination node IDs.

    Raises
    ------
    BuildingError
        Informs that the src_id was not found in the pipeline._nodes.
    BuildingError
        Informs that the dst_id was not found in the pipeline._nodes.
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

        graph[link.src_id].append(link.dst_id)

    return graph


def build_task_inputs(
    inputs: Dict[str, Any], catalog: Catalog
) -> Dict[str, Any]:
    """Builds the inputs of a task.

    Parameters
    ----------
    inputs : Dict[str, Any]
        Inputs of the task. The keys are the callable parameters and the 
        values are the data required for the parameters. The values can 
        also be placeholders for the catalog items.

        Placeholders:
            'c.<item_id>': gets an item.
            'c.[<item_id>, ..., <item_id>]': gets a list of items.
    catalog : Catalog
        Catalog that stores the items.

    Returns
    -------
    task_inputs : Dict[str, Any]
        Inputs of the task. The keys are the callable parameters and 
        the values are the data required for the parameters.

    Raises
    ------
    CatalogError
        Informs that the id was not found in the _items.
    """

    task_inputs = {}

    for in_key, in_value in inputs.items():
        if isinstance(in_value, str) and in_value.startswith('c.'):
            in_value = in_value.replace('c.', '')

            if in_value.startswith('[') and in_value.endswith(']'):
                task_inputs[in_key] = []

                for item_id in in_value[1:-1].split(','):
                    task_inputs[in_key].append(
                        catalog.get_item(item_id.strip())
                    )
            else:
                task_inputs[in_key] = catalog.get_item(in_value)
        else:
            task_inputs[in_key] = in_value

    return task_inputs


def build_task_outputs(outputs: List[str], returns: Any) -> Dict[str, Any]:
    """Builds the outputs of a task.

    Parameters
    ----------
    outputs : List[str]
        Outputs of the task. The outputs must match the returns in terms 
        of size.
    returns : Any
        Returns of the task obtained from its execution.

    Returns
    -------
    task_outputs : Dict[str, Any]
        Outputs of the task. The keys are the task outputs and the 
        values are the task returns obtained from the execution.

    Raises
    ------
    BuildingError
        Informs that the outputs_qty is not equal to the returns_qty.
    """

    task_outputs = {}
    outputs_qty = len(outputs)

    if outputs_qty > 0:
        if outputs_qty == 1:
            returns = [returns]

        try:
            returns_qty = len(returns)
        except TypeError:
            returns_qty = 1

        _check_diff_outputs_qty(outputs_qty, returns_qty)
        task_outputs = dict(zip(outputs, returns))

    return task_outputs


def _check_diff_outputs_qty(outputs_qty: int, returns_qty: int) -> None:
    """Checks if the quantity of outputs and returns is different.

    Parameters
    ----------
    outputs_qty : int
        Quantity of outputs.
    returns_qty : int
        Quantity of returns.

    Raises
    ------
    BuildingError
        Informs that the outputs_qty is not equal to the returns_qty.
    """

    if outputs_qty != returns_qty:
        raise BuildingError(
            'outputs_qty is not equal to the returns_qty', 
            [f'{outputs_qty} != {returns_qty}']
        )
