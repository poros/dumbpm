from collections import Counter
from itertools import chain

from pandas import DataFrame
from pandas import read_csv

flatten = chain.from_iterable


def parse_input(filename: str) -> DataFrame:
    """Parse csv input file using pandas."""
    csv = read_csv(filename)
    csv.rename(columns=lambda c: c.lower().rstrip("s"), inplace=True)
    if "milestone" in csv:
        csv.rename(columns={"milestone": "task"}, inplace=True)

    if "task" not in csv:
        raise ValueError("Task column must be specified")
    if csv["task"].isnull().values.any():
        raise ValueError("All tasks must have a name")
    counts: Counter[str] = Counter(csv["task"])
    dups = [(i, c) for i, c in counts.items() if c > 1]
    if dups:
        raise ValueError(f"Task names must be unique: {dups}")

    if "best" not in csv:
        raise ValueError("Best column must be specified")
    if csv["best"].isnull().values.any():
        raise ValueError("All tasks must have a best-case estimate")

    if "worst" not in csv:
        raise ValueError("Worst column must be specified")
    if csv["worst"].isnull().values.any():
        raise ValueError("All tasks must have a worst-case estimate")

    if "expected" not in csv:
        raise ValueError("Expected column must be specified")
    if csv["expected"].isnull().values.any():
        raise ValueError("All tasks must have an expected estimate")

    if any(filter(lambda x: isinstance(x, int) and x < 0, flatten(csv.values))):
        raise ValueError("Negative estimates are not allowed")

    for row in csv.itertuples():
        if not (row.best <= row.expected <= row.worst):
            raise ValueError(
                "Best-case, expected and worst-case estimates for a task must be "
                f"monotonically increasing: {row=}"
            )

    return csv
