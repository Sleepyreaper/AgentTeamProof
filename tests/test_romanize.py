"""Tests for the romanize package: core contract + CLI behavior.

SPEC SOURCE: task spec "romanize" ground truth (symbols, subtractive
pairs, range 1..3999, canonical round-trip behavior) and the CLI
examples `romanize 1994` -> "MCMXCIV" / `romanize --from MCMXCIV` -> "1994".
"""

import pytest

import romanize
from romanize.core import to_roman, from_roman
from romanize.cli import main


# ---------------------------------------------------------------------------
# Package import smoke test (public export surface via romanize/__init__.py)
# ---------------------------------------------------------------------------

def test_package_exports_to_roman_and_from_roman():
    # GIVEN the public package import (not the internal core module)
    from romanize import to_roman as pkg_to_roman
    from romanize import from_roman as pkg_from_roman

    # WHEN used for a known value pair
    numeral = pkg_to_roman(1994)
    value = pkg_from_roman("MCMXCIV")

    # THEN the exported functions behave exactly like romanize.core's
    assert numeral == "MCMXCIV", (
        f"expected 'MCMXCIV' from package-level to_roman(1994), got {numeral!r}. "
        "Gil, check romanize/__init__.py exports the correct function."
    )
    assert value == 1994, (
        f"expected 1994 from package-level from_roman('MCMXCIV'), got {value!r}. "
        "Gil, check romanize/__init__.py exports the correct function."
    )
    assert romanize.to_roman is to_roman, (
        "romanize.to_roman should be the same object as romanize.core.to_roman"
    )
    assert romanize.from_roman is from_roman, (
        "romanize.from_roman should be the same object as romanize.core.from_roman"
    )


# ---------------------------------------------------------------------------
# Direct examples from the spec
# ---------------------------------------------------------------------------

def test_to_roman_three_is_iii():
    # GIVEN 3, WHEN converted, THEN "III"
    result = to_roman(3)
    assert result == "III", (
        f"expected 'III' for to_roman(3), got {result!r}. "
        "Gil, check the additive symbol loop."
    )


def test_to_roman_four_is_iv():
    # GIVEN 4, WHEN converted, THEN "IV" (subtractive pair)
    result = to_roman(4)
    assert result == "IV", (
        f"expected 'IV' for to_roman(4), got {result!r}. "
        "Gil, the subtractive pair table may be missing (4, 'IV')."
    )


def test_to_roman_1994_is_mcmxciv():
    # GIVEN 1994, WHEN converted, THEN "MCMXCIV"
    result = to_roman(1994)
    assert result == "MCMXCIV", (
        f"expected 'MCMXCIV' for to_roman(1994), got {result!r}. "
        "Gil, verify M/CM/XC/IV ordering in the values table."
    )


def test_from_roman_mcmxciv_is_1994():
    # GIVEN "MCMXCIV", WHEN parsed, THEN 1994
    result = from_roman("MCMXCIV")
    assert result == 1994, (
        f"expected 1994 for from_roman('MCMXCIV'), got {result!r}. "
        "Gil, check the decode loop sums subtractive pairs correctly."
    )


# ---------------------------------------------------------------------------
# Parameterized round-trips for required values
# ---------------------------------------------------------------------------

REQUIRED_ROUND_TRIP_VALUES = [1, 4, 9, 40, 3999, 1994]


@pytest.mark.parametrize("value", REQUIRED_ROUND_TRIP_VALUES)
def test_to_roman_then_from_roman_round_trips(value):
    # GIVEN a required integer value
    # WHEN converted to Roman and back to int
    numeral = to_roman(value)
    round_tripped = from_roman(numeral)
    # THEN the original value is recovered exactly
    assert round_tripped == value, (
        f"round-trip failed: to_roman({value}) -> {numeral!r} -> "
        f"from_roman -> {round_tripped}, expected {value}. "
        "Gil, to_roman and from_roman must agree on canonical form."
    )


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_value", [0, 4000])
def test_to_roman_out_of_range_raises_value_error(bad_value):
    # GIVEN an out-of-range integer
    # WHEN/THEN to_roman raises ValueError
    with pytest.raises(ValueError):
        to_roman(bad_value)


@pytest.mark.parametrize("bad_numeral", ["IIII", ""])
def test_from_roman_invalid_numeral_raises_value_error(bad_numeral):
    # GIVEN an invalid Roman numeral string
    # WHEN/THEN from_roman raises ValueError
    with pytest.raises(ValueError):
        from_roman(bad_numeral)


# ---------------------------------------------------------------------------
# CLI behavior
# ---------------------------------------------------------------------------

def test_cli_positional_int_prints_roman(capsys):
    # GIVEN `romanize 1994`
    exit_code = main(["1994"])
    captured = capsys.readouterr()

    # THEN it prints "MCMXCIV" and exits cleanly
    assert exit_code == 0
    assert captured.out.strip() == "MCMXCIV", (
        f"expected CLI to print 'MCMXCIV' for `romanize 1994`, got {captured.out!r}"
    )


def test_cli_from_flag_prints_int(capsys):
    # GIVEN `romanize --from MCMXCIV`
    exit_code = main(["--from", "MCMXCIV"])
    captured = capsys.readouterr()

    # THEN it prints "1994" and exits cleanly
    assert exit_code == 0
    assert captured.out.strip() == "1994", (
        f"expected CLI to print '1994' for `romanize --from MCMXCIV`, got {captured.out!r}"
    )