from unittest import TestCase

from ipipeline.exceptions import CatalogError
from ipipeline.structure.catalog import Catalog


class TestCatalog(TestCase):
    def setUp(self) -> None:
        self._items = {'i1': 2, 'i2': 4}

    def test_init__items_eq_dict(self) -> None:
        catalog = Catalog('c1', items=self._items, tags=['t1'])

        self.assertEqual(catalog._id, 'c1')
        self.assertDictEqual(catalog._items, self._items)
        self.assertListEqual(catalog._tags, ['t1'])

    def test_get__items_eq_dict(self) -> None:
        catalog = Catalog('c1', items=self._items, tags=['t1'])

        self.assertEqual(catalog.id, 'c1')
        self.assertDictEqual(catalog.items, self._items)
        self.assertListEqual(catalog.tags, ['t1'])

    def test_set__items_eq_dict(self) -> None:
        catalog = Catalog('c1', items=self._items, tags=['t1'])
        catalog.id = 'c2'
        catalog.items = {'i3': 8}
        catalog.tags = ['t2']

        self.assertEqual(catalog.id, 'c2')
        self.assertDictEqual(catalog.items, {'i3': 8})
        self.assertListEqual(catalog.tags, ['t2'])

    def test_check_item__id_eq_id(self) -> None:
        catalog = Catalog('c1', items=self._items)
        checked = catalog.check_item('i1')

        self.assertTrue(checked)

    def test_check_item__id_ne_id(self) -> None:
        catalog = Catalog('c1', items=None)
        checked = catalog.check_item('i1')

        self.assertFalse(checked)

    def test_get_item__id_eq_id(self) -> None:
        catalog = Catalog('c1', items=self._items)
        item = catalog.get_item('i1')

        self.assertEqual(item, 2)

    def test_get_item__id_ne_id(self) -> None:
        catalog = Catalog('c1', items=None)

        with self.assertRaisesRegex(
            CatalogError, r'id was not found in the _items: id == i1'
        ):
            _ = catalog.get_item('i1')

    def test_set_item__id_eq_id(self) -> None:
        catalog = Catalog('c1', items=self._items)
        catalog.set_item('i1', 8)

        self.assertDictEqual(catalog.items, {'i1': 8, 'i2': 4})

    def test_set_item__id_ne_id(self) -> None:
        catalog = Catalog('c1', items=None)
        catalog.set_item('i1', 2)

        self.assertDictEqual(catalog.items, {'i1': 2})

    def test_remove_existent_item(self) -> None:
        catalog = Catalog('c1', items={'i1': 7, 'i2': 0}, tags=None)
        catalog.remove_item('i1')

        self.assertDictEqual(catalog.items, {'i2': 0})

    def test_remove_inexistent_item(self) -> None:
        catalog = Catalog('c1', items=None, tags=None)

        with self.assertRaisesRegex(
            CatalogError, r'id not found in the _items: id == i1'
        ):
            catalog.remove_item('i1')
