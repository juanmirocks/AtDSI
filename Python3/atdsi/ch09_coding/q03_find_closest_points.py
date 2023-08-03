import heapq
from typing import Any, Callable, TypeAlias

import numpy as np
import numpy.typing as npt

from atdsi.types import NonNegativeInt

Coordinates: TypeAlias = npt.NDArray


def find_closest_points_1(
    reference: Coordinates, k: NonNegativeInt, *others: Coordinates, **extra: Any
) -> list[Coordinates]:
    """
    Use `sorted` and then take only the first k elements.


    Complexity:
    # m == len(others) and (assumed) k << m

    * Time: O(m * log(m))
    * Space: O(m)


    See `sorted` ("Timsort") details:
    * https://en.wikipedia.org/wiki/Timsort
    """
    dist_fun: Callable[[Coordinates, Coordinates], np.number] = extra.get("dist_fun", calc_dist_Euclidean)
    sort_key: Callable[[Coordinates], np.number] = lambda other: dist_fun(reference, other)

    return sorted(others, key=sort_key)[0:k]  # Time: O(m * log(m)) - Space: O(m)


def find_closest_points_2(
    reference: Coordinates, k: NonNegativeInt, *others: Coordinates, **extra: Any
) -> list[Coordinates]:
    """
    Alternative: use min-heap to only store & sort on k elements.


    Complexity:
    # m == len(others) and (assumed) k << m

    * Time: O(m * log(k))
    * Space: O(k)


    See heapq Python implementation details & complexity:
    * https://github.com/python/cpython/blob/3.11/Lib/heapq.py#L397
    * https://stackoverflow.com/a/23038826/341320
    """
    dist_fun: Callable[[Coordinates, Coordinates], np.number] = extra.get("dist_fun", calc_dist_Euclidean)
    sort_key: Callable[[Coordinates], np.number] = lambda other: dist_fun(reference, other)

    return heapq.nsmallest(k, others, key=sort_key)  # Time: O(m * log(k)) - Space: O(k)


# -----------------------------------------------------------------------------


def calc_dist_Euclidean(a: Coordinates, b: Coordinates) -> np.number:
    # See: https://stackoverflow.com/a/1401828/341320
    return np.linalg.norm(a - b)
    # Alternatively:
    # require(a.shape == b.shape and len(a.shape) == 1)
    # return math.sqrt(sum((a[i] - b[i])**2 for i in range(0, a.shape[0])))


# -----------------------------------------------------------------------------

from atdsi.tutil import run_test_cases


def a(*points: int | float) -> Coordinates:
    """Sugar syntax for `np.array(...)`"""
    return np.array(list(points))


def equal(x: list[Coordinates], y: list[Coordinates]) -> bool:
    return len(x) == len(y) and all(np.array_equal(x_i, y_i) for x_i, y_i in zip(x, y))


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
    run_test_cases(TEST_CASES, find_closest_points_1, find_closest_points_2, equal=equal)
