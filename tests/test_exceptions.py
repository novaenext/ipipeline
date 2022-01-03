from unittest import TestCase

from ipipeline.exceptions import (
    BaseError, 
    BuildingError, 
    CatalogError, 
    ExecutionError, 
    InfoError, 
    InstanceError, 
    PipelineError, 
    SortingError, 
    SystemError
)


class TestBaseError(TestCase):
    def test_init(self) -> None:
        error = BaseError('error descr', 'error == value')

        self.assertEqual(error._descr, 'error descr')
        self.assertEqual(error._detail, 'error == value')

    def test_str(self) -> None:
        error = BaseError('error descr', 'error == value')
        error_msg = error.__str__()

        self.assertEqual(error_msg, 'error descr: error == value')


class TestBuildingError(TestCase):
    def test_deriv(self) -> None:
        error = BuildingError('', '')

        self.assertIsInstance(error, BaseError)


class TestCatalogError(TestCase):
    def test_deriv(self) -> None:
        error = CatalogError('', '')

        self.assertIsInstance(error, BaseError)


class TestExecutionError(TestCase):
    def test_deriv(self) -> None:
        error = ExecutionError('', '')

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
