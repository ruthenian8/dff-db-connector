import pytest

from dff_db_connector.dff_db_connector import DffDbConnector, DffAbstractConnector


def test_main():
    assert issubclass(DffDbConnector, DffAbstractConnector)
