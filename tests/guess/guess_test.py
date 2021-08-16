import pandas.testing

from dumbpm.est.est import compute_duration
from dumbpm.est.est import compute_max_sprints
from dumbpm.est.est import compute_stats
from dumbpm.guess.guess import guesstimate


def test_compute_max_sprints() -> None:
    assert compute_max_sprints(scope=10, velocity=[6.0, 5.0], change=[1.0, 2.0]) == 4


def test_compute_max_sprints_max() -> None:
    assert compute_max_sprints(scope=10, velocity=[5.0, 1.0], change=[3.0, 1.0]) == 2000


def test_compute_duration() -> None:
    velocity = [1.0, 5.0, 5.0, 6.0, 8.0, 1.0]
    change = [1.0, -1.0, 2.0, 1.0, 1.0, 1.0]
    assert compute_duration(scope=10, velocity=velocity, change=change) == 4


def test_compute_duration_max_sprints() -> None:
    velocity = [1.0, 5.0, 5.0, 6.0, 8.0, 1.0]
    change = [1.0, -1.0, 5.0, 10.0, 10.0, 11.0]
    assert compute_duration(scope=10, velocity=velocity, change=change) == 6


def test_compute_duration_no_change() -> None:
    velocity = [1.0, 5.0, 5.0, 6.0, 8.0, 1.0]
    change = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert compute_duration(scope=10, velocity=velocity, change=change) == 3


def test_guesstimate() -> None:
    actual = guesstimate(
        task=["Task A", "Task B", "Task C", "Task D", "Task E", "Task F"],
        best=[5.0, 6.0, 1.0, 10.0, 5.0, 12.0],
        expected=[10.0, 12.0, 13.0, 13.0, 7.0, 25.0],
        worst=[20.0, 40.0, 24.0, 15.0, 12.0, 34.0],
        simulations=10,
        random_seed=1234,
    )
    expected = compute_stats([19, 19, 24, 21, 16, 23, 19, 22, 16, 21])
    pandas.testing.assert_frame_equal(expected, actual)


def test_estimate_normal() -> None:
    actual = estimate(
        scope=100,
        velocity=[5.0, 6.0, 10.0],
        change=[1.0, 2.0, 3.0],
        normal=True,
        simulations=10,
        random_seed=1234,
    )
    expected = compute_stats([21, 18, 17, 22, 19, 20, 23, 18, 19, 18])
    pandas.testing.assert_frame_equal(expected, actual)


def test_estimate_no_changes() -> None:
    actual = estimate(
        scope=100,
        velocity=[5.0, 6.0, 10.0],
        change=[0, 0, 0],
        normal=False,
        simulations=10,
        random_seed=1234,
    )
    expected = compute_stats([15, 16, 13, 14, 16, 17, 14, 16, 13, 14])
    pandas.testing.assert_frame_equal(expected, actual)


def test_estimate_normal_no_changes() -> None:
    actual = estimate(
        scope=100,
        velocity=[5.0, 6.0, 10.0],
        change=[0, 0, 0],
        normal=True,
        simulations=10,
        random_seed=1234,
    )
    expected = compute_stats([14, 14, 15, 13, 12, 13, 15, 14, 15, 13])
    pandas.testing.assert_frame_equal(expected, actual)
