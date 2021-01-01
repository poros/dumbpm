from pandas import DataFrame
from pandas import read_csv


def parse_input(filename: str) -> DataFrame:
    """Parse csv input file using pandas."""
    csv = read_csv(filename)
    csv.rename(columns=lambda c: c.lower(), inplace=True)

    if "velocity" not in csv:
        raise ValueError("Velocity column must be specified")
    if csv["velocity"].isnull().values.any():
        raise ValueError("All past sprints must specify a velocity value")
    if any(v < 0 for v in csv["velocity"].values):
        raise ValueError("Negative velocity is not allowed")

    if "change" not in csv:
        csv["change"] = [0] * len(csv["velocity"])
    csv["change"].fillna(0, inplace=True)

    return csv
