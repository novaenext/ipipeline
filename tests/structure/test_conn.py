from unittest import TestCase

from ipipeline.structure.conn import Conn


class TestConn(TestCase):
    def test_init(self) -> None:
        conn = Conn('c1', 'n1', 'n2', tags=['data'])

        self.assertEqual(conn.id, 'c1')
        self.assertEqual(conn.src_id, 'n1')
        self.assertEqual(conn.dst_id, 'n2')
        self.assertEqual(conn.power, None)
        self.assertListEqual(conn.tags, ['data'])

    def test_defaults(self) -> None:
        conn1 = Conn('c1', 'n1', 'n2')
        conn2 = Conn('c2', 'n2', 'n3')

        self.assertIs(conn1.power, conn2.power)
