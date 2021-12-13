from unittest import TestCase

from ipipeline.structure.signal import BaseSignal, Signal


class TestBaseSignal(TestCase):
    def test_init(self) -> None:
        base_signal = BaseSignal(
            's1', 
            'e1', 
            'skip', 
            True, 
            tags=['data']
        )

        self.assertEqual(base_signal.id, 's1')
        self.assertEqual(base_signal.elem_id, 'e1')
        self.assertEqual(base_signal.type, 'skip')
        self.assertEqual(base_signal.status, True)
        self.assertListEqual(base_signal.tags, ['data'])


class TestSignal(TestCase):
    def test_deriv(self) -> None:
        signal = Signal('s1', 'e1', 'skip', True)

        self.assertIsInstance(signal, BaseSignal)
