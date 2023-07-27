from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

# See: https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-types-defined-in-stubs-but-not-at-runtime
if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison


def prod_first_k(x: list[SupportsRichComparison], k: int) -> SupportsRichComparison:
    """
    Memory-efficiently multiply first `k` elements of `x` list.

    Alternative to: math.prod(x[:k]) to avoid creating a sub-list.
    """
    ret: SupportsRichComparison = 1

    for i in range(min(k, len(x))):
        ret *= x[i]

    return ret


# -----------------------------------------------------------------------------


def get_max_product_1(x: Iterable[SupportsRichComparison], k: int) -> list[SupportsRichComparison]:
    """
    Complexity:
    * Time: O(n * log(n))
    * Space: O(n)
    """
    x_sorted = sorted(x, reverse=True)
    return prod_first_k(x_sorted, k)


def get_max_product_2_mut(x: list[SupportsRichComparison], k: int) -> list[SupportsRichComparison]:
    """
    Alternative: (IT MUTATES input x) sorting is done in place.

    Complexity:
    * Time: O(n * log(n))
    * Space: O(1)
    """
    x.sort(reverse=True)
    return prod_first_k(x, k)




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
    (([-2, -4, 5, 3], 3), 40) # fails here
]


def test():
    run_test_cases(
        TEST_CASES,
        get_max_product_1,
        get_max_product_2_mut
    )
