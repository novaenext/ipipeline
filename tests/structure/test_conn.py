from unittest import TestCase

from ipipeline.structure.conn import Conn


class TestConn(TestCase):
    def test_init__src_id_eq_str__dst_id_eq_str(self) -> None:
        conn = Conn('c1', 'n1', 'n2', tags=['t1'])

        self.assertEqual(conn._id, 'c1')
        self.assertEqual(conn._src_id, 'n1')
        self.assertEqual(conn._dst_id, 'n2')
        self.assertListEqual(conn._tags, ['t1'])

    def test_get__src_id_eq_str__dst_id_eq_str(self) -> None:
        conn = Conn('c1', 'n1', 'n2', tags=['t1'])

        self.assertEqual(conn.src_id, 'n1')
        self.assertEqual(conn.dst_id, 'n2')

    def test_set__src_id_eq_str__dst_id_eq_str(self) -> None:
        conn = Conn('c1', 'n1', 'n2', tags=['t1'])
        conn.src_id = 'n3'
        conn.dst_id = 'n4'

        self.assertEqual(conn.src_id, 'n3')
        self.assertEqual(conn.dst_id, 'n4')
