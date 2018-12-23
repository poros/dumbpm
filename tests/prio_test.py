from typing import List
from typing import Tuple

from dumbpm.prio import actual_value
from dumbpm.prio import Item
from dumbpm.prio import normalize
from dumbpm.prio import prioritize
from dumbpm.prio import tot_value


def test_actual_value() -> None:
    assert actual_value(10, 5, 6, 10) == 5 / (10 * 6) + 10


def test_normalize() -> None:
    assert normalize([5, 6, 1, 2, 4, 10]) == [0.5, 0.6, 0.1, 0.2, 0.4, 1]


def test_tot_value() -> None:
    assert tot_value((Item("A", 1, 1), Item("B", 2, 1), Item("C", 3, 1)), 3) == 6.0
    assert tot_value((Item("A", 1, 1), Item("B", 2, 1), Item("C", 3, 1)), 2) == 0.0


def test_prioritize() -> None:
    projects = ["A", "B", "C", "D"]
    value = [10.0, 10.0, 10.0, 10.0]
    cost = [10.0, 10.0, 10.0, 10.0]
    duration = [10.0, 10.0, 10.0, 10.0]
    rigging = [0.0, 10.0, 0.0, 1.0]
    alternatives = [(), (), (), ()]
    max_cost = 20.0
    assert prioritize(
        projects, cost, value, duration, rigging, alternatives, max_cost
    ) == ["B", "D"]


def test_prioritize_with_alternatives() -> None:
    projects = ["A", "B", "C", "D"]
    value = [10.0, 10.0, 10.0, 10.0]
    cost = [10.0, 10.0, 10.0, 10.0]
    duration = [10.0, 10.0, 10.0, 10.0]
    rigging = [0.0, 10.0, 0.1, 1.0]
    alternatives: List[Tuple[str, ...]] = [(), ("D",), (), ("B",)]
    max_cost = 20.0
    assert prioritize(
        projects, cost, value, duration, rigging, alternatives, max_cost
    ) == ["B", "C"]
