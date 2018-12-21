from functools import lru_cache
from functools import reduce
from typing import FrozenSet
from typing import Iterable
from typing import List
from typing import Tuple


def actual_value(cost: float, value: float, duration: float, rigging: float) -> float:
    """Compute actual value for a project, paying attention to zeros."""
    cost = cost or 1
    duration = duration or 1
    return value / (cost * duration) + rigging


def normalize(items: List[float]) -> List[float]:
    """Normalizes all items between 0 and 1."""
    n = max(items)
    return [i / n for i in items]


def prioritize(
    projects: List[str],
    cost: List[float],
    value: List[float],
    duration: List[float],
    rigging: List[float],
    max_cost: float,
) -> List[List[str]]:
    """Prioritize projects based on cost, value, duration and rigging, also
    making sure that the cost doesn't go over the maximum cost.
    """
    params = zip(
        normalize(cost), normalize(value), normalize(duration), normalize(rigging)
    )
    params_value = [actual_value(*p) for p in params]
    solutions = prio(
        tuple(zip(params_value, cost)), max_cost, 0, 0, (0,) * len(projects), 0
    )

    def sort(r: Iterable[Tuple[str, float]]) -> Iterable[Tuple[str, float]]:
        return sorted(r, key=lambda k: k[1], reverse=True)

    sorted_solutions = (
        sort((projects[i], params_value[i]) for i, p in enumerate(s) if p)
        for s in solutions[0]
    )
    return [[i[0] for i in s] for s in sorted_solutions]


Solution = Tuple[int, ...]
Solutions = Tuple[FrozenSet[Solution], float]
Projects = Tuple[Tuple[float, float], ...]


def prio(
    projects: Projects,
    max_cost: float,
    tot_value: float,
    tot_cost: float,
    state: Solution,
    step: int,
) -> Solutions:
    """Actual function for prioritization."""
    curr = frozenset(
        {(frozenset({state}), sum(projects[i][0] for i, y in enumerate(state) if y))}
    )
    projects_left = projects[step:]
    calls = frozenset(
        {
            prio(
                projects,
                max_cost,
                tot_value + value,
                tot_cost + cost,
                state[:i] + (1,) + state[i + 1 :],
                step + 1,
            )
            for i, (value, cost) in enumerate(projects_left)
            if (tot_cost + cost) <= max_cost
        }
    )
    solutions: FrozenSet[Solutions] = calls | curr

    @lru_cache()
    def compute_best(solutions):
        max_value = max(s[1] for s in solutions)
        best_sets = (s[0] for s in solutions if s[1] == max_value)
        return (reduce(lambda x, y: x | y, best_sets, frozenset()), max_value)

    return compute_best(solutions)
