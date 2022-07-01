"""Class related to the node procedures."""

from typing import Callable, Dict, List

from ipipeline.structure.info import Info
from ipipeline.utils.checking import check_none


class Node(Info):
    """Stores a task.

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
        Outputs of the task. The outputs must match the returns in terms 
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
            Outputs of the task. The outputs must match the returns in terms 
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
