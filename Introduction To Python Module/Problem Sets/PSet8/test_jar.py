import pytest
from jar import Jar


def test_init():
    jar = Jar()
    assert jar.capacity == 12  # default value
    jar2 = Jar(5)
    assert jar2.capacity == 5
    with pytest.raises(ValueError):
        Jar(-5)
    with pytest.raises(ValueError):
        Jar("string")


def test_str():
    jar = Jar()
    jar.deposit(5)
    assert str(jar) == "🍪🍪🍪🍪🍪"
    jar.deposit(2)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪"
    jar.withdraw(4)
    assert str(jar) == "🍪🍪🍪"


def test_deposit():
    jar = Jar(10)
    jar.deposit(5)
    assert jar.size == 5
    jar.deposit(3)
    assert jar.size == 8
    with pytest.raises(ValueError):
        jar.deposit(3)  # would exceed capacity
    with pytest.raises(ValueError):
        jar.deposit(-2)  # negative value not allowed


def test_withdraw():
    jar = Jar(10)
    jar.deposit(5)
    jar.withdraw(3)
    assert jar.size == 2
    with pytest.raises(ValueError):
        jar.withdraw(5)  # would exceed current size
    with pytest.raises(ValueError):
        jar.withdraw(-2)  # negative value not allowed
