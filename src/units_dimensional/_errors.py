from typing import Literal

Code = Literal["unknown_unit", "dimension_mismatch", "parse_error", "input_too_large"]


class UnitsError(Exception):
    """Raised for unit parsing or conversion failures."""

    def __init__(self, code: Code, message: str):
        self.code = code
        super().__init__(message)
