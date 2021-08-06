import re
from inspect import signature
from typing import List

from ipipeline.exceptions import InstanceError


class InstanceIdentifier:
    def __init__(self, id_: str, tags: List[str] = []) -> None:
        self._id = self._check_id(id_)
        self._tags = tags

    @property
    def id(self) -> str:
        return self._id

    @property
    def tags(self) -> List[str]:
        return self._tags

    def _check_id(self, id_: str) -> str:
        if re.fullmatch(r'[\w-]+', id_):
            return id_
        else:
            raise InstanceError(
                'id_ does not match the pattern '
                '(only letters, digits, underscore and/or dash)',
                f'id_ == {id_}'
            )


def create_instance_repr(instance: object) -> str:
    param_reprs = []

    for param in signature(instance.__init__).parameters.values():
        value = None

        for attr in [
            f'_{param.name}', param.name, 
            f'_{param.name[:-1]}', param.name[:-1]
        ]:
            if attr in instance.__dict__:
                value = getattr(instance, attr)

                if isinstance(value, str):
                    value = f'\'{value}\''

                break

        param_reprs.append(f'{param.name}={value}')

    return f'{instance.__class__.__name__}({", ".join(param_reprs)})'
