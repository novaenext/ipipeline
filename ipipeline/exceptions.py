"""Classes related to the exception procedures.

The exceptions are bound to a module rather than a specific error. To 
inform about the specifications of an error the parameters must be used.
"""

from typing import List


class BaseError(Exception):
    """Informs the occurrence of an error related to the ipipeline package.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    def __init__(self, text: str, causes: List[str]) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        text : str
            Text of the error.
        causes : List[str]
            Causes of the error.
        """

        self._text = text
        self._causes = causes

    def __str__(self) -> str:
        """Builds the error message.

        Returns
        -------
        msg : str
            Message of the error.
        """

        return f'{self._text}: {", ".join(self._causes)}'


class BuildingError(BaseError):
    """Informs the occurrence of an error related to the building module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass


class CatalogError(BaseError):
    """Informs the occurrence of an error related to the catalog module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass


class ExecutorError(BaseError):
    """Informs the occurrence of an error related to the executors module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass


class InfoError(BaseError):
    """Informs the occurrence of an error related to the info module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass


class InstanceError(BaseError):
    """Informs the occurrence of an error related to the instance module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass


class PipelineError(BaseError):
    """Informs the occurrence of an error related to the pipeline module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass


class SortingError(BaseError):
    """Informs the occurrence of an error related to the sorting module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass


class SystemError(BaseError):
    """Informs the occurrence of an error related to the system module.

    Attributes
    ----------
    _text : str
        Text of the error.
    _causes : List[str]
        Causes of the error.
    """

    pass
