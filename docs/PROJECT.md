# Project record

## Objective

Parse quantities such as `9.81 m/s^2` and convert them between units with exact dimensional analysis over SI base dimensions.

## Scope

- Public API: `parse_quantity`, frozen `Quantity` with `value: Fraction`, `unit: str` and `to`, `convert`, `dimension_of`, and `UnitsError` with the codes `unknown_unit`, `dimension_mismatch`, `parse_error`, and `input_too_large`.
- Exact rational factors from `fractions.Fraction`; floating point only for the final result.
- A fixed unit table for SI base and derived units, common imperial units, and SI prefixes on the prefixable names listed in the specification.
- A compact, non-recursive unit grammar with `*`, `/`, `^`, the dimensionless unit `1`, and exponents limited to `-12..12`.
- Input text limited to 200 characters and numeric literal exponents limited to `-100..100`.
- A command line entry point at `units_dimensional.__main__:main` and `python -m units_dimensional`.

## Out of scope

- Affine temperatures such as degree Celsius and Fahrenheit; `K` is a temperature difference.
- Parentheses or any recursive unit-expression grammar.
- User-defined units or a registration API.
- Runtime dependencies, network access, and library I/O.
- Any behavior not provided by the public API and CLI above.

## Timeline

The specification does not record a timeline for this utility.

## Effort metrics

| Metric | Value |
|---|---|
| Tokens (input / output) | 464755 / 61411 |
| Hours (human) | pending measurement |
| Cost (USD) | 0.0870 |

## Factory run u269 (measured from API usage)

| Phase | Model | Batch | Input | Output | Cache write | Cache read | Cost (USD) |
|---|---|---|---|---|---|---|---|
| generation | deepseek-v4-pro | yes | 1433 | 23655 | 0 | 3328 | 0.0479 |
| fix-1 | deepseek-flash | no | 6990 | 2342 | 0 | 19968 | 0.0025 |
| fix-2 | deepseek-flash | no | 5085 | 1051 | 0 | 17664 | 0.0014 |
| audit | deepseek-flash | no | 22754 | 15769 | 0 | 236928 | 0.0136 |
| fix-3 | deepseek-flash | no | 8240 | 4054 | 0 | 82688 | 0.0039 |
| docs | deepseek-flash | no | 59421 | 14540 | 0 | 256 | 0.0176 |

Total: $0.0870. Prices: deepseek line, as measured by its adapter.
