import re
from inspect import signature
from typing import List

from ipipeline.exception import InstanceError


class Identification:
    def __init__(self, id: str, tags: List[str] = []) -> None:
        self._id = self._check_valid_id(id)
        self._tags = tags

    @property
    def id(self) -> str:
        return self._id

    @property
    def tags(self) -> List[str]:
        return self._tags

    def _check_valid_id(self, id: str) -> str:
        if re.fullmatch(r'[\w-]+', id):
            return id
        else:
            raise InstanceError(
                'id not validated according to the pattern '
                '(letters, digits, underscore and/or dash)', 
                f'id == {id}'
            )

    def __repr__(self) -> str:
        return create_instance_repr(self)


def create_instance_repr(instance: object) -> str:
    instance_repr = f'{instance.__class__.__name__}('

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

        instance_repr += f'{param.name}={value}, '

    return f'{instance_repr})'.replace(', )', ')')
