"""Tests for the romanize package: core contract + CLI behavior.

SPEC SOURCE: task spec "romanize" ground truth (symbols, subtractive
pairs, range 1..3999, canonical round-trip behavior) and the CLI
examples `romanize 1994` -> "MCMXCIV" / `romanize --from MCMXCIV` -> "1994".
"""

import pytest

from romanize.core import to_roman, from_roman
from romanize.cli import main


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


@pytest.mark.parametrize("value", REQUIRED_ROUND_TRIP_VALUES)
def test_from_roman_then_to_roman_round_trips(value):
    # GIVEN a required integer value, first rendered to a numeral
    numeral = to_roman(value)
    # WHEN parsed back and re-rendered
    re_rendered = to_roman(from_roman(numeral))
    # THEN the canonical numeral form is stable
    assert re_rendered == numeral, (
        f"round-trip failed: {numeral!r} -> from_roman -> re-rendered as "
        f"{re_rendered!r}, expected {numeral!r} unchanged. "
        "Gil, from_roman and to_roman must be inverses of each other."
    )


# ---------------------------------------------------------------------------
# Error cases: out-of-range integers
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value", [0, -1, 4000, 10000])
def test_to_roman_raises_value_error_for_out_of_range(value):
    # GIVEN an integer outside 1..3999
    # WHEN to_roman is called
    # THEN a ValueError is raised
    with pytest.raises(ValueError):
        to_roman(value)
    # If this test fails, Gil: to_roman must validate 1 <= n <= 3999.


# ---------------------------------------------------------------------------
# Error cases: invalid numerals
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("numeral", ["IIII", "VX", "", "IC", "ABC", "iv"])
def test_from_roman_raises_value_error_for_invalid_numeral(numeral):
    # GIVEN a malformed or non-canonical Roman numeral string
    # WHEN from_roman is called
    # THEN a ValueError is raised
    with pytest.raises(ValueError):
        from_roman(numeral)
    # If this test fails, Gil: from_roman must reject anything that does
    # not round-trip to its own canonical form (e.g. "IIII" is not "IV").


# ---------------------------------------------------------------------------
# CLI behavior: the two documented examples
# ---------------------------------------------------------------------------

def test_cli_prints_roman_numeral_for_integer_argument(capsys):
    # GIVEN the CLI invoked with a positional integer, e.g. `romanize 1994`
    # WHEN main() runs
    exit_code = main(["1994"])
    # THEN it prints the expected Roman numeral and exits cleanly
    captured = capsys.readouterr()
    assert captured.out.strip() == "MCMXCIV", (
        f"expected CLI to print 'MCMXCIV' for `romanize 1994`, "
        f"got {captured.out.strip()!r}. "
        "Gil, check that main() calls to_roman(number) and prints the result."
    )
    assert exit_code == 0, (
        f"expected exit code 0 for a successful conversion, got {exit_code}. "
        "Gil, main() should return 0 on success."
    )


def test_cli_prints_integer_for_from_roman_argument(capsys):
    # GIVEN the CLI invoked with --from, e.g. `romanize --from MCMXCIV`
    # WHEN main() runs
    exit_code = main(["--from", "MCMXCIV"])
    # THEN it prints the expected integer and exits cleanly
    captured = capsys.readouterr()
    assert captured.out.strip() == "1994", (
        f"expected CLI to print '1994' for `romanize --from MCMXCIV`, "
        f"got {captured.out.strip()!r}. "
        "Gil, check that main() calls from_roman(value) and prints the result."
    )
    assert exit_code == 0, (
        f"expected exit code 0 for a successful conversion, got {exit_code}. "
        "Gil, main() should return 0 on success."
    )