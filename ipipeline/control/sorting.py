"""Functions related to the sorting procedures."""

from typing import Dict, List

from ipipeline.exception import SortingError


def sort_graph_topo(graph: Dict[str, list]) -> List[list]:
    """Sorts the graph topology to find its topological order.

    The graph must be a directed acyclic graph from which the topological 
    (not necessarily unique) order can be obtained. This implementation is 
    based on the Kahn algorithm.

    Parameters
    ----------
    graph : Dict[str, list]
        Graph of the pipeline. The keys are the IDs of the source nodes 
        and the values are the dependencies formed by the IDs of the 
        destination nodes.

    Returns
    -------
    topo_order : List[list]
        Topological order of the graph. The inner lists represent groups 
        of nodes where the groups must be executed in order and the nodes 
        within them can be processed simultaneously.

    Raises
    ------
    SortingError
        Informs that the dst_node_id was not specified as src_node_id.
    SortingError
        Informs that a circular dependency was found in the graph.
    """

    topo_order = []
    ind_nodes_qty = 0
    in_conns_qty = _obtain_in_conns_qty(graph)
    ind_node_ids = _find_ind_node_ids(in_conns_qty)

    while ind_node_ids:
        next_node_ids = []
        topo_order.append(ind_node_ids)

        for src_node_id in ind_node_ids:
            for dst_node_id in graph[src_node_id]:
                in_conns_qty[dst_node_id] -= 1

                if in_conns_qty[dst_node_id] == 0:
                    next_node_ids.append(dst_node_id)

            ind_nodes_qty += 1
        ind_node_ids = next_node_ids
    _check_diff_nodes_qty(len(graph.keys()), ind_nodes_qty)

    return topo_order


def _obtain_in_conns_qty(graph: Dict[str, list]) -> Dict[str, int]:
    """Obtains the quantity of incoming connections for each node in the graph.

    Parameters
    ----------
    graph : Dict[str, list]
        Graph of the pipeline. The keys are the IDs of the source nodes 
        and the values are the dependencies formed by the IDs of the 
        destination nodes.

    Returns
    -------
    in_conns_qty : Dict[str, int]
        Quantity of incoming connections for each node in the graph. The 
        keys are the node IDs and the values are the quantity of incoming 
        connections.

    Raises
    ------
    SortingError
        Informs that the dst_node_id was not specified as src_node_id.
    """

    in_conns_qty = dict.fromkeys(graph.keys(), 0)

    for dst_node_ids in graph.values():
        for dst_node_id in dst_node_ids:
            try:
                in_conns_qty[dst_node_id] += 1
            except KeyError as error:
                raise SortingError(
                    'dst_node_id not specified as src_node_id', 
                    f'dst_node_id == {dst_node_id}'
                ) from error

    return in_conns_qty


def _find_ind_node_ids(in_conns_qty: Dict[str, int]) -> List[str]:
    """Finds the IDs of the independent nodes.

    Independent nodes are nodes that have no incoming connections, which 
    suggests no dependencies.

    Parameters
    ----------
    in_conns_qty : Dict[str, int]
        Quantity of incoming connections for each node in the graph. The 
        keys are the node IDs and the values are the quantity of incoming 
        connections.

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


def _check_diff_nodes_qty(nodes_qty: int, ind_nodes_qty: int) -> None:
    """Checks if the quantity of nodes and independent nodes is different.

    The difference between these quantities represents the detection of a 
    cycle that consists of a path from a node back to itself. Therefore, 
    this situation prevents the graph from being traversed.

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
            f'{nodes_qty} != {ind_nodes_qty}'
        )
