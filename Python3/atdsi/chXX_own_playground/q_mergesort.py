import operator
from typing import Any, Callable


def merge_sorted_lists_1(a: list[Any], b: list[Any], lt: Callable[[Any, Any], bool] = operator.lt) -> list[Any]:
    ret: list[Any] = []
    a_idx = 0
    b_idx = 0

    while a_idx < len(a) and b_idx < len(b):
        if lt(a[a_idx], b[b_idx]):
            ret.append(a[a_idx])
            a_idx += 1
        else:
            ret.append(b[b_idx])
            b_idx += 1

    while a_idx < len(a):
        ret.append(a[a_idx])
        a_idx += 1

    while b_idx < len(b):
        ret.append(b[b_idx])
        b_idx += 1

    return ret


def mergesort_1(x: list[Any], lt: Callable[[Any, Any], bool] = operator.lt) -> list[Any]:
    if len(x) < 2:
        return x

    mid = len(x) // 2

    a = mergesort_1(x[:mid], lt=lt)
    b = mergesort_1(x[mid:], lt=lt)
    return merge_sorted_lists_1(a, b, lt=lt)


# -----------------------------------------------------------------------------

from atdsi.tutil import gen_random_seq, run_test_cases

TEST_CASES_A = [
    (([], []), []),
    (([1], []), [1]),
    (([], [1]), [1]),
    (([1], [1]), [1, 1]),
    (([1, 2, 3, 4, 5], [0, 1, 3, 7]), [0, 1, 1, 2, 3, 3, 4, 5, 7]),
    (([5, 4, 3, 2, 1], [7, 3, 1, 0], operator.gt), [7, 5, 4, 3, 3, 2, 1, 1, 0]),
]


def test_merge_sorted_lists():
    run_test_cases(TEST_CASES_A, merge_sorted_lists_1)


# -----------------------------------------------------------------------------

TEST_CASES_B = [
    (([], ), []),
    (([1], ), [1]),
    (([1, 2, 3, 4, 5], ), [1, 2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], operator.gt), [5, 4, 3, 2, 1]),
    (lambda: ((s := gen_random_seq(min=1, max=100), ), sorted(s)))(),
]


def test_mergesort():
    run_test_cases(TEST_CASES_B, mergesort_1)
