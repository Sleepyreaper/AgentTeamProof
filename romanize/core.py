"""Core conversion logic for the romanize package.

Contains the shared numeral tables and to_roman(). from_roman() will be
added later in this same file.
"""

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


def _validate_int_range(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError(f"expected an int, got {type(n).__name__}")
    if n < MIN_VALUE or n > MAX_VALUE:
        raise ValueError(
            f"value {n} out of range: must be between {MIN_VALUE} and {MAX_VALUE}"
        )