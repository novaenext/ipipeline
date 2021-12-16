from unittest import TestCase

from ipipeline.exception import CatalogError
from ipipeline.structure.catalog import Catalog


class TestCatalog(TestCase):
    def test_init(self) -> None:
        catalog = Catalog('c1', tags=['data'])

        self.assertEqual(catalog.id, 'c1')
        self.assertDictEqual(catalog.items, {})
        self.assertListEqual(catalog.tags, ['data'])

    def test_defaults(self) -> None:
        catalog1 = Catalog('c1')
        catalog2 = Catalog('c2')

        self.assertIsNot(catalog1.items, catalog2.items)

    def test_add_inexistent_item(self) -> None:
        catalog = Catalog('c1')
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7})

    def test_add_existent_item(self) -> None:
        catalog = Catalog('c1', items={'i1': 0, 'i2': 0})
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7, 'i2': 0})

    def test_check_existent_item(self) -> None:
        catalog = Catalog('c1', items={'i1': 7, 'i2': 0})
        checked = catalog.check_item('i1')

        self.assertTrue(checked)

    def test_check_inexistent_item(self) -> None:
        catalog = Catalog('c1')
        checked = catalog.check_item('i1')

        self.assertFalse(checked)

    def test_obtain_existent_item(self) -> None:
        catalog = Catalog('c1', items={'i1': 7, 'i2': 0})
        item = catalog.obtain_item('i1')

        self.assertEqual(item, 7)

    def test_obtain_inexistent_item(self) -> None:
        catalog = Catalog('c1')

        with self.assertRaisesRegex(
            CatalogError, r'id not found in the _items: id == i1'
        ):
            _ = catalog.obtain_item('i1')

    def test_remove_existent_item(self) -> None:
        catalog = Catalog('c1', items={'i1': 7, 'i2': 0})
        catalog.remove_item('i1')

        self.assertDictEqual(catalog.items, {'i2': 0})

    def test_remove_inexistent_item(self) -> None:
        catalog = Catalog('c1')

        with self.assertRaisesRegex(
            CatalogError, r'id not found in the _items: id == i1'
        ):
            catalog.remove_item('i1')

    def test_clean_existent_items(self) -> None:
        catalog = Catalog('c1', items={'i1': 7, 'i2': 0})
        catalog.clean_items()

        self.assertDictEqual(catalog.items, {})

    def test_clean_inexistent_items(self) -> None:
        catalog = Catalog('c1')
        catalog.clean_items()

        self.assertDictEqual(catalog.items, {})
