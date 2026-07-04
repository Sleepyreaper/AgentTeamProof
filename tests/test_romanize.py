"""Tests for romanize.core: to_roman / from_roman contract.

SPEC SOURCE: task spec "romanize" ground truth (symbols, subtractive
pairs, range 1..3999, canonical round-trip behavior).
"""

import pytest

from romanize.core import to_roman, from_roman


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
    # GIVEN a required integer value's canonical numeral
    numeral = to_roman(value)
    # WHEN parsed back to int and re-encoded
    result = to_roman(from_roman(numeral))
    # THEN we get the same canonical numeral back
    assert result == numeral, (
        f"expected re-encoding of {numeral!r} to equal itself, got {result!r}. "
        "Gil, this means from_roman/to_roman are not perfect inverses."
    )


# ---------------------------------------------------------------------------
# Error cases: out-of-range integers
# ---------------------------------------------------------------------------

def test_to_roman_zero_raises_value_error():
    # GIVEN 0, which is below the valid range
    # WHEN / THEN to_roman raises ValueError
    with pytest.raises(ValueError):
        to_roman(0)


def test_to_roman_4000_raises_value_error():
    # GIVEN 4000, which is above the valid range
    # WHEN / THEN to_roman raises ValueError
    with pytest.raises(ValueError):
        to_roman(4000)


@pytest.mark.parametrize("bad_value", [-1, -100, 4000, 10000])
def test_to_roman_out_of_range_raises_value_error(bad_value):
    # GIVEN a value outside 1..3999
    # WHEN / THEN to_roman raises ValueError
    with pytest.raises(ValueError):
        to_roman(bad_value)


# ---------------------------------------------------------------------------
# Error cases: invalid numeral strings
# ---------------------------------------------------------------------------

def test_from_roman_iiii_raises_value_error():
    # GIVEN "IIII", a non-canonical (invalid) numeral
    # WHEN / THEN from_roman raises ValueError
    with pytest.raises(ValueError):
        from_roman("IIII")


def test_from_roman_empty_string_raises_value_error():
    # GIVEN "", an empty string
    # WHEN / THEN from_roman raises ValueError
    with pytest.raises(ValueError):
        from_roman("")


@pytest.mark.parametrize(
    "bad_numeral",
    ["VX", "IIII", "", "ABCD", "iv", "MMMM", "IIV", "IL", "VV", "  IV"],
)
def test_from_roman_invalid_numerals_raise_value_error(bad_numeral):
    # GIVEN a malformed or non-canonical numeral string
    # WHEN / THEN from_roman raises ValueError
    with pytest.raises(ValueError):
        from_roman(bad_numeral)


# ---------------------------------------------------------------------------
# Inverse property test over a representative sample
# ---------------------------------------------------------------------------

SAMPLE_VALUES = [1, 2, 3, 4, 5, 9, 10, 14, 40, 49, 90, 99, 400, 444, 900,
                 999, 1000, 1444, 1994, 2023, 3888, 3999]


@pytest.mark.parametrize("value", SAMPLE_VALUES)
def test_inverse_property_to_roman_from_roman(value):
    # GIVEN any value in the representative sample
    # WHEN converted to Roman then back to int
    # THEN the composition is the identity function
    assert from_roman(to_roman(value)) == value, (
        f"inverse property violated for {value}: "
        f"from_roman(to_roman({value})) != {value}. "
        "Gil, this is the core contract — please check it carefully."
    )