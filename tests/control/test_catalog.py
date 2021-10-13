from unittest import TestCase

from ipipeline.control.catalog import BaseCatalog, Catalog
from ipipeline.exception import CatalogError


class MockBaseCatalog(BaseCatalog):
    def add_item(self) -> None:
        pass

    def check_item(self) -> None:
        pass
   
    def obtain_item(self) -> None:
        pass

    def remove_item(self) -> None:
        pass


class TestBaseCatalog(TestCase):
    def test_init(self) -> None:
        base_catalog = MockBaseCatalog()

        self.assertDictEqual(base_catalog.items, {})


class TestCatalog(TestCase):
    def test_deriv(self) -> None:
        catalog = Catalog()

        self.assertIsInstance(catalog, BaseCatalog)

    def test_add_inexistent_item(self) -> None:
        catalog = Catalog()
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7})

    def test_add_existent_item(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 0, 'i2': 0}
        catalog.add_item('i1', 7)

        self.assertDictEqual(catalog.items, {'i1': 7, 'i2': 0})

    def test_check_existent_item(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 0, 'i2': 0}
        checked = catalog.check_item('i1')

        self.assertTrue(checked)

    def test_check_inexistent_item(self) -> None:
        catalog = Catalog()
        checked = catalog.check_item('i1')

        self.assertFalse(checked)

    def test_obtain_existent_item(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 7}
        item = catalog.obtain_item('i1')

        self.assertEqual(item, 7)

    def test_obtain_inexistent_item(self) -> None:
        catalog = Catalog()

        with self.assertRaisesRegex(
            CatalogError, r'id_ not found in the _items: id_ == i1'
        ):
            _ = catalog.obtain_item('i1')

    def test_remove_existent_item(self) -> None:
        catalog = Catalog()
        catalog._items = {'i1': 0, 'i2': 0}
        catalog.remove_item('i1')

        self.assertDictEqual(catalog.items, {'i2': 0})

    def test_remove_inexistent_item(self) -> None:
        catalog = Catalog()

        with self.assertRaisesRegex(
            CatalogError, r'id_ not found in the _items: id_ == i1'
        ):
            catalog.remove_item('i1')
