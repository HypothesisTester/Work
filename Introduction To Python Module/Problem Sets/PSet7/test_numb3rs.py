import pytest
from numb3rs import validate  # Import function under test


def test_valid_ip():
    assert validate("127.0.0.1")
    assert validate("255.255.255.255")


def test_invalid_ip():
    assert not validate("512.512.512.512")
    assert not validate("1.2.3.1000")
    assert not validate("cat")
