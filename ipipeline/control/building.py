from typing import Any, Dict, List

from ipipeline.exceptions import BuildingError


def build_func_inputs(
    inputs: Dict[str, Any], items: Dict[str, Any]
) -> Dict[str, Any]:
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
    if outputs_qty != returns_qty:
        raise BuildingError(
            'outputs_qty is not equal to the returns_qty', 
            f'{outputs_qty} != {returns_qty}'
        )
