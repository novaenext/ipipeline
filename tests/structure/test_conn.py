from unittest import TestCase

from ipipeline.structure.conn import BaseConn, Conn


class TestBaseConn(TestCase):
    def test_init(self) -> None:
        base_conn = BaseConn('c1', 'n1', 'n2', tags=['data'])

        self.assertEqual(base_conn.id, 'c1')
        self.assertEqual(base_conn.src_id, 'n1')
        self.assertEqual(base_conn.dst_id, 'n2')
        self.assertEqual(base_conn.value, None)
        self.assertListEqual(base_conn.tags, ['data'])


class TestConn(TestCase):
    def test_new(self) -> None:
        conn = Conn('c1', 'n1', 'n2')

        self.assertIsInstance(conn, BaseConn)
