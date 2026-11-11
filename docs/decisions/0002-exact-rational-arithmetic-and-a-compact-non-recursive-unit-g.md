# Exact rational arithmetic and a compact non-recursive unit grammar

Status: accepted (generated, pending human review)

## Context

A dependency-free unit conversion utility needed to parse common quantities and convert with exact factors.

## Decision

Represent all conversion factors as `fractions.Fraction`, parse a small grammar without parentheses, and raise typed `UnitsError` on malformed input or dimension mismatch.

## Consequences

No runtime dependencies, exact conversion factors, easy audit, limited to SI and a curated set of imperial units; affine temperatures are out of scope.
