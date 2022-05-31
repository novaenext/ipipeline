"""Class related to the node procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.structure.info import Info
from ipipeline.utils.checking import check_none


class Node(Info):
    """Stores a task and its inputs and outputs.

    Attributes
    ----------
    _id : str
        ID of the node.
    _task : Callable
        Task of the node.
    _inputs : Dict[str, Any], optional
        Inputs of the task. The keys are the callable parameters and the 
        items are the data required for the parameters. The items can also 
        be placeholders for the catalog items.

        Placeholders:
            'c.<item_id>': gets an item.
            'c.[<item_id>, ..., <item_id>]': gets a list of items.
    _outputs : List[str], optional
        Outputs of the task. The outputs must match the returns in terms 
        of size.
    _tags : List[str], optional
        Tags of the node to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        task: Callable, 
        inputs: Dict[str, Any] = None, 
        outputs: List[str] = None, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the node.
        task : Callable
            Task of the node.
        inputs : Dict[str, Any], optional
            Inputs of the task. The keys are the callable parameters and the 
            items are the data required for the parameters. The items can also 
            be placeholders for the catalog items.

            Placeholders:
                'c.<item_id>': gets an item.
                'c.[<item_id>, ..., <item_id>]': gets a list of items.
        outputs : List[str], optional
            Outputs of the task. The outputs must match the returns in terms 
            of size.
        tags : List[str], optional
            Tags of the node to provide more context.

        Raises
        ------
        InfoError
            Informs that the id did not match the pattern.
        """

        super().__init__(id, tags=tags)

        self._task = task
        self._inputs = check_none(inputs, {})
        self._outputs = check_none(outputs, [])

    @property
    def task(self) -> Callable:
        """Gets the _task attribute.

        Returns
        -------
        task : Callable
            Task of the node.
        """

        return self._task

    @property
    def inputs(self) -> Dict[str, Any]:
        """Gets the _inputs attribute.

        Returns
        -------
        inputs : Dict[str, Any]
            Inputs of the task. The keys are the callable parameters and the 
            items are the data required for the parameters. The items can also 
            be placeholders for the catalog items.

            Placeholders:
                'c.<item_id>': gets an item.
                'c.[<item_id>, ..., <item_id>]': gets a list of items.
        """

        return self._inputs

    @property
    def outputs(self) -> List[str]:
        """Gets the _outputs attribute.

        Returns
        -------
        outputs : List[str]
            Outputs of the task. The outputs must match the returns in terms 
            of size.
        """

        return self._outputs
