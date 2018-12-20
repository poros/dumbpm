import pytest

from dumbpm.prio import actual_value
from dumbpm.prio import any_negative
from dumbpm.prio import normalize
from dumbpm.prio import parse_input
from dumbpm.prio import prioritize


def test_actual_value() -> None:
    assert actual_value(10, 5, 6, 10) == 5 / (10 * 6) + 10


def test_normalize() -> None:
    assert normalize([5, 6, 1, 2, 4, 10]) == [0.5, 0.6, 0.1, 0.2, 0.4, 1]


def test_any_negative() -> None:
    assert not any_negative([1, 2, 3, 4, 0])
    assert any_negative([0, -1, 3])


def test_parse_input_negative() -> None:
    with pytest.raises(ValueError):
        parse_input([0, -1, 3])


def test_parse_input() -> None:
    inp = [0, 1.0, 3.0]
    assert parse_input(inp) == inp


def test_prioritize() -> None:
    projects = ["A", "B", "C", "D"]
    value = [10.0, 10.0, 10.0, 10.0]
    cost = [10.0, 10.0, 10.0, 10.0]
    duration = [10.0, 10.0, 10.0, 10.0]
    rigging = [0.0, 10.0, 0.0, 1.0]
    max_cost = 20.0
    assert prioritize(projects, cost, value, duration, rigging, max_cost) == [
        ["B", "D"]
    ]
