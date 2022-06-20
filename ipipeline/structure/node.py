"""Class related to the node procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.structure.info import Info
from ipipeline.utils.checking import check_none


class Node(Info):
    """Stores an executable unit of the graph.

    Attributes
    ----------
    _id : str
        ID of the node.
    _task : Callable
        Task of the node.
    _inputs : Dict[str, Any], optional
        Inputs of the task. The keys are the callable parameters and the 
        values are the data required for the parameters. The values can also 
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
            values are the data required for the parameters. The values can 
            also be placeholders for the catalog items.

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

    @task.setter
    def task(self, task: Callable) -> None:
        """Sets the _task attribute.

        Parameters
        ----------
        task : Callable
            Task of the node.
        """

        self._task = task

    @property
    def inputs(self) -> Dict[str, Any]:
        """Gets the _inputs attribute.

        Returns
        -------
        inputs : Dict[str, Any]
            Inputs of the task. The keys are the callable parameters and the 
            values are the data required for the parameters. The values can 
            also be placeholders for the catalog items.

            Placeholders:
                'c.<item_id>': gets an item.
                'c.[<item_id>, ..., <item_id>]': gets a list of items.
        """

        return self._inputs

    @inputs.setter
    def inputs(self, inputs: Dict[str, Any]) -> None:
        """Sets the _inputs attribute.

        Parameters
        ----------
        inputs : Dict[str, Any]
            Inputs of the task. The keys are the callable parameters and the 
            values are the data required for the parameters. The values can 
            also be placeholders for the catalog items.

            Placeholders:
                'c.<item_id>': gets an item.
                'c.[<item_id>, ..., <item_id>]': gets a list of items.
        """

        self._inputs = inputs

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

    @outputs.setter
    def outputs(self, outputs: List[str]) -> None:
        """Sets the _outputs attribute.

        Parameters
        ----------
        outputs : List[str]
            Outputs of the task. The outputs must match the returns in terms 
            of size.
        """

        self._outputs = outputs
