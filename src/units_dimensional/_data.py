from fractions import Fraction
from typing import Final

DIMENSION_ORDER: Final = ("m", "kg", "s", "A", "K", "mol", "cd")
DIMENSION_NAMES: Final = {
    "m": "length",
    "kg": "mass",
    "s": "time",
    "A": "current",
    "K": "temperature",
    "mol": "amount",
    "cd": "luminosity",
}

UNIT_TABLE: Final[dict[str, tuple[dict[str, int], Fraction]]] = {
    "m": ({"m": 1}, Fraction(1)),
    "g": ({"kg": 1}, Fraction(1, 1000)),
    "s": ({"s": 1}, Fraction(1)),
    "A": ({"A": 1}, Fraction(1)),
    "K": ({"K": 1}, Fraction(1)),
    "mol": ({"mol": 1}, Fraction(1)),
    "cd": ({"cd": 1}, Fraction(1)),
    "min": ({"s": 1}, Fraction(60)),
    "h": ({"s": 1}, Fraction(3600)),
    "day": ({"s": 1}, Fraction(86400)),
    "Hz": ({"s": -1}, Fraction(1)),
    "N": ({"kg": 1, "m": 1, "s": -2}, Fraction(1)),
    "J": ({"kg": 1, "m": 2, "s": -2}, Fraction(1)),
    "W": ({"kg": 1, "m": 2, "s": -3}, Fraction(1)),
    "Pa": ({"kg": 1, "m": -1, "s": -2}, Fraction(1)),
    "C": ({"s": 1, "A": 1}, Fraction(1)),
    "V": ({"kg": 1, "m": 2, "s": -3, "A": -1}, Fraction(1)),
    "L": ({"m": 3}, Fraction(1, 1000)),
    "in": ({"m": 1}, Fraction(254, 10000)),
    "ft": ({"m": 1}, Fraction(3048, 10000)),
    "mi": ({"m": 1}, Fraction(1609344, 1000)),
    "lb": ({"kg": 1}, Fraction(45359237, 100000000)),
    "oz": ({"kg": 1}, Fraction(28349523125, 1000000000000)),
}

PREFIXES: Final[dict[str, Fraction]] = {
    "G": Fraction(1_000_000_000),
    "M": Fraction(1_000_000),
    "k": Fraction(1_000),
    "c": Fraction(1, 100),
    "m": Fraction(1, 1000),
    "u": Fraction(1, 1_000_000),
    "\u00b5": Fraction(1, 1_000_000),
    "n": Fraction(1, 1_000_000_000),
}

PREFIXABLE_BASES: Final = frozenset(
    {"m", "g", "s", "A", "mol", "cd", "Hz", "N", "J", "W", "Pa", "C", "V", "L"}
)


def format_dimension(dim: dict[str, int]) -> str:
    """Return a human-readable representation of a dimension dictionary."""
    if not dim:
        return "1"
    if len(dim) == 1:
        sym, exp = next(iter(dim.items()))
        if sym in DIMENSION_NAMES and exp == 1:
            return DIMENSION_NAMES[sym]
    return _expr_with_symbols(dim)


def _expr_with_symbols(dim: dict[str, int]) -> str:
    pos_parts = []
    neg_parts = []
    for sym in DIMENSION_ORDER:
        exp = dim.get(sym, 0)
        if exp == 0:
            continue
        if exp > 0:
            pos_parts.append(sym if exp == 1 else f"{sym}^{exp}")
        else:
            neg_parts.append(sym if exp == -1 else f"{sym}^{-exp}")
    pos_str = "*".join(pos_parts) if pos_parts else "1"
    if not neg_parts:
        return pos_str
    neg_str = "*".join(neg_parts)
    return f"{pos_str}/{neg_str}"
