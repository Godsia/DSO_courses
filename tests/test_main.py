"""Tests for main module."""

import pytest

from src.app.main import add, greet, multiply


def test_add():
    """Test add function."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_multiply():
    """Test multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5
    assert multiply(0, 10) == 0


def test_greet():
    """Test greet function."""
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"


@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (5, 5, 10), (-1, 1, 0)])
def test_add_parametrized(a, b, expected):
    """Parametrized test for add."""
    assert add(a, b) == expected

