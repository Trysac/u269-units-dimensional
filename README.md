# units-dimensional

[![PyPI version](https://img.shields.io/pypi/v/trysac-units-dimensional)](https://pypi.org/project/trysac-units-dimensional/)
[![License: MIT](https://img.shields.io/pypi/l/trysac-units-dimensional)](LICENSE)
[![CI](https://github.com/Trysac/u269-units-dimensional/actions/workflows/ci.yml/badge.svg)](https://github.com/Trysac/u269-units-dimensional/actions/workflows/ci.yml)

Parse quantities such as 9.81 m/s^2 and convert them between units with exact dimensional analysis over SI base dimensions

## Problem

Describe in two or three sentences the concrete problem this utility solves, who hits it, and what
they do today without it. Replace this paragraph when the first real feature lands.

## Install

```sh
pip install trysac-units-dimensional
# or
uv add trysac-units-dimensional
```

Requires Python 3.10 or newer. No runtime dependencies.

## Usage

```python
import units_dimensional

# normalize() trims surrounding whitespace and lower-cases the text.
print(units_dimensional.normalize("  Hello World "))  # -> "hello world"

# Blank input is rejected explicitly instead of returning an empty string.
try:
    units_dimensional.normalize("   ")
except ValueError as exc:
    print(f"rejected: {exc}")
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) and [decisions](docs/decisions/)
- [Testing](docs/TESTING.md) and [security](docs/SECURITY.md)
- [Project record](docs/PROJECT.md) and [stack](docs/STACK.md)
- [Changelog](CHANGELOG.md) and [contributing guide](CONTRIBUTING.md)

## License

[MIT](LICENSE) (c) 2026 Miguel Gomez
