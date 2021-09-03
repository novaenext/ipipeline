from unittest import TestCase

from ipipeline.exceptions import SequenceError
from ipipeline.utils.sequence import flatten_nested_seq


class TestFlattenNestedSeq(TestCase):
    def test_nested_seq(self) -> None:
        flattened_seq = flatten_nested_seq([['n1'], ['n4', 'n3'], ['n2']])

        self.assertListEqual(flattened_seq, ['n1', 'n4', 'n3', 'n2'])

    def test_unnested_seq(self) -> None:
        with self.assertRaisesRegex(
            SequenceError, r'seq not flattened: seq == \[1, 7\]'
        ):
            _ = flatten_nested_seq([1, 7])
