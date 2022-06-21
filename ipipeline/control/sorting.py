"""Functions related to the sorting procedures."""

from typing import Dict, List

from ipipeline.exceptions import SortingError


def sort_graph_topo(graph: Dict[str, list]) -> List[list]:
    """Sorts the graph topology to find its topological order.

    The graph must be acyclic to be able to obtain its topological order 
    that is not necessarily unique. 

    Parameters
    ----------
    graph : Dict[str, list]
        Graph of the pipeline. The keys are the source node IDs and the 
        values are a list of destination node IDs.

    Returns
    -------
    topo_order : List[list]
        Topological order of the graph. The inner lists represent groups 
        of nodes that must be executed in order and the nodes within these 
        groups can be executed simultaneously.

    Raises
    ------
    SortingError
        Informs that the dst_node_id was not specified as a src_node_id.
    SortingError
        Informs that a circular dependency was found in the graph.

    Notes
    -----
        Based on the Kahn algorithm.
    """

    topo_order = []
    ind_nodes_qty = 0
    in_conns_qty = _get_incomings_qty(graph)
    ind_node_ids = _find_ind_node_ids(in_conns_qty)

    while ind_node_ids:
        cand_node_ids = []
        topo_order.append(ind_node_ids)

        for src_node_id in ind_node_ids:
            for dst_node_id in graph[src_node_id]:
                in_conns_qty[dst_node_id] -= 1

                if in_conns_qty[dst_node_id] == 0:
                    cand_node_ids.append(dst_node_id)

            ind_nodes_qty += 1
        ind_node_ids = cand_node_ids
    _check_circular_dependency(len(graph.keys()), ind_nodes_qty)

    return topo_order


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


def _find_ind_node_ids(in_conns_qty: Dict[str, int]) -> List[str]:
    """Finds the IDs of the independent nodes.

    An independent node is a node that has no incoming connections.

    Parameters
    ----------
    in_conns_qty : Dict[str, int]
        Quantity of incoming connections for each node. The keys are the 
        node IDs and the values are the quantity of incoming connections.

    Returns
    -------
    ind_node_ids : List[str]
        IDs of the independent nodes.
    """

    ind_node_ids = []

    for node_id, in_qty in in_conns_qty.items():
        if in_qty == 0:
            ind_node_ids.append(node_id)

    return ind_node_ids


def _check_circular_dependency(nodes_qty: int, ind_nodes_qty: int) -> None:
    """Checks for a circular dependency.

    The circular dependency prevents the formation of the topological order.

    Parameters
    ----------
    nodes_qty : int
        Quantity of nodes.
    ind_nodes_qty : int
        Quantity of independent nodes.

    Raises
    ------
    SortingError
        Informs that a circular dependency was found in the graph.
    """

    if nodes_qty != ind_nodes_qty:
        raise SortingError(
            'circular dependency found in the graph', 
            [f'{nodes_qty} != {ind_nodes_qty}']
        )
