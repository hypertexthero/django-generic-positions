"""Factories of the ``generic_positions`` app."""
import factory

from .test_app.models import DummyModel


class DummyModelFactory(factory.Factory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel

    name = 'Foobar'