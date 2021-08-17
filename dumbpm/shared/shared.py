from pandas import DataFrame


def compute_stats(duration: list[int]) -> DataFrame:
    """Statistics to visualize for the result of a Monte Carlo simulation."""
    return DataFrame(duration, columns=["Duration"]).describe(
        percentiles=[0.5, 0.75, 0.90, 0.99]
    )
