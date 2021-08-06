from itertools import chain
from typing import List

from ipipeline.exceptions import SequenceError


def flatten_nested_list(nested_list: List[list]) -> list:
    try:
        return list(chain(*nested_list))
    except TypeError as error:
        raise SequenceError(
            'nested list not flattened', f'nested_list == {nested_list}'
        ) from error
