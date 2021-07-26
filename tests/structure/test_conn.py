from unittest import TestCase

from ipipeline.exceptions import InstanceError
from ipipeline.structure.conn import BaseConn, Conn


class TestBaseConn(TestCase):
    def test_init_valid_args(self) -> None:
        base_conn = BaseConn('c1', 'n1', 'n2', tags=['data'])

        self.assertEqual(base_conn.id, 'c1')
        self.assertEqual(base_conn.src_id, 'n1')
        self.assertEqual(base_conn.dst_id, 'n2')
        self.assertEqual(base_conn.weight, 0)
        self.assertListEqual(base_conn.tags, ['data'])

    def test_init_invalid_args(self) -> None:
        with self.assertRaisesRegex(
            InstanceError, 
            r'id_ does not match the pattern \(only letters, digits, '
            r'underscore and/or dash\): id_ == c1,'
        ):
            _ = BaseConn('c1,', 'n1', 'n2')

    def test_repr(self) -> None:
        base_conn = BaseConn('c1', 'n1', 'n2')
        instance_repr = base_conn.__repr__()

        self.assertEqual(
            instance_repr, 
            'BaseConn('
                'id_=\'c1\', '
                'src_id=\'n1\', '
                'dst_id=\'n2\', '
                'weight=0, '
                'tags=[]'
            ')'
        )


class TestConn(TestCase):
    def test_new_valid_args(self) -> None:
        conn = Conn('c1', 'n1', 'n2')
        
        self.assertIsInstance(conn, BaseConn)
