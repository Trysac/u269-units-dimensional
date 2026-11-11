# trysac-units-dimensional

Exact dimensional analysis for unit conversion. The library parses quantities such as `9.81 m/s^2` and converts between compatible units with rational arithmetic; floating point appears only in the final result. It has no runtime dependencies and uses a fixed unit table with a compact, non-recursive grammar.

## Installation

```bash
pip install trysac-units-dimensional
```

## Usage

```python
from units_dimensional import convert

print(convert("1 km/h", "m/s"))  # 0.2777777777777778
print(convert("1 mi", "km"))  # 1.609344
print(convert("1 lb", "kg"))  # 0.45359237
```

The command line entry point takes a quantity and a target unit:

```bash
python -m units_dimensional '1 km/h' 'm/s'
# 0.2777777777777778
```

## API

- `parse_quantity(text: str) -> Quantity` — parses `<number> <unit>`. Raises `UnitsError` with code `input_too_large` when `text` exceeds 200 characters, `parse_error` for malformed syntax or a numeric exponent outside [-100, 100], and `unknown_unit` for an unknown unit.
- `Quantity` — frozen dataclass with `value: Fraction` and `unit: str`; `to(unit: str) -> float` converts the quantity and raises `UnitsError` on failure.
- `convert(text: str, to_unit: str) -> float` — parses `text` and converts to `to_unit`; raises `UnitsError` on failure.
- `dimension_of(unit: str) -> dict[str, int]` — returns base dimensions with zero exponents omitted.
- `UnitsError` — exception with a `code` attribute: `unknown_unit`, `dimension_mismatch`, `parse_error`, or `input_too_large`.

The command line interface has two positional arguments, `quantity` and `target_unit`, and no flags. It prints `repr(result)`, returns 0 on success, 1 on `UnitsError`, and 2 for missing arguments.

## Unit Grammar

- Quantity: `number whitespace unit`; leading or trailing whitespace is rejected.
- Number: optional sign, digits with an optional fraction, and an optional exponent.
- Unit: `factor (('*' | '/') factor)*`
- Factor: `name ('^' optional '-' digits)?`
- `/` applies to the single next factor only (`m/s/s` is `m*s^-2`).
- `1` is the dimensionless unit.
- Unit exponents are limited to `-12..12`; numeric literal exponents are limited to `-100..100`.
- Names are case-sensitive. An exact table name wins over a prefix plus name; otherwise one prefix plus a prefixable table name is accepted.
- SI prefixes: `G`, `M`, `k`, `c`, `m`, `u`, the micro sign, and `n`, on `m`, `g`, `s`, `A`, `mol`, `cd`, `Hz`, `N`, `J`, `W`, `Pa`, `C`, `V`, and `L`.
- There are no parentheses.

Affine temperatures (degree Celsius, Fahrenheit) are out of scope; `K` represents a temperature difference.

## Limitations

- Input quantity text longer than 200 characters raises `UnitsError('input_too_large')`.
- Unit exponents outside `-12..12` and numeric exponents outside `-100..100` raise `UnitsError('parse_error')`.
- The conversion returns a Python float; a final `float()` overflow raises `UnitsError('parse_error')` with message `value out of range`.
- The unit table is fixed; there is no API for registering user-defined units.
- There are no runtime dependencies, no network access, and no affine temperature support.

## Why not pint

`pint` is a full unit library with a much larger feature set. This utility targets the common conversion case with no dependencies, exact `Fraction` factors, and a small fixed grammar that is easy to audit.

## Security

See [docs/SECURITY.md](docs/SECURITY.md).
