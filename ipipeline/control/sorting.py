from typing import Dict, List

from ..exceptions import SortingError


def _create_in_conns_qty(graph: Dict[str, list]) -> Dict[str, int]:
    in_conns_qty = dict.fromkeys(graph, 0)

    for dst_node_ids in graph.values():
        for dst_node_id in dst_node_ids:
            try:
                in_conns_qty[dst_node_id] += 1
            except KeyError as error:
                raise SortingError(
                    'dst_node_id without src_node_id', 
                    f'dst_node_id == {dst_node_id}'
                ) from error

    return in_conns_qty


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
