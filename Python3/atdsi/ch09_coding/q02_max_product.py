from __future__ import annotations
import heapq

from typing import TYPE_CHECKING, Iterable
import math
from atdsi import require

# See: https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-types-defined-in-stubs-but-not-at-runtime
if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison


# -----------------------------------------------------------------------------

# Helper functions & constants


# See: https://docs.python.org/3.10/library/math.html?highlight=math%20prod#math.prod
_PROD_START: SupportsRichComparison = 1


def prod_first_k(x: list[SupportsRichComparison], k: int) -> SupportsRichComparison:
    """
    Memory-efficiently multiply first `k` elements of `x` list.

    Alternative to: math.prod(x[:k]) to avoid creating a sub-list.

    Note: (arbitrarily & for simplicity) just like math.prod by default, this function returns 1 if x is empty or k is 0
    """
    ret: SupportsRichComparison = _PROD_START

    for i in range(min(k, len(x))):
        ret *= x[i]

    return ret


# Would be useful for generic solution with negative numbers and any k
def how_many_last_k_nums_are_negative(x: list[SupportsRichComparison], k: int) -> int:
    ret = 0
    for i in range(len(x) - 1, max(-1, len(x) - 1 - k), -1):
        if x[i] < 0:
            ret += 1
        else:
            return ret
    return ret


def try_max_multiplying_head_with_last_2_negative_numbers(
    x: list[SupportsRichComparison], k: int
) -> SupportsRichComparison:
    if k != 3:
        raise NotImplementedError(
            "k must be 3 to allow for negative numbers (as per exact book's question/problem definition). A generic solution is not implemented yet"
        )
    else:
        return max(prod_first_k(x, k), x[0] * math.prod(x[len(x) - 2 :]))


# -----------------------------------------------------------------------------


def get_max_product_1(x: Iterable[SupportsRichComparison], k: int) -> list[SupportsRichComparison]:
    """
    Complexity:
    * Time: O(n * log(n))
    * Space: O(n)
    """
    x_sorted = sorted(x, reverse=True)

    if (
        len(x_sorted) == 0 or k == 0
    ):  # check the length of x_sorted as input Iterable might not have an efficient `len` implementation
        return _PROD_START
    elif x_sorted[-1] >= 0 or k == 1:
        return prod_first_k(x_sorted, k)
    else:
        return try_max_multiplying_head_with_last_2_negative_numbers(x_sorted, k)


def get_max_product_2_mut(x: list[SupportsRichComparison], k: int) -> list[SupportsRichComparison]:
    """
    Alternative: (IT MUTATES input x) sorting is done in place.

    Complexity:
    * Time: O(n * log(n))
    * Space: O(1)
    """
    if len(x) == 0 or k == 0:
        return _PROD_START

    x.sort(reverse=True)
    if x[-1] >= 0 or k == 1:
        return prod_first_k(x, k)
    else:
        return try_max_multiplying_head_with_last_2_negative_numbers(x, k)


def get_max_product_3(x: list[SupportsRichComparison], k: int) -> list[SupportsRichComparison]:
    """
    Alternative: when k is known and small (3, as per question/problem exact definition) we can use a min/max-heap to more efficiently get the max & min elements.
    See: https://docs.python.org/3.10/library/heapq.html?highlight=heapq#heapq.nsmallest

    Complexity:
    * NOTE: we treat k (=3) as a constant

    * Time: O(n * log(k)) -> O(n) -- see: https://stackoverflow.com/a/23038826/341320
    * Space: O(k)  -> O(1)
    """
    if k == 3:
        largest_3 = heapq.nlargest(3, x)
        smallest_2 = heapq.nsmallest(2, x)
        return max(math.prod(largest_3), largest_3[0] * math.prod(smallest_2))
    else:
        return get_max_product_1(x, k)


# -----------------------------------------------------------------------------

from atdsi.tutil import run_test_cases

TEST_CASES = [
    (([], 0), 1),
    (([3], 0), 1),
    (([0], 0), 1),
    (([0], 1), 0),
    (([3], 1), 3),
    (([3, 2], 2), 6),
    (([3, 2, 5], 2), 15),
    (([1, 3, 4, 5], 3), 60),
    # Negative numbers
    (([-2, -4, 5, 3], 3), 40),  # as per question/problem definition
    (([-2, -4, -5, 3], 3), 60),
    (([-1, 2, 2, 2], 3), 8),
    (([-1, -8, 2, 2, 2], 3), 16),
    (([-1, -8, -2, 2, 2], 3), 32),
    # Negative numbers, when k != 3 (not requested in question/problem), not implemented
    # (([-1, -8, -2, -2, 2], 4), 32)
]


def test():
    run_test_cases(TEST_CASES, get_max_product_1, get_max_product_2_mut, get_max_product_3)


def test_how_many_last_nums_are_negative():
    TEST_CASES = [
        (([], 0), 0),
        (([], 1), 0),
        (([3], 0), 0),
        (([0], 0), 0),
        (([0], 1), 0),
        (([-1], 1), 1),
        (([-1], 2), 1),
        (([8, -9], 2), 1),
        (([-8, -9], 2), 2),
        (([-8, -9], 1), 1),
        (([3, -8, -9], 3), 2),
    ]

    run_test_cases(TEST_CASES, how_many_last_k_nums_are_negative)
