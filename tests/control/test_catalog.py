from unittest import TestCase

from ipipeline.control.catalog import BaseCatalog, Catalog
from ipipeline.exceptions import CatalogError


class TestCatalog(TestCase):
    def test_new(self) -> None:
        catalog = Catalog()

        self.assertIsInstance(catalog, BaseCatalog)

    def test_add_item_inexistent_id(self) -> None:
        catalog = Catalog()
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7})

    def test_add_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 0, 'i2': 0}
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7, 'i2': 0})

    def test_check_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 0, 'i2': 0}
        checked = catalog.check_item('i1')

        self.assertTrue(checked)

    def test_check_item_inexistent_id(self) -> None:
        catalog = Catalog()
        checked = catalog.check_item('i1')

        self.assertFalse(checked)

    def test_obtain_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 7}
        item = catalog.obtain_item('i1')

        self.assertEqual(item, 7)

    def test_obtain_item_inexistent_id(self) -> None:
        catalog = Catalog()

        with self.assertRaisesRegex(
            CatalogError, r'id_ not found in the _items: id_ == i1'
        ):
            _ = catalog.obtain_item('i1')

    def test_remove_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 0, 'i2': 0}
        catalog.remove_item('i1')

        self.assertDictEqual(catalog.items, {'i2': 0})

    def test_remove_item_inexistent_id(self) -> None:
        catalog = Catalog()

        with self.assertRaisesRegex(
            CatalogError, r'id_ not found in the _items: id_ == i1'
        ):
            catalog.remove_item('i1')
