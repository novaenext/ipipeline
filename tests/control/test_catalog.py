from unittest import TestCase

from ipipeline.exceptions import CatalogError
from ipipeline.control.catalog import BaseCatalog, Catalog


class MockBaseCatalog(BaseCatalog):
    def add_item(self) -> None:
        pass

    def update_item(self) -> None:
        pass

    def check_item(self) -> None:
        pass
   
    def obtain_item(self) -> None:
        pass

    def remove_item(self) -> None:
        pass


class TestBaseCatalog(TestCase):
    def test_init_valid_args(self) -> None:
        base_catalog = MockBaseCatalog()

        self.assertDictEqual(base_catalog.items, {})


class TestCatalog(TestCase):
    def test_new_valid_args(self) -> None:
        catalog = Catalog()
        
        self.assertIsInstance(catalog, BaseCatalog)

    def test_add_item_inexistent_id(self) -> None:
        catalog = Catalog()
        catalog.add_item('i1', {'x': 7})

        self.assertDictEqual(catalog.items, {'i1': {'x': 7}})

    def test_add_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': {'x': 0}}
        catalog.add_item('i1', {'x': 7})

        self.assertDictEqual(catalog.items, {'i1': {'x': 7}})

    def test_update_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': {'x': 0, 'y': 7}}
        catalog.update_item('i1', {'x': 7, 'z': 7})

        self.assertDictEqual(catalog.items, {'i1': {'x': 7, 'y': 7, 'z': 7}})

    def test_update_item_inexistent_id(self) -> None:
        catalog = Catalog()

        with self.assertRaisesRegex(CatalogError, r'id_ not found: id_ == i1'):
            catalog.update_item('i1', {'x': 7, 'z': 7})

    def test_check_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': {'x': 0}}
        checked = catalog.check_item('i1')

        self.assertTrue(checked)

    def test_check_item_inexistent_id(self) -> None:
        catalog = Catalog()
        checked = catalog.check_item('i1')

        self.assertFalse(checked)

    def test_obtain_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': {'x': 7}}
        item = catalog.obtain_item('i1')

        self.assertDictEqual(item, {'x': 7})

    def test_obtain_item_inexistent_id(self) -> None:
        catalog = Catalog()

        with self.assertRaisesRegex(CatalogError, r'id_ not found: id_ == i1'):
            _ = catalog.obtain_item('i1')

    def test_remove_item_existent_id(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': {'x': 7}, 'i2': {'x': 7}}
        catalog.remove_item('i1')

        self.assertDictEqual(catalog.items, {'i2': {'x': 7}})

    def test_remove_item_inexistent_id(self) -> None:
        catalog = Catalog()

        with self.assertRaisesRegex(CatalogError, r'id_ not found: id_ == i1'):
            catalog.remove_item('i1')
