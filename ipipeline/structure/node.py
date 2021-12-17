"""Class related to the node procedures."""

from typing import Any, Callable, Dict, List

from ipipeline.structure.info import Info
from ipipeline.util.instance import check_none_arg


class Node(Info):
    """Stores a function and its specifications.

    The specifications are used to build the inputs and outputs to execute 
    the function that is bound to the node.

    Attributes
    ----------
    _id : str
        ID of the node.
    _func : Callable
        Function that represents an execution unit.
    _inputs : Dict[str, Any]
        Inputs of the function. The keys are the function parameters and 
        the values are any default values and/or placeholders for the 
        catalog items.

        'c.<item_id>': obtains a single item.
        'c.[<item_id>, ..., <item_id>]': obtains multiple items.
    _outputs : List[str]
        Outputs of the function. The outputs must match the returns in 
        terms of length. If one output is expected, the return can be of 
        any type, however, in cases with more than one output, the returns 
        must be a sequence.
    _tags : List[str]
        Tags of the node to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        func: Callable, 
        inputs: Dict[str, Any] = None, 
        outputs: List[str] = None, 
        tags: List[str] = None
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the node.
        func : Callable
            Function that represents an execution unit.
        inputs : Dict[str, Any], default=None
            Inputs of the function. The keys are the function parameters and 
            the values are any default values and/or placeholders for the 
            catalog items.

            'c.<item_id>': obtains a single item.
            'c.[<item_id>, ..., <item_id>]': obtains multiple items.
        outputs : List[str], default=None
            Outputs of the function. The outputs must match the returns in 
            terms of length. If one output is expected, the return can be of 
            any type, however, in cases with more than one output, the returns 
            must be a sequence.
        tags : List[str], default=None
            Tags of the node to provide more context.

        Raises
        ------
        InfoError
            Informs that the id was not validated according to the pattern.
        """

        self._func = func
        self._inputs = check_none_arg(inputs, {})
        self._outputs = check_none_arg(outputs, [])

        super().__init__(id, tags=tags)

    @property
    def func(self) -> Callable:
        """Obtains the _func attribute.

        Returns
        -------
        func : Callable
            Function that represents an execution unit.
        """

        return self._func

    @property
    def inputs(self) -> Dict[str, Any]:
        """Obtains the _inputs attribute.

        Returns
        -------
        inputs : Dict[str, Any]
            Inputs of the function. The keys are the function parameters and 
            the values are any default values and/or placeholders for the 
            catalog items.

            'c.<item_id>': obtains a single item.
            'c.[<item_id>, ..., <item_id>]': obtains multiple items.
        """

        return self._inputs

    @property
    def outputs(self) -> List[str]:
        """Obtains the _outputs attribute.

        Returns
        -------
        outputs : List[str]
            Outputs of the function. The outputs must match the returns in 
            terms of length. If one output is expected, the return can be of 
            any type, however, in cases with more than one output, the returns 
            must be a sequence.
        """

        return self._outputs
