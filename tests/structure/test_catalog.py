from unittest import TestCase

from ipipeline.exception import CatalogError
from ipipeline.structure.catalog import BaseCatalog, Catalog


class MockBaseCatalog(BaseCatalog):
    def add_item(self) -> None:
        pass

    def check_item(self) -> None:
        pass
   
    def obtain_item(self) -> None:
        pass

    def remove_item(self) -> None:
        pass

    def clean_items(self) -> None:
        pass


class TestBaseCatalog(TestCase):
    def test_init(self) -> None:
        base_catalog = MockBaseCatalog('c1', tags=['data'])

        self.assertEqual(base_catalog.id, 'c1')
        self.assertDictEqual(base_catalog.items, {})
        self.assertListEqual(base_catalog.tags, ['data'])


class TestCatalog(TestCase):
    def test_deriv(self) -> None:
        catalog = Catalog('c1')

        self.assertIsInstance(catalog, BaseCatalog)

    def test_add_inexistent_item(self) -> None:
        catalog = Catalog('c1')
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7})

    def test_add_existent_item(self) -> None:
        catalog = Catalog('c1')
        catalog._items = {'i1': 0, 'i2': 0}
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7, 'i2': 0})

    def test_check_existent_item(self) -> None:
        catalog = Catalog('c1')
        catalog._items = {'i1': 0, 'i2': 0}
        checked = catalog.check_item('i1')

        self.assertTrue(checked)

    def test_check_inexistent_item(self) -> None:
        catalog = Catalog('c1')
        checked = catalog.check_item('i1')

        self.assertFalse(checked)

    def test_obtain_existent_item(self) -> None:
        catalog = Catalog('c1')
        catalog._items = {'i1': 7}
        item = catalog.obtain_item('i1')

        self.assertEqual(item, 7)

    def test_obtain_inexistent_item(self) -> None:
        catalog = Catalog('c1')

        with self.assertRaisesRegex(
            CatalogError, r'id not found in the _items: id == i1'
        ):
            _ = catalog.obtain_item('i1')

    def test_remove_existent_item(self) -> None:
        catalog = Catalog('c1')
        catalog._items = {'i1': 0, 'i2': 0}
        catalog.remove_item('i1')

        self.assertDictEqual(catalog.items, {'i2': 0})

    def test_remove_inexistent_item(self) -> None:
        catalog = Catalog('c1')

        with self.assertRaisesRegex(
            CatalogError, r'id not found in the _items: id == i1'
        ):
            catalog.remove_item('i1')

    def test_clean_existent_items(self) -> None:
        catalog = Catalog('c1')
        catalog._items = {'i1': 0, 'i2': 0}
        catalog.clean_items()

        self.assertDictEqual(catalog.items, {})

    def test_clean_inexistent_items(self) -> None:
        catalog = Catalog('c1')
        catalog.clean_items()

        self.assertDictEqual(catalog.items, {})
