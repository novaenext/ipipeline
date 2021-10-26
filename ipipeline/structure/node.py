"""Classes related to the node procedures."""

from abc import ABC
from typing import Any, Callable, Dict, List

from ipipeline.util.instance import Identification


class BaseNode(ABC, Identification):
    """Provides an interface to the node classes.

    Attributes
    ----------
    _id : str
        ID of the node.
    _func : Callable
        Function that performs a specific action.
    _inputs : Dict[str, Any]
        Inputs of the function. The keys are the function parameters and 
        the values are anything entered directly and/or obtained from the 
        catalog in the form of 'c.<item_id>'.
    _outputs : List[str]
        Outputs of the function. The outputs must match the returns in 
        terms of length. If one output is expected, the returns can be of 
        any type, however, in cases with more than one output, the returns 
        must be some type of sequence.
    _tags : List[str]
        Tags of the node to provide more context.
    """

    def __init__(
        self, 
        id: str, 
        func: Callable, 
        inputs: Dict[str, Any] = {}, 
        outputs: List[str] = [], 
        tags: List[str] = []
    ) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        id : str
            ID of the node.
        func : Callable
            Function that performs a specific action.
        inputs : Dict[str, Any], default={}
            Inputs of the function. The keys are the function parameters and 
            the values are anything entered directly and/or obtained from the 
            catalog in the form of 'c.<item_id>'.
        outputs : List[str], default=[]
            Outputs of the function. The outputs must match the returns in 
            terms of length. If one output is expected, the returns can be of 
            any type, however, in cases with more than one output, the returns 
            must be some type of sequence.
        tags : List[str], default=[]
            Tags of the node to provide more context.

        Raises
        ------
        InstanceError
            Informs that the id was not validated according to the pattern.
        """

        self._func = func
        self._inputs = inputs
        self._outputs = outputs

        super().__init__(id, tags=tags)

    @property
    def func(self) -> Callable:
        """Obtains the _func attribute.

        Returns
        -------
        func : Callable
            Function that performs a specific action.
        """

        return self._func

    @property
    def inputs(self) -> Dict[str, Any]:
        """Obtains the _inputs attribute.

        Returns
        -------
        inputs : Dict[str, Any]
            Inputs of the function. The keys are the function parameters and 
            the values are anything entered directly and/or obtained from the 
            catalog in the form of 'c.<item_id>'.
        """

        return self._inputs

    @property
    def outputs(self) -> List[str]:
        """Obtains the _outputs attribute.

        Returns
        -------
        outputs : List[str]
            Outputs of the function. The outputs must match the returns in 
            terms of length. If one output is expected, the returns can be of 
            any type, however, in cases with more than one output, the returns 
            must be some type of sequence.
        """

        return self._outputs


class Node(BaseNode):
    """Stores a function and its inputs and outputs.

    Attributes
    ----------
    _id : str
        ID of the node.
    _func : Callable
        Function that performs a specific action.
    _inputs : Dict[str, Any]
        Inputs of the function. The keys are the function parameters and 
        the values are anything entered directly and/or obtained from the 
        catalog in the form of 'c.<item_id>'.
    _outputs : List[str]
        Outputs of the function. The outputs must match the returns in 
        terms of length. If one output is expected, the returns can be of 
        any type, however, in cases with more than one output, the returns 
        must be some type of sequence.
    _tags : List[str]
        Tags of the node to provide more context.
    """

    pass
