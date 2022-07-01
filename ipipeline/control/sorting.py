"""Functions related to the sorting procedures."""

from typing import Dict, List

from ipipeline.exceptions import SortingError


def sort_topology(graph: Dict[str, list]) -> List[list]:
    """Sorts the graph topology to find a linear ordering of the nodes.

    The topological ordering depends on a directed acyclic graph and its 
    order is not necessarily unique.

    Parameters
    ----------
    graph : Dict[str, list]
        Graph of the pipeline. The keys are the source node IDs and the 
        values are the lists of destination node IDs.

    Returns
    -------
    ordering : List[list]
        Ordering of the graph. The inner lists represent groups of nodes 
        that must be executed sequentially and the nodes within these 
        groups can be executed simultaneously.

    Raises
    ------
    SortingError
        Informs that the dst_id was not set as a src_id.
    SortingError
        Informs that a circular dependency was found in the graph.

    Notes
    -----
        Based on the Kahn's algorithm.
    """

    ordering = []
    incomings_qty = _get_incomings_qty(graph)
    unbound_ids = _get_unbound_ids(incomings_qty)

    while unbound_ids:
        tmp_ids = []
        ordering.append(unbound_ids)

        for src_id in unbound_ids:
            del incomings_qty[src_id]

            for dst_id in graph[src_id]:
                incomings_qty[dst_id] -= 1

                if incomings_qty[dst_id] == 0:
                    tmp_ids.append(dst_id)

        unbound_ids = tmp_ids

    if incomings_qty:
        raise SortingError(
            'circular dependency was found in the graph', 
            [f'incomings_qty == {incomings_qty}']
        )

    return ordering


def _get_incomings_qty(graph: Dict[str, list]) -> Dict[str, int]:
    """Gets the quantity of incoming links for each node.

    Parameters
    ----------
    graph : Dict[str, list]
        Graph of the pipeline. The keys are the source node IDs and the 
        values are the lists of destination node IDs.

    Returns
    -------
    incomings_qty : Dict[str, int]
        Quantity of incoming links for each node. The keys are the node IDs 
        and the values are the quantity of incoming links.

    Raises
    ------
    SortingError
        Informs that the dst_id was not set as a src_id.
    """

    incomings_qty = dict.fromkeys(graph.keys(), 0)

    for dst_ids in graph.values():
        for dst_id in dst_ids:
            try:
                incomings_qty[dst_id] += 1
            except KeyError as error:
                raise SortingError(
                    'dst_id was not set as a src_id', [f'dst_id == {dst_id}']
                ) from error

    return incomings_qty


def _get_unbound_ids(incomings_qty: Dict[str, int]) -> List[str]:
    """Gets the node IDs that has no incoming links.

    Parameters
    ----------
    incomings_qty : Dict[str, int]
        Quantity of incoming links for each node. The keys are the node IDs 
        and the values are the quantity of incoming links.

    Returns
    -------
    unbound_ids : List[str]
        IDs of the nodes that has no incoming links.
    """

    unbound_ids = []

    for id, in_qty in incomings_qty.items():
        if in_qty == 0:
            unbound_ids.append(id)

    return unbound_ids
