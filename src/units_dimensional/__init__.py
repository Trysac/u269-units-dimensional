"""Exact dimensional analysis for unit conversion.

Parses a compact quantity syntax such as ``9.81 m/s^2`` and converts between
compatible units using rational arithmetic (no floating point until the final
result).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from ._convert import convert_quantity
from ._errors import UnitsError
from ._parser import parse_number, parse_unit

__all__ = [
    "Quantity",
    "UnitsError",
    "__version__",
    "convert",
    "dimension_of",
    "parse_quantity",
]

__version__ = "0.1.0"


@dataclass(frozen=True)
class Quantity:
    """A parsed quantity with an exact value and a unit expression."""

    value: Fraction
    unit: str

    def to(self, unit: str) -> float:
        """Convert this quantity to the given target unit expression."""
        return convert_quantity(self.value, self.unit, unit)


def parse_quantity(text: str) -> Quantity:
    """Parse ``<number> <unit>`` into a Quantity.

    Raises:
        UnitsError: with code 'input_too_large' if ``text`` exceeds 200 characters,
            'parse_error' for malformed syntax, or 'unknown_unit' for an unknown unit.
    """
    if len(text) > 200:
        raise UnitsError("input_too_large", "input exceeds 200 characters")
    if not text or text[0].isspace() or text[-1].isspace():
        raise UnitsError("parse_error", "expected number followed by unit")
    parts = text.split()
    if len(parts) != 2:
        raise UnitsError("parse_error", "expected number followed by unit")
    num_str, unit_str = parts
    value = parse_number(num_str)
    parse_unit(unit_str)  # validate
    return Quantity(value, unit_str)


def convert(text: str, to_unit: str) -> float:
    """Parse ``text`` and convert the quantity to ``to_unit``."""
    quantity = parse_quantity(text)
    return quantity.to(to_unit)


def dimension_of(unit: str) -> dict[str, int]:
    """Return the base dimensions of a unit expression (zero exponents omitted)."""
    dim, _ = parse_unit(unit)
    return dim
