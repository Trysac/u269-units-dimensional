import sys
from argparse import ArgumentParser

from . import UnitsError, convert


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(
        prog="units_dimensional", description="Convert quantities between units"
    )
    parser.add_argument("quantity", help="quantity with unit, e.g. '1 km/h'")
    parser.add_argument("target_unit", help="target unit, e.g. 'm/s'")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # Missing arguments make argparse exit with status 2; honour the
        # ``main(argv) -> int`` contract by returning that status instead.
        if exc.code == 2:
            return 2
        raise
    try:
        result = convert(args.quantity, args.target_unit)
    except UnitsError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(repr(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
