import subprocess
import sys
from fractions import Fraction

import pytest

from units_dimensional import Quantity, UnitsError, convert, dimension_of, parse_quantity
from units_dimensional.__main__ import main


def test_convert_speed():
    assert convert("1 km/h", "m/s") == pytest.approx(1000 / 3600)


def test_convert_mile_to_km():
    assert convert("1 mi", "km") == pytest.approx(1.609344)


def test_convert_pound_to_kg():
    assert convert("1 lb", "kg") == pytest.approx(0.45359237)


def test_convert_newton():
    assert convert("1 N", "kg*m/s^2") == pytest.approx(1.0)


def test_convert_energy():
    assert convert("3 kW*h", "MJ") == pytest.approx(10.8)


def test_convert_pascal():
    assert convert("1 Pa", "N/m^2") == pytest.approx(1.0)


def test_dimension_mismatch():
    with pytest.raises(UnitsError) as exc_info:
        convert("2 kg", "m")
    assert exc_info.value.code == "dimension_mismatch"
    assert str(exc_info.value) == "cannot convert kg (mass) to m (length)"


def test_dimension_of_joule():
    assert dimension_of("J") == {"kg": 1, "m": 2, "s": -2}


def test_dimension_of_dimensionless():
    assert dimension_of("1") == {}


def test_parse_quantity_decimal():
    q = parse_quantity("9.81 m/s^2")
    assert q == Quantity(Fraction("9.81"), "m/s^2")


def test_parse_quantity_scientific():
    q = parse_quantity("-3e2 ms")
    assert q.value == Fraction(-300)
    assert q.unit == "ms"


def test_unknown_unit_furlong():
    with pytest.raises(UnitsError) as exc_info:
        convert("1 furlong", "m")
    assert exc_info.value.code == "unknown_unit"
    assert "furlong" in str(exc_info.value)


def test_unknown_unit_kgg():
    with pytest.raises(UnitsError) as exc_info:
        convert("1 kgg", "m")
    assert exc_info.value.code == "unknown_unit"
    assert "kgg" in str(exc_info.value)


def test_parse_error_malformed_div():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("m//s")
    assert exc_info.value.code == "parse_error"


def test_parse_error_malformed_exponent():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("5 m^")
    assert exc_info.value.code == "parse_error"


def test_parse_error_no_number():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("abc")
    assert exc_info.value.code == "parse_error"


def test_input_too_large():
    long_text = "1 " + "m" * 200
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity(long_text)
    assert exc_info.value.code == "input_too_large"


def test_input_exactly_200():
    # 198-digit number (1 followed by 197 zeros) + space + 'm' = 200 chars.
    text_200 = "1" + "0" * 197 + " m"
    assert len(text_200) == 200
    q = parse_quantity(text_200)
    assert q.unit == "m"
    assert q.value == Fraction(10**197)


def test_prefix_ambiguity_minute():
    assert convert("1 min", "s") == pytest.approx(60)


def test_prefix_ambiguity_mile():
    assert convert("1 mi", "ft") == pytest.approx(5280)


def test_prefix_ambiguity_millimetre():
    assert convert("1 mm", "m") == pytest.approx(0.001)


def test_prefix_ambiguity_millisecond():
    assert convert("1 ms", "s") == pytest.approx(0.001)


def test_micro_sign():
    assert convert("1 µm", "m") == pytest.approx(1e-6)


def test_micro_prefix_u():
    assert convert("1 um", "m") == pytest.approx(1e-6)


def test_dimensionless_ratio():
    assert convert("1 m/km", "1") == pytest.approx(0.001)


def test_negative_value():
    assert convert("-5 m", "ft") == pytest.approx(-5 / 0.3048)


def test_exponent_minus2():
    assert convert("1 m^-2", "1/m^2") == pytest.approx(1.0)


def test_division_applies_to_single_factor():
    assert convert("1 m/s/s", "m/s^2") == pytest.approx(1.0)


def test_exponent_out_of_range_positive():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("1 m^13")
    assert exc_info.value.code == "parse_error"


def test_exponent_out_of_range_negative():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("1 m^-13")
    assert exc_info.value.code == "parse_error"


def test_malformed_exponent_plus():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("1 m^+2")
    assert exc_info.value.code == "parse_error"


def test_malformed_exponent_letter():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("1 m^a")
    assert exc_info.value.code == "parse_error"


def test_non_prefixable_base():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("1 kmin")
    assert exc_info.value.code == "unknown_unit"


def test_cli_success(capsys):
    result = convert("1 km/h", "m/s")
    assert main(["1 km/h", "m/s"]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == repr(result)
    assert captured.err == ""


def test_cli_prints_float_repr(capsys):
    assert main(["1 km/h", "m/s"]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "0.2777777777777778"
    assert captured.err == ""


def test_cli_dimension_mismatch(capsys):
    assert main(["2 kg", "m"]) == 1
    captured = capsys.readouterr()
    assert captured.err.strip() == "cannot convert kg (mass) to m (length)"
    assert captured.out == ""


def test_cli_missing_args(capsys):
    assert main([]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "usage" in captured.err.lower()


def test_module_cli_subprocess():
    proc = subprocess.run(
        [sys.executable, "-m", "units_dimensional", "1 km/h", "m/s"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == "0.2777777777777778"
    assert proc.stderr == ""


def test_numeric_exponent_too_large():
    with pytest.raises(UnitsError) as exc_info:
        parse_quantity("1e999999999 m")
    assert exc_info.value.code == "parse_error"


def test_conversion_overflow_is_units_error():
    quantity = Quantity(Fraction(10**400), "m")
    with pytest.raises(UnitsError) as exc_info:
        quantity.to("m")
    assert exc_info.value.code == "parse_error"
