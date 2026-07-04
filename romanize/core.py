"""Core conversion logic for the romanize package.

Contains the shared numeral tables plus to_roman() and from_roman().
from_roman() validates strictly: it decodes the numeral and then
re-encodes the result with to_roman(), rejecting the input unless the
re-encoded canonical form matches exactly. This catches non-canonical
strings such as "IIII" or "VX" that a naive summing parser would accept.
"""

import re

_ROMAN_VALUES = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

_ROMAN_PATTERN = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)

MIN_VALUE = 1
MAX_VALUE = 3999


def to_roman(n: int) -> str:
    """Convert an integer in 1..3999 to its canonical Roman numeral string."""
    _validate_int_range(n)

    result = []
    remaining = n
    for value, symbol in _ROMAN_VALUES:
        if remaining <= 0:
            break
        count, remaining = divmod(remaining, value)
        result.append(symbol * count)

    return "".join(result)


def from_roman(s: str) -> int:
    """Convert a Roman numeral string to its integer value.

    Raises ValueError for empty, malformed, or non-canonical numerals
    (e.g. "IIII", "VX", ""). Validation is strict: the decoded value is
    re-encoded with to_roman() and must match the input exactly.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("expected a non-empty Roman numeral string")

    if not _ROMAN_PATTERN.match(s):
        raise ValueError(f"invalid Roman numeral: {s!r}")

    value = 0
    remaining = s
    for amount, symbol in _ROMAN_VALUES:
        while remaining.startswith(symbol):
            value += amount
            remaining = remaining[len(symbol):]

    if remaining:
        raise ValueError(f"invalid Roman numeral: {s!r}")

    if value < MIN_VALUE or value > MAX_VALUE or to_roman(value) != s:
        raise ValueError(f"invalid Roman numeral: {s!r}")

    return value


def _validate_int_range(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError(f"expected an int, got {type(n).__name__}")
    if n < MIN_VALUE or n > MAX_VALUE:
        raise ValueError(
            f"value {n} out of range: must be between {MIN_VALUE} and {MAX_VALUE}"
        )