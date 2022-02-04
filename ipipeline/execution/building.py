"""Functions related to the building procedures."""

from typing import Any, Dict, List

from ipipeline.exceptions import BuildingError
from ipipeline.structure.catalog import Catalog


def build_task_inputs(
    inputs: Dict[str, Any], catalog: Catalog
) -> Dict[str, Any]:
    """Builds the inputs of a task.

    Parameters
    ----------
    inputs : Dict[str, Any]
        Inputs of the task. The keys are the function parameters and 
        the values are any default values and/or placeholders for the 
        catalog items.

        'c.<item_id>': obtains a single item.
        'c.[<item_id>, ..., <item_id>]': obtains multiple items.
    catalog : Catalog
        Catalog that stores the items from an execution.

    Returns
    -------
    task_inputs : Dict[str, Any]
        Inputs of the task. The keys are the function parameters and 
        the values are any default values and/or items obtained from the 
        catalog.

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
                        catalog.obtain_item(item_id.strip())
                    )
            else:
                task_inputs[in_key] = catalog.obtain_item(in_value)
        else:
            task_inputs[in_key] = in_value

    return task_inputs


def build_task_outputs(outputs: List[str], returns: Any) -> Dict[str, Any]:
    """Builds the outputs of a task.

    Parameters
    ----------
    outputs : List[str]
        Outputs of the task. The outputs must match the returns in 
        terms of length. If one output is expected, the return can be of 
        any type, however, in cases with more than one output, the returns 
        must be a sequence.
    returns : Any
        Returns of the task obtained from its execution.

    Returns
    -------
    task_outputs : Dict[str, Any]
        Outputs of the task. The keys are the outputs and the values 
        are the returns obtained from the execution.

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
            f'{outputs_qty} != {returns_qty}'
        )
