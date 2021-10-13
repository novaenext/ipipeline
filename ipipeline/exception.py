class BaseError(Exception):
    def __init__(self, descr: str, detail: str) -> None:  
        self._descr = descr
        self._detail = detail

    def __str__(self) -> str:
        return f'{self._descr}: {self._detail}'


class ActionError(BaseError):
    pass


class BuildingError(BaseError):
    pass


class CatalogError(BaseError):
    pass


class ExecutionError(BaseError):
    pass


class InstanceError(BaseError):
    pass


class PipelineError(BaseError):
    pass


class SortingError(BaseError):
    pass


class SystemError(BaseError):
    pass