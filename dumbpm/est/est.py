import math
from typing import Callable
from typing import Optional

from numpy.random import default_rng
from pandas import DataFrame
from scipy.stats import norm

from dumbpm.shared import compute_stats


def compute_duration(
    scope: int,
    velocity: list[float],
    change: list[float],
) -> int:
    """Given the simulated velocity and scope change per sprint, compute how many
    sprints are necessary to finish the project.
    """
    max_sprints = len(velocity)
    delta = 0.0
    for n in range(max_sprints):
        delta += velocity[n] - change[n]
        if scope <= delta:
            return n + 1
    return max_sprints


def compute_max_sprints(scope: int, velocity: list[float], change: list[float]) -> int:
    """Compute a max number of sprints for the simulation. This is useful for two
    reasons:
    1. To avoid an infinite simulation in case scope changes are bigger than sprint
    velocities
    2. To pre-compute all random input values for the iteration in one go to improve
    performance
    """
    max_change = max(change)
    min_velocity = min(velocity)
    if max_change >= min_velocity:
        print(
            """WARNING: Max scope change >= minimum velocity.
            Sprints will be capped at 2000 per simulation."""
        )
        return 2000
    return math.ceil(scope / (min_velocity - max_change))


def generate_sprints_simulator(
    velocity: list[float],
    change: list[float],
    max_sprints: int,
    normal: bool,
    random_seed: Optional[int],
) -> Callable[[], tuple[list[float], list[float]]]:
    """Simulate the velocity and the scope change for the sprints in the simulation."""
    rng = default_rng(random_seed)
    if normal:
        velocity_mean, velocity_stdev = norm.fit(velocity)
        velocity_norm = norm(loc=velocity_mean, scale=velocity_stdev)
        change_mean, change_stdev = norm.fit(change)
        change_norm = norm(loc=change_mean, scale=change_stdev)

        def generate_sprints() -> tuple[list[float], list[float]]:
            rn_velocity = velocity_norm.rvs(size=max_sprints, random_state=rng).round(0)
            rn_change = change_norm.rvs(size=max_sprints, random_state=rng).round(0)
            return rn_velocity, rn_change

    else:

        def generate_sprints() -> tuple[list[float], list[float]]:
            rn_velocity = rng.choice(velocity, max_sprints).tolist()
            rn_change = rng.choice(change, max_sprints).tolist()
            return rn_velocity, rn_change

    return generate_sprints


def estimate(
    scope: int,
    velocity: list[float],
    change: list[float],
    normal: bool,
    simulations: int,
    random_seed: Optional[int] = None,
) -> DataFrame:
    """Estimate the duration of a project based on past sprints velocity and scope
    changes using a Monte Carlo simulation.
    The duration estimate is measured in number of sprints.
    Every simulations is composed by several iterations, each of which represents a
    sprint.
    By default, velocity and scope change for each iteration are picked at random
    following a uniform probability distribution from the provided historical data.
    If `normal` is True, the input will be modelled as normal distribution from which
    velocity and scope changes will be derived.
    In order to make test reproducible, an optional parameter `random_state` has been
    introduced.
    """
    duration = []
    max_sprints = compute_max_sprints(scope=scope, velocity=velocity, change=change)
    simulate_sprints = generate_sprints_simulator(
        velocity=velocity,
        change=change,
        max_sprints=max_sprints,
        normal=normal,
        random_seed=random_seed,
    )
    for i in range(simulations):
        rn_velocity, rn_change = simulate_sprints()
        duration.append(
            compute_duration(
                scope=scope,
                velocity=rn_velocity,
                change=rn_change,
            )
        )
    return compute_stats(duration)
