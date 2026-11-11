# Security

The library parses untrusted quantity and unit strings using a fixed grammar and a fixed unit table. It performs no network access, filesystem access, authentication, or secret handling.

## Defended

- Input length: `parse_quantity` rejects its `text` argument when longer than 200 characters with `UnitsError('input_too_large')`; exactly 200 characters is accepted.
- Unit exponents: every factor exponent must be in `-12..12`; an exponent outside that range raises `UnitsError('parse_error')`.
- Recursion: the grammar has no parentheses and `parse_unit` is iterative, so parser depth is fixed.
- Numeric exponents: a numeric literal exponent outside `-100..100` raises `UnitsError('parse_error')`.
- Exact arithmetic: conversion factors are `fractions.Fraction`; float conversion happens only for the final result. If the final `float()` overflows, the code raises `UnitsError('parse_error')` with message `value out of range`.
- Fixed vocabulary: only names in the unit table and one prefix plus a prefixable table name are accepted; anything else raises `UnitsError('unknown_unit')`.
- Error messages: parsing errors echo at most the token or unit name being parsed, and the 200-character limit on `parse_quantity` text is checked before parsing.

## Not defended

- No authentication, authorization, sandboxing, or per-call resource quota beyond the length and exponent limits above.
- No defense against CPU or memory exhaustion from inputs inside the allowed limits, such as a 200-character numeric literal or a numeric exponent of 100.
- The `to_unit` argument of `convert` and `Quantity.to`, and the CLI `target_unit`, are not covered by the 200-character gate; a large target expression can appear in a dimension-mismatch error.
- No affine temperature handling; Celsius and Fahrenheit are out of scope, and `K` is a temperature difference.
- No secret handling; the library contains no secrets.
- No protection against downstream misuse of the returned float, including precision loss after conversion.
