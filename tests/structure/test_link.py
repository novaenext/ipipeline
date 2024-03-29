from unittest import TestCase

from ipipeline.structure.link import Link


class TestLink(TestCase):
    def test_init__args_eq_types(self) -> None:
        link = Link('l1', 'n1', 'n2', tags=['t1'])

        self.assertEqual(link._id, 'l1')
        self.assertEqual(link._src_id, 'n1')
        self.assertEqual(link._dst_id, 'n2')
        self.assertListEqual(link._tags, ['t1'])

    def test_get__args_eq_types(self) -> None:
        link = Link('l1', 'n1', 'n2', tags=['t1'])

        self.assertEqual(link.id, 'l1')
        self.assertEqual(link.src_id, 'n1')
        self.assertEqual(link.dst_id, 'n2')
        self.assertListEqual(link.tags, ['t1'])

    def test_set__args_eq_types(self) -> None:
        link = Link('l1', 'n1', 'n2', tags=['t1'])
        link.id = 'l2'
        link.src_id = 'n3'
        link.dst_id = 'n4'
        link.tags = ['t2']

        self.assertEqual(link.id, 'l2')
        self.assertEqual(link.src_id, 'n3')
        self.assertEqual(link.dst_id, 'n4')
        self.assertListEqual(link.tags, ['t2'])
