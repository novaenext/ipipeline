from typing import Dict, List

from ..exceptions import SortingError


def _create_ind_node_ids(in_conns_qty: Dict[str, int]) -> List[str]:
    ind_node_ids = []

    for node_id, in_qty in in_conns_qty.items():
        if in_qty == 0:
            ind_node_ids.append(node_id)

    return ind_node_ids


def _check_diff_nodes_qty(exp_nodes_qty: int, curr_nodes_qty: int) -> None:
    if exp_nodes_qty != curr_nodes_qty:
        raise SortingError(
            'circular dependency found', f'curr_nodes_qty == {curr_nodes_qty}'
        )
