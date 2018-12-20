import pytest

from dumbpm.parse import any_negative
from dumbpm.parse import parse_input


def test_any_negative() -> None:
    assert not any_negative([1, 2, 3, 4, 0])
    assert any_negative([0, -1, 3])


def test_parse_input_negative() -> None:
    with pytest.raises(ValueError):
        parse_input([0, -1, 3])


def test_parse_input() -> None:
    inp = [0, 1.0, 3.0]
    assert parse_input(inp) == inp
