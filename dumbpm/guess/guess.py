from typing import Callable
from typing import NamedTuple
from typing import Optional

from numpy.random import default_rng
from pandas import DataFrame
from scipy.stats import beta

from dumbpm.shared import compute_stats


class ThreePointEstimate(NamedTuple):
    best: int
    expected: int
    worst: int


class BetaParams(NamedTuple):
    a: float
    b: float
    loc: int
    scale: int


def compute_beta_dist_params(est: ThreePointEstimate) -> BetaParams:
    # A lower lambda value than the usual 4 gives more probability to the values
    # closer to the extremes, reducing the peakedness of the curve.
    # Given that we have a very low confidence at this stage of planning and that we
    # are using a Monte Carlo simulation to compensate that, it makes sense to lower it.
    # Wikipedia says the usual values for modified PERT go from 2 to 3.5.
    lamb = 2.5
    loc = est.best
    scale = est.worst - est.best
    # in case it's a flat line with all three estimates matching
    # monotonicity it's already checked at parsing time, so no issue here
    if est.best == est.worst:
        a = 1.0
        b = 1.0
    else:
        a = 1 + lamb * (est.expected - est.best) / (est.worst - est.best)
        b = 1 + lamb * (est.worst - est.expected) / (est.worst - est.best)
    return BetaParams(a, b, loc, scale)


def generate_project_simulator(
    task: list[str],
    best: list[int],
    expected: list[int],
    worst: list[int],
    random_seed: Optional[int],
) -> Callable[[], int]:
    """Simulate the velocity and the scope change for the sprints in the simulation."""
    estimates = [ThreePointEstimate(*x) for x in zip(best, expected, worst)]
    # The PERT distribution is not available in numpy as a class, but it is an
    # application of the beta distribution
    parameters = [compute_beta_dist_params(est) for est in estimates]
    rng = default_rng(random_seed)
    perts = [beta(a=p.a, b=p.b, loc=p.loc, scale=p.scale) for p in parameters]

    def simulate_project() -> int:
        rvs = [pert.rvs(random_state=rng).round(0) for pert in perts]
        return sum(rvs)

    return simulate_project


def guesstimate(
    task: list[str],
    best: list[int],
    expected: list[int],
    worst: list[int],
    simulations: int,
    random_seed: Optional[int] = None,
) -> DataFrame:
    """Estimate the duration of a project based on three-point estimation of breakdown
    tasks or milestones using a Monte Carlo simulation.
    The project duration is measured in the same unit used to estimate the duration of
    the tasks or milestones. It can be a unit of time (e.g. days, weeks) or story
    points.
    Eeach simulation is the sum of the duration of each tasks picked at random from a
    modified-PERT distribution computed using the best-case, expected and worst-case
    estimates provided.
    In order to make test reproducible, an optional parameter `random_state` has been
    introduced.
    """
    simulate_project = generate_project_simulator(
        task=task,
        best=best,
        expected=expected,
        worst=worst,
        random_seed=random_seed,
    )
    duration = [simulate_project() for _ in range(simulations)]
    return compute_stats(duration)
