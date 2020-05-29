from typing import List
from typing import Tuple

import numpy as np
import pytest

from dumbpm.prio import combine_cost_and_duration
from dumbpm.prio import compute_score
from dumbpm.prio import Item
from dumbpm.prio import norm
from dumbpm.prio import prioritize
from dumbpm.prio import total_score


def test_norm() -> None:
    assert norm([5, 6, 1, 2, 4, 10]) == [0.5, 0.6, 0.1, 0.2, 0.4, 1]


def test_combine_score_and_duration() -> None:
    cost = [0.5, 1.0]
    duration = [1, 0.2]
    assert combine_cost_and_duration(cost, duration) == ([0.5, 0.2], [0.0, 0.0])


def test_compute_score() -> None:
    value = [10.0, 20.0]
    cost = [20.0, 10.0]
    duration = [20.0, 10.0]
    risk = [3.0, 6.0]
    rigging = [1.0, 5.0]

    np.testing.assert_array_almost_equal(
        compute_score(value, cost, duration, risk, rigging), [0.6, 2.0]
    )


def test_compute_score_div_by_zero() -> None:
    value = [10.0, 20.0]
    cost = [20.0, 0.0]
    duration = [20.0, 0.0]
    risk = [3.0, 0.0]
    rigging = [1.0, 5.0]
    with pytest.raises(ValueError):
        compute_score(value, cost, duration, risk, rigging)


def test_total_score() -> None:
    assert total_score((Item("A", 1, 1), Item("B", 2, 1), Item("C", 3, 1)), 3) == 6.0
    assert total_score((Item("A", 1, 1), Item("B", 2, 1), Item("C", 3, 1)), 2) == 0.0


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
        cost_per_duration=False,
    ) == ["B", "D"]


def test_prioritize_cost_per_duration() -> None:
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
            cost_per_duration=True,
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
            cost_per_duration=False,
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
        cost_per_duration=False,
    ) == ["B", "C"]
