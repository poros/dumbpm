import math
from typing import List
from typing import Optional

from numpy.random import default_rng
from pandas import DataFrame


def compute_sprints(
    scope: int,
    velocity: List[float],
    change: List[float],
    max_sprints: int,
) -> int:
    """Given the simulated velocity and scope change per sprint, compute how many
    sprints are necessary to finish the project.
    To protect the simulation from infinite projects (where scope change is higher than
    velocity), a maximum number of sprints is provided.
    """
    delta = 0.0
    for n in range(max_sprints):
        delta += velocity[n] - change[n]
        if scope <= delta:
            return n + 1
    return max_sprints


def compute_stats(duration: List[int]) -> DataFrame:
    return DataFrame(duration, columns=["Duration"]).describe(
        percentiles=[0.5, 0.75, 0.90, 0.99]
    )


def compute_max_sprints(scope: int, velocity: List[float], change: List[float]) -> int:
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


def estimate(
    scope: int,
    velocity: List[float],
    change: List[float],
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
    rng = default_rng(random_seed)
    max_sprints = compute_max_sprints(scope=scope, velocity=velocity, change=change)
    duration = []
    for i in range(simulations):
        rn_velocity = rng.choice(velocity, max_sprints)
        rn_change = rng.choice(change, max_sprints)
        # print(rn_velocity)
        # print(rn_change)
        duration.append(
            compute_sprints(
                scope=scope,
                velocity=rn_velocity,
                change=rn_change,
                max_sprints=max_sprints,
            )
        )
    print(duration)
    return compute_stats(duration)
