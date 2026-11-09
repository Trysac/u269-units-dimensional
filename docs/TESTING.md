# Testing

## Running

```sh
python -m pytest tests/test_units_dimensional.py
```

## Policy

The tests exercise the public API (`import units_dimensional`) and the CLI entry point (`units_dimensional.__main__.main` and `python -m units_dimensional`). They assert return values, exception codes and messages, stdout, stderr, and process return codes. No coverage threshold or conformance marker configuration is present in the repository shown.

## Tiers

There is a single test tier: the unit tests in `tests/test_units_dimensional.py`. No external-tool or conformance tier exists in the repository shown.

## Layout

`tests/test_units_dimensional.py` is the only test file. It covers:

- conversion: `1 km/h` to `m/s`, `1 mi` to `km`, `1 lb` to `kg`, `1 N` to `kg*m/s^2`, `3 kW*h` to `MJ`, `1 Pa` to `N/m^2`;
- dimensions: mismatch (`2 kg` to `m`), `dimension_of('J')`, and the dimensionless unit `1`;
- parsing: decimal `9.81 m/s^2`, scientific `-3e2 ms`, unknown units `furlong` and `kgg`, malformed division `m//s`, malformed exponent `5 m^`, and missing number `abc`;
- limits: input longer than 200 characters, exactly 200 characters, exponents `m^13` and `m^-13`, malformed `m^+2` and `m^a`, non-prefixable `kmin`, and numeric exponent `1e999999999`;
- prefixes and ambiguity: `min`, `mi`, `mm`, `ms`, the micro sign, and `u`;
- arithmetic edges: `1 m/km` to `1`, `-5 m` to `ft`, `m^-2` to `1/m^2`, and `m/s/s` to `m/s^2`;
- CLI: `main` success, printed float repr, dimension mismatch on stderr with return 1, missing arguments with return 2, and the `python -m units_dimensional` subprocess;
- overflow: `Quantity(Fraction(10**400), 'm').to('m')` raises `UnitsError` with code `parse_error`.
