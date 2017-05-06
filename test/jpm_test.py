"""Test the jpm package"""


import jpm


def test_doc():
    assert jpm.__doc__


def test_version():
    assert jpm.__version__ > '0.0.0'
