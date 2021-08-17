from collections import Counter
from itertools import chain

from pandas import DataFrame
from pandas import read_csv

flatten = chain.from_iterable


def parse_input(filename: str) -> DataFrame:
    """Parse csv input file using pandas."""
    csv = read_csv(filename)
    csv.rename(columns=lambda c: c.lower().rstrip("s"), inplace=True)

    if "project" not in csv:
        raise ValueError("Projects column must be specified")
    if csv["project"].isnull().values.any():
        raise ValueError("All projects must have a name")
    counts: Counter[str] = Counter(csv["project"])
    dups = [(i, c) for i, c in counts.items() if c > 1]
    if dups:
        raise ValueError(f"Projects names must be unique: {dups}")

    if "value" not in csv:
        raise ValueError("Value column must be specified")
    if csv["value"].isnull().values.any():
        raise ValueError("All projects must have a value")

    csv.rename(columns={"pq": "cost"}, inplace=True)
    if "cost" not in csv:
        raise ValueError("Cost column must be specified")
    if csv["cost"].isnull().values.any():
        raise ValueError("All projects must have a cost")

    if "duration" not in csv:
        csv["duration"] = [0] * len(csv["project"])
    if csv["duration"].isnull().values.any():
        raise ValueError(
            "All projects must have a duration, if the Duration column is specified"
        )

    if "risk" not in csv:
        csv["risk"] = [0] * len(csv["project"])
    if csv["risk"].isnull().values.any():
        raise ValueError(
            "All projects must have a risk, if the Risk column is specified"
        )

    csv.rename(columns={"rig": "rigging"}, inplace=True)
    if "rigging" not in csv:
        csv["rigging"] = [0] * len(csv["project"])
    else:
        csv["rigging"].fillna(0, inplace=True)

    csv.rename(columns={"alt": "alternative"}, inplace=True)
    if "alternative" not in csv:
        csv["alternative"] = [""] * len(csv["project"])
    else:
        csv["alternative"].fillna("", inplace=True)
    csv["alternative"] = [tuple(a.split(", ")) if a else () for a in csv["alternative"]]
    missing = [
        a
        for alts in csv["alternative"]
        if alts
        for a in alts
        if a not in csv["project"].values
    ]
    if missing:
        raise ValueError(f"Alternatives and projects don't match: {missing}")
    alts_map = dict(zip(csv["project"], csv["alternative"]))
    asym = next(
        ((p, a) for p, alts in alts_map.items() for a in alts if p not in alts_map[a]),
        None,
    )
    if asym:
        raise ValueError(
            f"{asym[0]} lists {asym[1]} as alternative, but not the other way around"
        )

    if any(filter(lambda x: isinstance(x, float) and x < 0, flatten(csv.values))):
        raise ValueError("Negative values are not allowed")

    return csv
