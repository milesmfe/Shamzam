import unittest
import json

from catalogue.controller import CatalogueController


def test_index():
    catalogue_controller = CatalogueController()
    result = catalogue_controller.index()
    assert result == {'message': 'Hello, World!'}
