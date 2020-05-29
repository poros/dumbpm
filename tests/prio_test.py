from typing import List
from typing import Tuple

from dumbpm.prio import combined_value
from dumbpm.prio import compute_actual_value
from dumbpm.prio import Item
from dumbpm.prio import normalize
from dumbpm.prio import prioritize
from dumbpm.prio import tot_value


def test_combined_value() -> None:
    assert combined_value(5, 10, 6, 3) == 5 / (10 * 6 * 3)
    assert combined_value(1, 0, 0, 0) == 1


def test_normalize() -> None:
    assert normalize([5, 6, 1, 2, 4, 10]) == [0.5, 0.6, 0.1, 0.2, 0.4, 1]


def test_compute_actual_value() -> None:
    value = [10.0, 20.0]
    cost = [10.0, 20.0]
    duration = [10.0, 20.0]
    risk = [3.0, 6.0]
    rigging = [1.0, 5.0]

    assert compute_actual_value(value, cost, duration, risk, rigging) == [1.2, 1.25]


def test_tot_value() -> None:
    assert tot_value((Item("A", 1, 1), Item("B", 2, 1), Item("C", 3, 1)), 3) == 6.0
    assert tot_value((Item("A", 1, 1), Item("B", 2, 1), Item("C", 3, 1)), 2) == 0.0


def test_prioritize() -> None:
    projects = ["A", "B", "C", "D"]
    value = [10.0, 10.0, 10.0, 10.0]
    cost = [10.0, 10.0, 10.0, 10.0]
    duration = [10.0, 10.0, 10.0, 10.0]
    risk = [3.0, 3.0, 3.0, 3.0]
    rigging = [0.0, 10.0, 0.0, 1.0]
    alternatives: List[Tuple[str, ...]] = [(), (), (), ()]
    max_cost = 20.0
    assert prioritize(
        projects,
        value,
        cost,
        duration,
        risk,
        rigging,
        alternatives,
        max_cost,
        duration_cost_budget=False,
    ) == ["B", "D"]


def test_prioritize_duration_cost_budget() -> None:
    projects = ["A", "B", "C", "D"]
    value = [100.0, 20.0, 100.0, 10.0]
    cost = [10.0, 10.0, 10.0, 10.0]
    duration = [10.0, 10.0, 50.0, 10.0]
    multiplied_cost = [100.0, 100.0, 500.0, 100.0]
    unit_duration = [1.0, 1.0, 1.0, 1.0]
    risk = [3.0, 3.0, 3.0, 3.0]
    rigging = [0.0, 0.0, 0.0, 0.0]
    alternatives: List[Tuple[str, ...]] = [(), (), (), ()]
    max_cost = 200.0
    assert (
        prioritize(
            projects,
            value,
            cost,
            duration,
            risk,
            rigging,
            alternatives,
            max_cost,
            duration_cost_budget=True,
        )
        == prioritize(
            projects,
            value,
            multiplied_cost,
            unit_duration,
            risk,
            rigging,
            alternatives,
            max_cost,
            duration_cost_budget=False,
        )
        == ["A", "B"]
    )


def test_prioritize_with_alternatives() -> None:
    projects = ["A", "B", "C", "D"]
    value = [10.0, 10.0, 10.0, 10.0]
    cost = [10.0, 10.0, 10.0, 10.0]
    duration = [10.0, 10.0, 10.0, 10.0]
    risk = [3.0, 3.0, 3.0, 3.0]
    rigging = [0.0, 10.0, 0.1, 1.0]
    alternatives: List[Tuple[str, ...]] = [(), ("D",), (), ("B",)]
    max_cost = 20.0
    assert prioritize(
        projects,
        value,
        cost,
        duration,
        risk,
        rigging,
        alternatives,
        max_cost,
        duration_cost_budget=False,
    ) == ["B", "C"]
