"""Functions related to the building procedures."""

from typing import Any, Dict, List

from ipipeline.exception import BuildingError
from ipipeline.structure.catalog import BaseCatalog


def build_func_inputs(
    inputs: Dict[str, Any], catalog: BaseCatalog
) -> Dict[str, Any]:
    """Builds the inputs of a function.

    Parameters
    ----------
    inputs : Dict[str, Any]
        Inputs of the function. The keys are the function parameters and 
        the values are any default values and/or items obtained from the 
        catalog through a specific syntax.

        'c.<item_id>': syntax to obtain a single item.
        'c.[<item_id>, ..., <item_id>]': syntax to obtain a list of items.
    catalog : BaseCatalog
        Catalog that stores the items from the execution.

    Returns
    -------
    func_inputs : Dict[str, Any]
        Inputs of the function built according to the default values 
        and/or the items obtained from the catalog. The keys are the 
        function parameters and the values are the function arguments.

    Raises
    ------
    CatalogError
        Informs that the id was not found in the _items.
    """

    func_inputs = {}

    for in_key, in_value in inputs.items():
        if isinstance(in_value, str) and in_value.startswith('c.'):
            in_value = in_value.replace('c.', '')

            if in_value.startswith('[') and in_value.endswith(']'):
                func_inputs[in_key] = []

                for item_id in in_value[1:-1].split(','):
                    func_inputs[in_key].append(
                        catalog.obtain_item(item_id.strip())
                    )
            else:
                func_inputs[in_key] = catalog.obtain_item(in_value)
        else:
            func_inputs[in_key] = in_value

    return func_inputs


def build_func_outputs(outputs: List[str], returns: Any) -> Dict[str, Any]:
    """Builds the outputs of a function.

    Parameters
    ----------
    outputs : List[str]
        Outputs of the function. The outputs must match the returns in 
        terms of length. If one output is expected, the returns can be of 
        any type, however, in cases with more than one output, the returns 
        must be some type of sequence.
    returns : Any
        Returns of the function obtained from its execution.

    Returns
    -------
    func_outputs : Dict[str, Any]
        Outputs of the function built according to the combination of the 
        outputs and returns. The keys are the outputs and the values are 
        the returns.

    Raises
    ------
    BuildingError
        Informs that the outputs_qty is not equal to the returns_qty.
    """

    func_outputs = {}
    outputs_qty = len(outputs)

    if outputs_qty > 0:
        if outputs_qty == 1:
            returns = [returns]

        try:
            returns_qty = len(returns)
        except TypeError:
            returns_qty = 1

        _check_diff_outputs_qty(outputs_qty, returns_qty)
        func_outputs = dict(zip(outputs, returns))

    return func_outputs


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
