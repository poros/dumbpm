from dumbpm.prio import actual_value
from dumbpm.prio import normalize
from dumbpm.prio import prioritize


def test_actual_value() -> None:
    assert actual_value(10, 5, 6, 10) == 5 / (10 * 6) + 10


def test_normalize() -> None:
    assert normalize([5, 6, 1, 2, 4, 10]) == [0.5, 0.6, 0.1, 0.2, 0.4, 1]


def test_prioritize() -> None:
    projects = ["A", "B", "C", "D"]
    value = [10.0, 10.0, 10.0, 10.0]
    cost = [10.0, 10.0, 10.0, 10.0]
    duration = [10.0, 10.0, 10.0, 10.0]
    rigging = [0.0, 10.0, 0.0, 1.0]
    max_cost = 20.0
    assert prioritize(projects, cost, value, duration, rigging, max_cost) == ["B", "D"]
