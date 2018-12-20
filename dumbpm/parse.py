from typing import List


def any_negative(items: List[float]) -> bool:
    """Check if there is any negative item."""
    return any(i < 0 for i in items)


def parse_input(csv: List[float]) -> List[float]:
    """Parse input."""
    if any_negative(csv):
        raise ValueError("Negative values are not allowed")
    return csv
