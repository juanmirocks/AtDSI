Remarks:
* Each chapter's python file is a book's question with my answer(s).
* I often provide multiple answer implementation alternatives and discuss the tradeoffs.
* Tests for the answers are written in the same file (implemented with [pytest](https://docs.pytest.org/en/7.3.x/)).
* My python code has [type annotations](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).


## Verify/test the answers

First, you need to have python [poetry](https://python-poetry.org).

```shell
# Install deps
poetry install


# Enter into the shell environment
poetry shell


# Test (all questions & answers)
pytest
```