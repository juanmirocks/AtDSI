from __future__ import annotations

from typing import Callable, Sequence, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from _typeshed import SupportsLenAndGetItem

import random
import string


Output = TypeVar("Output")


# To use within pytest `test*` functions
def run_test_cases(test_cases: Sequence[tuple[tuple, Output]], *funs: Callable[..., Output], **kwargs) -> None:
    equal = kwargs.get("equal", lambda x, y: x == y)

    for fun in funs:
        for input, expected_output in test_cases:
            input_str = (
                str(*input) if len(input) == 1 else str(input)
            )  # Get the input's string representation first in case the input is mutated inside the function
            output = fun(*input)
            assert equal(
                expected_output, output
            ), f"\n\nin:\n{input_str}]\n\n->\n\nexpected_out:\n{expected_output}\n\n vs. \n\nout:\n{output}"


def gen_random_seq(population: SupportsLenAndGetItem = string.ascii_lowercase, min: int = 1, max: int = 1):
    k = min if min == max else random.randint(min, max)  # nosec B311
    return random.choices(population, k=k)  # nosec B311
