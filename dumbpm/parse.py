from itertools import chain

from pandas import DataFrame
from pandas import read_csv


def parse_input(filename: str) -> DataFrame:
    """Parse csv input file using pandas."""
    csv = read_csv(filename)
    csv.fillna(0, inplace=True)
    csv.rename(columns=lambda c: c.lower().strip("s"), inplace=True)
    csv.rename(columns={"rig": "rigging"}, inplace=True)
    if any(
        filter(
            lambda x: isinstance(x, float) and x < 0, chain.from_iterable(csv.values)
        )
    ):
        raise ValueError("Negative values are not allowed")
    return csv
