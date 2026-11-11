import re
from fractions import Fraction
from typing import Final

from ._data import PREFIXABLE_BASES, PREFIXES, UNIT_TABLE
from ._errors import UnitsError

_NUMBER_RE: Final = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE]([+-]?\d+))?$")
_MAX_NUMBER_EXPONENT: Final = 100


def parse_number(text: str) -> Fraction:
    """Parse a numeric literal into an exact Fraction."""
    match = _NUMBER_RE.match(text)
    if not match:
        raise UnitsError("parse_error", f"invalid number '{text}'")
    exp_group = match.group(1)
    if exp_group is not None:
        exponent = int(exp_group)
        if abs(exponent) > _MAX_NUMBER_EXPONENT:
            raise UnitsError(
                "parse_error",
                f"numeric exponent out of range [-{_MAX_NUMBER_EXPONENT}, {_MAX_NUMBER_EXPONENT}]",
            )
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError):
        raise UnitsError("parse_error", f"invalid number '{text}'") from None


def parse_unit(unit_expr: str) -> tuple[dict[str, int], Fraction]:
    """Parse a unit expression.

    Returns a tuple (dimension, scale) where dimension is a dict of base dimensions
    to integer exponents and scale is the exact factor to SI base units.
    """
    if not unit_expr:
        raise UnitsError("parse_error", "empty unit expression")

    dim: dict[str, int] = {}
    scale = Fraction(1)
    i = 0
    n = len(unit_expr)
    last_op = "*"
    expect_factor = True

    while i < n:
        ch = unit_expr[i]
        if ch in "*/":
            if expect_factor:
                raise UnitsError("parse_error", f"unexpected operator '{ch}'")
            last_op = "*" if ch == "*" else "/"
            i += 1
            expect_factor = True
            continue

        if not expect_factor:
            raise UnitsError("parse_error", f"unexpected character '{ch}'")

        start = i
        if unit_expr[i] == "1":
            # '1' is the dimensionless unit.
            i += 1
        else:
            while i < n and (unit_expr[i].isalpha() or unit_expr[i] == "\u00b5"):
                i += 1
        if i == start:
            raise UnitsError("parse_error", f"unexpected character '{ch}'")
        name = unit_expr[start:i]

        exponent = 1
        if i < n and unit_expr[i] == "^":
            i += 1
            sign = 1
            if i < n and unit_expr[i] == "-":
                sign = -1
                i += 1
            elif i < n and unit_expr[i] == "+":
                raise UnitsError("parse_error", "unexpected '+' in exponent")
            if i >= n or not unit_expr[i].isdigit():
                raise UnitsError("parse_error", "malformed exponent")
            digits_start = i
            while i < n and unit_expr[i].isdigit():
                i += 1
            digits = unit_expr[digits_start:i]
            try:
                exp_val = int(digits)
            except ValueError:
                raise UnitsError("parse_error", "malformed exponent") from None
            if exp_val < -12 or exp_val > 12:
                raise UnitsError("parse_error", "exponent out of range [-12, 12]")
            exponent = sign * exp_val

        if name == "1":
            factor_dim: dict[str, int] = {}
            factor_scale = Fraction(1)
        elif name in UNIT_TABLE:
            factor_dim, base_scale = UNIT_TABLE[name]
            factor_scale = base_scale
        else:
            prefix = name[:1]
            if prefix in PREFIXES and name[1:] in UNIT_TABLE and name[1:] in PREFIXABLE_BASES:
                prefix_scale = PREFIXES[prefix]
                factor_dim, base_scale = UNIT_TABLE[name[1:]]
                factor_scale = prefix_scale * base_scale
            else:
                raise UnitsError("unknown_unit", f"unknown unit '{name}'")

        final_exponent = exponent
        if last_op == "/":
            final_exponent = -final_exponent

        for sym, exp in factor_dim.items():
            new_exp = dim.get(sym, 0) + exp * final_exponent
            if new_exp == 0:
                dim.pop(sym, None)
            else:
                dim[sym] = new_exp

        if final_exponent != 0:
            scale *= factor_scale**final_exponent

        expect_factor = False

    if expect_factor:
        raise UnitsError("parse_error", "unit expression ends with operator")

    return dim, scale
