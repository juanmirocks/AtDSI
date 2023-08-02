from typing import TypeAlias
import numpy as np
import numpy.typing as npt
from numbers import Real


Coordinates: TypeAlias = npt.NDArray


def find_closest_points_1(reference: Coordinates, k: int, *others: Coordinates, **extra: str) -> list[Coordinates]:
    print(reference)
    print(k),
    print(others),
    print(extra)
    ...


# -----------------------------------------------------------------------------

from atdsi.tutil import run_test_cases


def a(*points: Real) -> Coordinates:
    """Sugar syntax for `np.array(...)`"""
    return np.array(list(points))


TEST_CASES = [
    # Base edge cases
    ((a(0, 0), 0), []),
    ((a(0, 0), 0, a(1, 1)), []),
    ((a(0, 0), 1, a(1, 1)), [a(1, 1)]),
    ((a(0, 0), 1, a(1, 1), a(2, 2)), [a(1, 1)]),
    # Problem example
    ((a(0, 0), 3, a(2, -1), a(3, 2), a(4, 1), a(-1, -1), a(-2, 2)), [a(-1, -1), a(2, -1), a(-2, 2)]),
]


def test():
    run_test_cases(TEST_CASES, find_closest_points_1)
