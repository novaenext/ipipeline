from unittest import TestCase

from ipipeline.exceptions import SequenceError
from ipipeline.utils.sequence import flatten_nested_list


class TestFlattenNestedList(TestCase):
    def test_nested_list(self) -> None:
        flattened_list = flatten_nested_list([['n1'], ['n4', 'n3'], ['n2']])

        self.assertListEqual(flattened_list, ['n1', 'n4', 'n3', 'n2'])

    def test_unnested_list(self) -> None:
        with self.assertRaisesRegex(
            SequenceError, 
            r'nested list not flattened: nested_list == \[1, 7\]'
        ):
            _ = flatten_nested_list([1, 7])
