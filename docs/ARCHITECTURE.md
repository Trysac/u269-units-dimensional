# Architecture

`units_dimensional` is a stdlib-only package for exact unit conversion. Its modules are:

- `_errors.py` defines `UnitsError` with a `code` literal of `unknown_unit`, `dimension_mismatch`, `parse_error`, or `input_too_large`.
- `_data.py` holds the immutable dimension order/names, the fixed unit table, the prefix table, the set of prefixable base names, and `format_dimension`.
- `_parser.py` parses numeric literals into `Fraction` values and unit expressions into `(dimension, scale)` pairs. It uses `re` for numbers and an iterative loop for units.
- `_convert.py` checks dimension equality, multiplies by the source scale, divides by the target scale, and returns a `float`; overflow raises `UnitsError('parse_error')`.
- `__init__.py` exposes `Quantity`, `UnitsError`, `convert`, `dimension_of`, `parse_quantity`, and `__version__`.
- `__main__.py` provides `main(argv)` and the `python -m units_dimensional` entry point.
- `py.typed` marks the package as typed.

All conversion factors are `fractions.Fraction`, so arithmetic is exact until the final `float()` call. The grammar has no parentheses and `parse_unit` is iterative, so parser depth is fixed. `parse_quantity` limits its text argument to 200 characters; unit exponents are limited to `-12..12`; numeric literal exponents are limited to `-100..100`. Affine temperatures are not supported; `K` is a temperature difference.
