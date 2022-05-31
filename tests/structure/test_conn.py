from unittest import TestCase

from ipipeline.structure.conn import Conn


class TestConn(TestCase):
    def test_init__src_node_id_eq_str__dst_node_id_eq_str(self) -> None:
        conn = Conn('c1', 'n1', 'n2', tags=['t1'])

        self.assertEqual(conn.id, 'c1')
        self.assertEqual(conn.src_node_id, 'n1')
        self.assertEqual(conn.dst_node_id, 'n2')
        self.assertListEqual(conn.tags, ['t1'])
