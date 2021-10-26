"""Functions related to the building procedures."""

from typing import Any, Dict, List

from ipipeline.exception import BuildingError


def build_func_inputs(
    inputs: Dict[str, Any], items: Dict[str, Any]
) -> Dict[str, Any]:
    """Builds the inputs of a function.

    Parameters
    ----------
    inputs : Dict[str, Any]
        Inputs of the function. The keys are the function parameters and 
        the values are anything entered directly and/or obtained from the 
        catalog in the form of 'c.<item_id>'.
    items : Dict[str, Any]
        Items obtained from the executions. The keys are the item IDs 
        obtained from the outputs and the values are the items obtained 
        from the returns.

    Returns
    -------
    func_inputs : Dict[str, Any]
        Inputs of the function built according to the values entered 
        directly and/or obtained from the catalog. The keys are the 
        function parameters and the values are anything specified by 
        the parameters.

    Raises
    ------
    BuildingError
        Informs that the in_value was not found in the items.
    """

    func_inputs = {}

    for in_key, in_value in inputs.items():
        if isinstance(in_value, str) and in_value.startswith('c.'):
            try:
                func_inputs[in_key] = items[in_value.replace('c.', '')]
            except KeyError as error:
                raise BuildingError(
                    'in_value not found in the items', 
                    f'in_value == {in_value}'
                ) from error
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
