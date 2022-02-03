from unittest import TestCase

from ipipeline.structure.signal import Signal


class TestSignal(TestCase):
    def test_init(self) -> None:
        signal = Signal('s1', 'n1', 'skip', status=True, tags=['t1'])

        self.assertEqual(signal.id, 's1')
        self.assertEqual(signal.node_id, 'n1')
        self.assertEqual(signal.type, 'skip')
        self.assertEqual(signal.status, True)
        self.assertListEqual(signal.tags, ['t1'])

    def test_defaults(self) -> None:
        signal1 = Signal('s1', 'n1', 'skip')
        signal2 = Signal('s2', 'n2', 'skip')

        self.assertIs(signal1.status, signal2.status)
