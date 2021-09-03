from itertools import chain
from typing import List

from ipipeline.exceptions import SequenceError


def flatten_nested_seq(seq: List[list]) -> list:
    try:
        return list(chain(*seq))
    except TypeError as error:
        raise SequenceError('seq not flattened', f'seq == {seq}') from error
