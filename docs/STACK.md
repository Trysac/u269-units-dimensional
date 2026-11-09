# Stack

## Used

| Tool | Why |
|---|---|
| Python >= 3.10 | The code uses `list[str] | None`, `dict[str, int]`, and `from __future__ import annotations`. |
| Python standard library | The package uses `dataclasses`, `fractions`, `re`, `typing`, and `argparse`; it has no runtime dependencies. |
| pytest | `tests/test_units_dimensional.py` imports `pytest` and uses `pytest.raises` and `pytest.approx`. |

## Discarded

No third-party runtime dependencies are used or listed in the specification. No other tools are recorded by the code shown.
