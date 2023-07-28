from __future__ import annotations
import heapq

from typing import TYPE_CHECKING, Iterable, NewType, Sequence
import math
from itertools import islice

# See: https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-types-defined-in-stubs-but-not-at-runtime
if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison


# -----------------------------------------------------------------------------


# The best solution is: `get_max_product_4`


# -----------------------------------------------------------------------------

# Utility functions & constants


NonNegativeInt = NewType("NonNegativeInt", int)
""">=0 number -- Type property not enforced. We just use it for documentation purposes"""


# See: https://docs.python.org/3.10/library/math.html?highlight=math%20prod#math.prod
_PROD_START: SupportsRichComparison = 1


def prod_first_k(x: Iterable[SupportsRichComparison], k: NonNegativeInt) -> SupportsRichComparison:
    """
    Memory-efficiently multiply first `k` elements of `x` iterable.

    Alternative to: math.prod(x[:k]) to avoid creating a sub-seq.

    Note: (arbitrarily & for simplicity) just like math.prod by default, this function returns 1 if x is empty or k is 0
    """
    ret: SupportsRichComparison = _PROD_START

    so_far = 0

    for num in x:
        if so_far == k:
            return ret
        else:
            ret *= num
            so_far += 1

    return ret


def is_last_non_negative(x: Sequence[SupportsRichComparison]) -> bool:
    """
    ASSUMPTION: the sequence is not empty.
    """
    return x[-1] >= 0


# Would be useful for generic solution with negative numbers and any k
def how_many_last_k_nums_are_negative(x: Sequence[SupportsRichComparison], k: NonNegativeInt) -> int:
    ret = 0
    for i in range(len(x) - 1, max(-1, len(x) - 1 - k), -1):
        if x[i] < 0:
            ret += 1
        else:
            return ret
    return ret


def get_even_number_same_or_one_less(k: NonNegativeInt) -> int:
    """
    Return k if k is even, else k-1
    """
    if k % 2 == 0:
        return k
    else:
        return k - 1


# -----------------------------------------------------------------------------


# Specific-helper functions


def _try_max_multiplying_head_with_last_2_negative_numbers(
    x: list[SupportsRichComparison], k: NonNegativeInt
) -> SupportsRichComparison:
    if k != 3:
        raise NotImplementedError(
            "k must be 3 to allow for negative numbers (as per exact book's question/problem definition). A generic solution is not implemented yet"
        )
    else:
        return max(prod_first_k(x, k), x[0] * math.prod(x[len(x) - 2 :]))


# Copied from: https://docs.python.org/3/library/itertools.html#itertools-recipes
#
# Replace by itertools.batched when Python 3.12 is released: https://docs.python.org/3.12/library/itertools.html#itertools.batched
def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def _get_max_product_4__find_max_mult(
    largest_head: Sequence[SupportsRichComparison],
    smallest_tail_with_maybe_negatives: Sequence[SupportsRichComparison],
    k: NonNegativeInt,
) -> SupportsRichComparison:
    ret = prod_first_k(largest_head, k)

    if is_last_non_negative(smallest_tail_with_maybe_negatives):
        # Optimization to quickly check if there are no negative numbers
        return ret

    else:
        tail_prod: SupportsRichComparison = _PROD_START
        tail_taken: int = 0

        for negatives_pair in batched(reversed(smallest_tail_with_maybe_negatives), 2):
            if len(negatives_pair) < 2 or not all(e < 0 for e in negatives_pair):
                break
            else:
                tail_taken += 2
                tail_prod *= math.prod(negatives_pair)

                total = tail_prod * prod_first_k(largest_head, k - tail_taken)

                if total > ret:
                    ret = total
                elif ret > 0:
                    break

        return ret


# -----------------------------------------------------------------------------


def get_max_product_1(x: Iterable[SupportsRichComparison], k: NonNegativeInt) -> SupportsRichComparison:
    """
    Complexity:
    * Time: O(n * log(n))
    * Space: O(n)
    """
    x_sorted = sorted(x, reverse=True)

    if (
        k == 0 or len(x_sorted) == 0
    ):  # check the length of x_sorted as input Iterable might not have an efficient `len` implementation
        return _PROD_START
    elif k == 1 or is_last_non_negative(x_sorted):
        return prod_first_k(x_sorted, k)
    else:
        return _try_max_multiplying_head_with_last_2_negative_numbers(x_sorted, k)


def get_max_product_2_mut(x: list[SupportsRichComparison], k: NonNegativeInt) -> SupportsRichComparison:
    """
    Alternative: (IT MUTATES input x) sorting is done in place.

    Complexity:
    * Time: O(n * log(n))
    * Space: O(1)
    """
    if k == 0 or len(x) == 0:
        return _PROD_START

    x.sort(reverse=True)
    if k == 1 or is_last_non_negative(x):
        return prod_first_k(x, k)
    else:
        return _try_max_multiplying_head_with_last_2_negative_numbers(x, k)


def get_max_product_3(x: Sequence[SupportsRichComparison], k: NonNegativeInt) -> SupportsRichComparison:
    """
    Alternative: when k is known and small (3, as per question/problem exact definition) we can use a min/max-heap to more efficiently get the max & min elements.
    See: https://docs.python.org/3.10/library/heapq.html?highlight=heapq#heapq.nsmallest

    Complexity:
    * NOTE: following simplifications apply when treating k as a constant (=3).

    * Time: O(n * log(k)) -> O(n) -- see: https://stackoverflow.com/a/23038826/341320
    * Space: O(k) -> O(1)
    """
    if k == 3:
        largest_3 = heapq.nlargest(3, x)
        smallest_2 = heapq.nsmallest(2, x)
        return max(math.prod(largest_3), largest_3[0] * math.prod(smallest_2))
    else:
        return get_max_product_1(x, k)


def get_max_product_4(x: Iterable[SupportsRichComparison], k: NonNegativeInt) -> SupportsRichComparison:
    """
    Generic implementation, works with negative numbers and for any k

    Complexity:
    * Worst case if (k*2 > n):
        * Time: O(n * log(n))
        * Space: O(n)
    * Else (normal case, k << n):
        * Time: O(n * log(k))
        * Space: O(k)
    """
    match k:
        case 0:
            return _PROD_START
        case 1:
            try:
                return max(x)
            except ValueError:  # max() arg is an empty sequence
                return _PROD_START
        case _:
            x_seq = (
                x if isinstance(x, Sequence) else list(x)
            )  # make sure we have an indexable sequence to work on it efficiently -- Space O(1) if input is already a sequence, else O(n)

            # Arbitrary decision boundary to decide using `sorted` or heapq sorting
            is_k_big = k * 2 > len(x_seq)

            if is_k_big:
                x_sorted = sorted(x, reverse=True)  # Space O(n)
                largest_head = x_sorted
                # Space O(k) -- It could be optimized to use `x_sorted` dropping unneeded elements in place
                smallest_tail = x_sorted[-k:]  # Space O(k)

            else:
                # Space O(k) -- worst case: Space(n/2)
                largest_head = heapq.nlargest(k, x_seq)
                # Space O(k) -- worst case: Space(n/2)
                smallest_tail = heapq.nsmallest(get_even_number_same_or_one_less(k), x_seq)

            return _get_max_product_4__find_max_mult(largest_head, smallest_tail, k)


# -----------------------------------------------------------------------------

from atdsi.tutil import run_test_cases

TEST_CASES_NON_GENERIC = [
    (([], 0), _PROD_START),
    (([3], 0), _PROD_START),
    (([0], 0), _PROD_START),
    (([0], 1), 0),
    (([3], 1), 3),
    (([3, 2], 2), 6),
    (([3, 2, 5], 2), 15),
    (([1, 3, 4, 5], 3), 60),
    # Negative numbers with fixed k==3
    (([-2, -4, 5, 3], 3), 40),  # as per question/problem definition
    (([-2, -4, -5, 3], 3), 60),
    (([-1, 2, 2, 2], 3), 8),
    (([-1, -8, 2, 2, 2], 3), 16),
    (([-1, -8, -2, 2, 2], 3), 32),
]


def test_negative_numbers_only_for_fixed_k_3():
    run_test_cases(TEST_CASES_NON_GENERIC, get_max_product_1, get_max_product_2_mut, get_max_product_3)


TEST_CASES_NEGATIVE_GENERIC = [
    # Negative numbers, generic (when k != 3, not requested in question/problem)
    (([-1, -8, -2, -2, 2], 4), 32),  # -8 * -2 * -2 * -1,
    (([2, 2, -1, -1, -10, -10], 4), 400),  # -10 * -10 * 2 * 2
]


def test_generic():
    run_test_cases(TEST_CASES_NEGATIVE_GENERIC, get_max_product_4)
    run_test_cases(TEST_CASES_NON_GENERIC, get_max_product_4)
