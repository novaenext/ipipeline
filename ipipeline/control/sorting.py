from ..exceptions import SortingError


def _check_diff_nodes_qty(exp_nodes_qty: int, curr_nodes_qty: int) -> None:
    if exp_nodes_qty != curr_nodes_qty:
        raise SortingError(
            'circular dependency found', f'curr_nodes_qty == {curr_nodes_qty}'
        )
