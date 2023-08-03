from typing import Callable, Sequence, TypeVar


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
