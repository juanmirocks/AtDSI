from typing import Any, Sequence


def get_intersection_1(a: Sequence[Any], b: Sequence[Any]) -> list[Any]:
    """
    Complexity:
    * Time: O(a_len + b_len)
    * Space: O(min(a_len, b_len))
    """
    if len(b) < len(a):
        # Swap to always create an additional set only over the smallest input sequence
        a, b = b, a
    return list(set(a).intersection(b))


# -----------------------------------------------------------------------------

from atdsi.__util__ import run_test_cases


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
        get_intersection_1
    )
