from unittest import TestCase

from ipipeline.exceptions import (
    BaseError, 
    BuildingError, 
    CatalogError, 
    ExecutorError, 
    InfoError, 
    InstanceError, 
    PipelineError, 
    SortingError, 
    SystemError
)


class TestBaseError(TestCase):
    def test_init__text_eq_str__causes_eq_list(self) -> None:
        error = BaseError('error text', ['cause == item'])

        self.assertEqual(error._text, 'error text')
        self.assertListEqual(error._causes, ['cause == item'])

    def test_str__text_eq_str__causes_eq_empty_cause(self) -> None:
        error = BaseError('error text', [])
        msg = error.__str__()

        self.assertEqual(msg, 'error text: ')

    def test_str__text_eq_str__causes_eq_single_cause(self) -> None:
        error = BaseError('error text', ['cause == item'])
        msg = error.__str__()

        self.assertEqual(msg, 'error text: cause == item')

    def test_str__text_eq_str__causes_eq_multiple_causes(self) -> None:
        error = BaseError('error text', ['cause1 == item1', 'cause2 == item2'])
        msg = error.__str__()

        self.assertEqual(msg, 'error text: cause1 == item1, cause2 == item2')


class TestBuildingError(TestCase):
    def test_deriv(self) -> None:
        error = BuildingError('', '')

        self.assertIsInstance(error, BaseError)


class TestCatalogError(TestCase):
    def test_deriv(self) -> None:
        error = CatalogError('', '')

        self.assertIsInstance(error, BaseError)


class TestExecutorError(TestCase):
    def test_deriv(self) -> None:
        error = ExecutorError('', '')

        self.assertIsInstance(error, BaseError)


class TestInfoError(TestCase):
    def test_deriv(self) -> None:
        error = InfoError('', '')

        self.assertIsInstance(error, BaseError)


class TestInstanceError(TestCase):
    def test_deriv(self) -> None:
        error = InstanceError('', '')

        self.assertIsInstance(error, BaseError)


class TestPipelineError(TestCase):
    def test_deriv(self) -> None:
        error = PipelineError('', '')

        self.assertIsInstance(error, BaseError)


class TestSortingError(TestCase):
    def test_deriv(self) -> None:
        error = SortingError('', '')

        self.assertIsInstance(error, BaseError)


class TestSystemError(TestCase):
    def test_deriv(self) -> None:
        error = SystemError('', '')

        self.assertIsInstance(error, BaseError)
