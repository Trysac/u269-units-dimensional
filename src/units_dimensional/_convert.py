from fractions import Fraction

from ._data import format_dimension
from ._errors import UnitsError
from ._parser import parse_unit


def convert_quantity(value: Fraction, unit_expr: str, target_expr: str) -> float:
    """Convert a value from one unit expression to another, returning a float."""
    src_dim, src_scale = parse_unit(unit_expr)
    tgt_dim, tgt_scale = parse_unit(target_expr)
    if src_dim != tgt_dim:
        raise UnitsError(
            "dimension_mismatch",
            f"cannot convert {unit_expr} ({format_dimension(src_dim)}) "
            f"to {target_expr} ({format_dimension(tgt_dim)})",
        )
    result = value * src_scale / tgt_scale
    try:
        return float(result)
    except OverflowError:
        raise UnitsError("parse_error", "value out of range") from None
