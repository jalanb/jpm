"""Test the jpm package"""


import jpm


def test_doc():
    assert getattr(jpm, '__doc__', None) is not None


def test_version():
    assert jpm.__version__ > '0.0.0'
