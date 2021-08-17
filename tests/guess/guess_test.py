import numpy as np
import pandas.testing

from dumbpm.guess.guess import compute_beta_dist_params
from dumbpm.guess.guess import guesstimate
from dumbpm.guess.guess import ThreePointEstimate
from dumbpm.shared import compute_stats


def test_compute_beta_dist_params() -> None:
    est = ThreePointEstimate(best=10, expected=20, worst=60)
    params = compute_beta_dist_params(est)
    np.testing.assert_allclose(params.a, 1.5)  # type: ignore
    np.testing.assert_allclose(params.b, 3.0)  # type: ignore
    np.testing.assert_allclose(params.loc, 10)  # type: ignore
    np.testing.assert_allclose(params.scale, 50)  # type: ignore


def test_guesstimate() -> None:
    actual = guesstimate(
        task=["Task A", "Task B", "Task C", "Task D", "Task E", "Task F"],
        best=[5, 6, 1, 10, 5, 12],
        expected=[10, 12, 13, 13, 7, 25],
        worst=[20, 40, 24, 15, 12, 34],
        simulations=10,
        random_seed=1234,
    )
    expected = compute_stats([88, 92, 82, 93, 80, 97, 84, 95, 102, 86])
    pandas.testing.assert_frame_equal(expected, actual)
