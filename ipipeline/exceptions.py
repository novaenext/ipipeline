"""Classes related to the exception procedures.

The exceptions are bound to a module rather than a specific error. To 
inform about the specifications of an error the parameters must be used.
"""

class BaseError(Exception):
    """Informs the occurrence of an error related to the ipipeline package.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    def __init__(self, descr: str, detail: str) -> None:
        """Initializes the attributes.

        Parameters
        ----------
        descr : str
            Description of the error.
        detail : str
            Detail of the error represented as a valid expression.
        """

        self._descr = descr
        self._detail = detail

    def __str__(self) -> str:
        """Obtains the error message.

        Returns
        -------
        error_msg : str
            Error message.
        """

        return f'{self._descr}: {self._detail}'


class BuildingError(BaseError):
    """Informs the occurrence of an error related to the building module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass


class CatalogError(BaseError):
    """Informs the occurrence of an error related to the catalog module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass


class ExecutorError(BaseError):
    """Informs the occurrence of an error related to the executors module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass


class InfoError(BaseError):
    """Informs the occurrence of an error related to the info module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass


class InstanceError(BaseError):
    """Informs the occurrence of an error related to the instance module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass


class PipelineError(BaseError):
    """Informs the occurrence of an error related to the pipeline module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass


class SortingError(BaseError):
    """Informs the occurrence of an error related to the sorting module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass


class SystemError(BaseError):
    """Informs the occurrence of an error related to the system module.

    Attributes
    ----------
    _descr : str
        Description of the error.
    _detail : str
        Detail of the error represented as a valid expression.
    """

    pass
