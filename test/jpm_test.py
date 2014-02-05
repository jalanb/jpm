"""Test the jpm package"""


import jpm


def test_doc():
    assert getattr(jpm, '__doc__', None) is not None
