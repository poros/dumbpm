from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple


def combined_value(value: float, cost: float, duration: float, risk: float) -> float:
    """Compute the combined value for a project, paying attention to zeros."""
    cost = cost or 1
    duration = duration or 1
    risk = risk or 1
    return value / (cost * duration * risk)


def normalize(items: List[float]) -> List[float]:
    """Normalizes all items between 0 and 1."""
    n = max(items)
    return [i / n for i in items] if n > 0 else [0] * len(items)


def compute_actual_value(
    value: List[float],
    cost: List[float],
    duration: List[float],
    risk: List[float],
    rigging: List[float],
) -> List[float]:
    """
    Compute the actual value (used for prioriitization) of each item by
    norm(norm(value) / (norm(cost) * norm(duration) * norm(risk))) + norm(rigging)
    """
    params = zip(
        normalize(value), normalize(cost), normalize(duration), normalize(risk),
    )
    params_value = normalize([combined_value(*p) for p in params])
    return [sum(x) for x in zip(params_value, normalize(rigging))]


class Item(NamedTuple):
    name: str
    value: float
    weight: float


Items = Tuple[Item, ...]


def prioritize(
    projects: List[str],
    value: List[float],
    cost: List[float],
    duration: List[float],
    risk: List[float],
    rigging: List[float],
    alternatives: List[Tuple[str, ...]],
    max_cost: float,
    duration_cost_budget: bool,
) -> List[str]:
    """Prioritize projects based on cost, value, duration and rigging, also making sure
    that the cost doesn't go over the maximum cost.
    Projects listed as alternative of each other won't be selected together.
    For the formula used to compute the actual value of each item see
    compute_actual_value.
    The cost of an item can simply be cost or
    (cost * duration) if duration_cost_budget is True.
    """
    actual_value = compute_actual_value(value, cost, duration, risk, rigging)
    selected_cost = (
        [c * d for c, d in zip(cost, duration)] if duration_cost_budget else cost
    )
    alts = dict(zip(projects, alternatives))
    solution = prio(
        tuple(Item(*x) for x in zip(projects, actual_value, selected_cost)),
        max_cost,
        {},
        alts,
    )
    sorted_solution = sorted(solution, key=lambda k: k[1], reverse=True)
    return [s[0] for s in sorted_solution]


def tot_value(items: Items, max_weight: float) -> float:
    """Compute total value of a list of items, but return 0 if they weight more
    than max.
    """
    return (
        sum([i.value for i in items])
        if sum([i.weight for i in items]) <= max_weight
        else 0
    )


def prio(
    items: Items,
    max_weight: float,
    mem: Dict[Tuple[Items, float], Items],
    alts: Dict[str, Tuple[str, ...]],
) -> Items:
    """Actual function for prioritization."""
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
            if tot_value(included, max_weight) > tot_value(excluded, max_weight)
            else excluded
        )
        mem[(items, max_weight)] = solution
    return mem[(items, max_weight)]
