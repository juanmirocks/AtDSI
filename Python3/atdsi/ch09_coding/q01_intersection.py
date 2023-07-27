from typing import Any, Sequence


def get_intersection_1(a: Sequence[Any], b: Sequence[Any]) -> list[Any]:
    """
    Complexity:
    * Time: O(a_len + b_len)
    * Space: O(min(a_len, b_len))
    """
    if len(b) < len(a):
        # Swap to create an additional set over the smallest input sequence only
        a, b = b, a
    return list(set(a).intersection(b))


def get_intersection_2(a: Sequence[Any], b: Sequence[Any]) -> list[Any]:
    """
    Alternative: we iterate over b elements explicitly.

    Complexity:
    * Time: O(a_len + b_len)
    * Space: O(min(a_len, b_len))
    """
    if len(b) < len(a):
        # Swap to create an additional set over the smallest input sequence only
        a, b = b, a
    a_set = set(a)
    return [b_elem for b_elem in b if b_elem in a_set]


# -----------------------------------------------------------------------------

from atdsi.tutil import run_test_cases


TEST_CASES = [
    (([], []), []),
    (([1], []), []),
    (([], [1]), []),
    (([1], [1]), [1]),
    (([1, 2, 3, 4, 5], [0, 1, 3, 7]), [1, 3])
]


def test():
    run_test_cases(
        TEST_CASES,
        get_intersection_1,
        get_intersection_2
    )
