import unittest
import json

from lookup.controller import LookupController


def test_index():
    lookup_controller = LookupController()
    result = lookup_controller.index()
    assert result == {'message': 'Hello, World!'}
