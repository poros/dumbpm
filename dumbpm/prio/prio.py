from typing import NamedTuple
from typing import Tuple  # keep until PEP-585 fully supported in mypy


def norm(items: list[float]) -> list[float]:
    """Normalize all items between (0 , 1) by min-max normalization,
    but set min=0 because 0s will degrade the prioritization algorithm.
    """
    n = max(items)
    return [i / n for i in items] if n > 0 else [0.0] * len(items)


def compute_score(
    value: list[float],
    cost: list[float],
    duration: list[float],
    risk: list[float],
    rigging: list[float],
) -> list[float]:
    """
    Compute the score (used for prioritization) of each item by
    norm(norm(value) / (norm(cost) + norm(duration) + norm(risk))) + norm(rigging)

    Normalization of parameters is necessary because the algorithm makes no
    assumption about the interval of each parameter. The additional normalization
    before summing up rigging and the rest of the equation is so that rigging can
    have a sizeable influence in the outcome even if normalized.
    """
    numerator = norm(value)
    denominator = [c + d + r for c, d, r in zip(norm(cost), norm(duration), norm(risk))]
    if 0 in denominator:
        raise ValueError(
            "At least one project has 0 as combination of cost, duration and risk"
        )
    fraction = norm([n / d for n, d in zip(numerator, denominator)])
    return [f + r for f, r in zip(fraction, norm(rigging))]


class Item(NamedTuple):
    name: str
    score: float
    weight: float


Items = Tuple[Item, ...]


def combine_cost_and_duration(
    cost: list[float], duration: list[float]
) -> tuple[list[float], list[float]]:
    """If cost is assumed to be per unit of duration, multuply them in a single cost
    parameter and erase duration from the equation, so not to account for it twice.
    """
    combined_cost = [c * d for c, d in zip(cost, duration)]
    # duration is part of a sum operation, so we can erase it by making it 0
    erased_duration = [0.0] * len(duration)
    return combined_cost, erased_duration


def prioritize(
    projects: list[str],
    value: list[float],
    cost: list[float],
    duration: list[float],
    risk: list[float],
    rigging: list[float],
    alternatives: list[tuple[str, ...]],
    max_cost: float,
    cost_per_duration: bool,
) -> list[str]:
    """Prioritize projects based on cost, value, duration and rigging, also making sure
    that the cost doesn't go over the maximum cost.
    Projects listed as alternative of each other won't be selected together.
    For the formula used to compute the prioritizaion score of each item see
    compute_score.
    If cost_per_duration is True, cost is assumed to be per unit of duration.
    """
    n_cost, n_duration = (
        combine_cost_and_duration(cost, duration)
        if cost_per_duration
        else (cost, duration)
    )
    score = compute_score(value, n_cost, n_duration, risk, rigging)
    weight = n_cost
    alts = dict(zip(projects, alternatives))
    solution = prio(
        tuple(Item(*x) for x in zip(projects, score, weight)),
        max_cost,
        {},
        alts,
    )
    sorted_solution = sorted(solution, key=lambda k: k[1], reverse=True)
    return [s[0] for s in sorted_solution]


def total_score(items: Items, max_weight: float) -> float:
    """Compute total score of a list of items, but return 0 if they weight more
    than max_weight.
    """
    return (
        sum(i.score for i in items) if sum(i.weight for i in items) <= max_weight else 0
    )


def prio(
    items: Items,
    max_weight: float,
    mem: dict[tuple[Items, float], Items],
    alts: dict[str, tuple[str, ...]],
) -> Items:
    """Actual function for prioritization.
    It is a Knapsack solver using dynamic programming with memorization.
    """
    if not items:
        return ()
    if (items, max_weight) not in mem:
        excluded = prio(items[1:], max_weight, mem, alts)
        alternatives = alts[items[0][0]]
        items_left = tuple(i for i in items[1:] if i[0] not in alternatives)
        included = (items[0],) + prio(
            items_left, max_weight - items[0].weight, mem, alts
        )
        solution = (
            included
            if total_score(included, max_weight) > total_score(excluded, max_weight)
            else excluded
        )
        mem[(items, max_weight)] = solution
    return mem[(items, max_weight)]
