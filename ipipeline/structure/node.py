"""Class related to the node procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.exceptions import NodeError
from ipipeline.structure.catalog import Catalog
from ipipeline.structure.info import Info
from ipipeline.utils.checking import check_none


class Node(Info):
    """Stores a task with its inputs and outputs.

    Attributes
    ----------
    _id : str
        ID of the node.
    _task : Callable
        Task of the node.
    _pos_inputs : List[str]
        Positional inputs of the task. The elements are the IDs of the 
        catalog items.
    _key_inputs : Dict[str, str]
        Keyword inputs of the task. The keys are the task parameters and 
        the values are the IDs of the catalog items.
    _outputs : List[str]
        Outputs of the task. The outputs must match the results in terms 
        of size.
    _tags : List[str]
        Tags of the node to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        task: Callable, 
        pos_inputs: List[str] = None, 
        key_inputs: Dict[str, str] = None, 
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
        pos_inputs : List[str], optional
            Positional inputs of the task. The elements are the IDs of the 
            catalog items.
        key_inputs : Dict[str, str], optional
            Keyword inputs of the task. The keys are the task parameters and 
            the values are the IDs of the catalog items.
        outputs : List[str], optional
            Outputs of the task. The outputs must match the results in terms 
            of size.
        tags : List[str], optional
            Tags of the node to provide more context.
        """

        super().__init__(id, tags=tags)

        self._task = task
        self._pos_inputs = check_none(pos_inputs, [])
        self._key_inputs = check_none(key_inputs, {})
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
    def pos_inputs(self) -> List[str]:
        """Gets the _pos_inputs attribute.

        Returns
        -------
        pos_inputs : List[str]
            Positional inputs of the task. The elements are the IDs of the 
            catalog items.
        """

        return self._pos_inputs

    @pos_inputs.setter
    def pos_inputs(self, pos_inputs: List[str]) -> None:
        """Sets the _pos_inputs attribute.

        Parameters
        ----------
        pos_inputs : List[str]
            Positional inputs of the task. The elements are the IDs of the 
            catalog items.
        """

        self._pos_inputs = pos_inputs

    @property
    def key_inputs(self) -> Dict[str, str]:
        """Gets the _key_inputs attribute.

        Returns
        -------
        key_inputs : Dict[str, str]
            Keyword inputs of the task. The keys are the task parameters and 
            the values are the IDs of the catalog items.
        """

        return self._key_inputs

    @key_inputs.setter
    def key_inputs(self, key_inputs: Dict[str, str]) -> None:
        """Sets the _key_inputs attribute.

        Parameters
        ----------
        key_inputs : Dict[str, str]
            Keyword inputs of the task. The keys are the task parameters and 
            the values are the IDs of the catalog items.
        """

        self._key_inputs = key_inputs

    @property
    def outputs(self) -> List[str]:
        """Gets the _outputs attribute.

        Returns
        -------
        outputs : List[str]
            Outputs of the task. The outputs must match the results in terms 
            of size.
        """

        return self._outputs

    @outputs.setter
    def outputs(self, outputs: List[str]) -> None:
        """Sets the _outputs attribute.

        Parameters
        ----------
        outputs : List[str]
            Outputs of the task. The outputs must match the results in terms 
            of size.
        """

        self._outputs = outputs

    def build_pos_args(self, catalog: Catalog) -> List[Any]:
        """Builds the positional arguments of a task.

        Parameters
        ----------
        catalog : Catalog
            Catalog that stores the items of an execution.

        Returns
        -------
        pos_args : List[Any]
            Positional arguments of a task.
        """

        pos_args = []

        for item_id in self._pos_inputs:
            pos_args.append(catalog.get_item(item_id))

        return pos_args

    def build_key_args(self, catalog: Catalog) -> Dict[str, Any]:
        """Builds the keyword arguments of a task.

        Parameters
        ----------
        catalog : Catalog
            Catalog that stores the items of an execution.

        Returns
        -------
        key_args : Dict[str, Any]
            Keyword arguments of a task.
        """

        key_args = {}

        for param, item_id in self._key_inputs.items():
            key_args[param] = catalog.get_item(item_id)

        return key_args

    def execute_task(
        self, pos_args: List[Any], key_args: Dict[str, Any]
    ) -> Any:
        """Executes a task.

        Parameters
        ----------
        pos_args : List[Any]
            Positional arguments of a task.
        key_args : Dict[str, Any]
            Keyword arguments of a task.

        Returns
        -------
        results : Any
            Results generated by the task execution.

        Raises
        ------
        NodeError
            Informs that the task was not executed.
        """

        try:
            results = self._task(*pos_args, **key_args)

            return results
        except Exception as error:
            raise NodeError(
                'task was not executed', [f'id == {self._id}']
            ) from error

    def build_items(self, results: Any) -> Dict[str, Any]:
        """Builds the items of an execution.

        Parameters
        ----------
        results : Any
            Results generated by the task execution.

        Returns
        -------
        items : Dict[str, Any]
            Items of an execution. The keys are the item IDs and the values 
            are the arguments required by the tasks.

        Raises
        ------
        NodeError
            Informs that an invalid type was found for the results.
        NodeError
            Informs that the _outputs did not match the results in terms of 
            size.
        """

        items = {}

        if len(self._outputs) > 0:
            if len(self._outputs) == 1:
                results = [results]

            if not isinstance(results, (list, tuple)):
                raise NodeError(
                    'invalid type was found for the results', 
                    [f'type == {type(results)}']
                )

            if len(self._outputs) != len(results):
                raise NodeError(
                    '_outputs did not match the results in terms of size', 
                    [f'{len(self._outputs)} != {len(results)}']
                )

            items = dict(zip(self._outputs, results))

        return items
