class BaseError(Exception):
    def __init__(self, descr: str, detail: str) -> None:  
        self._descr = descr
        self._detail = detail

    def __str__(self) -> str:
        return f'{self._descr}: {self._detail}'


class NodeError(BaseError):
    pass


class PipelineError(BaseError):
    pass


class InstanceError(BaseError):
    pass
