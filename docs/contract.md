# romanize Behavioral Contract

This document defines the observable behavior of the `romanize` library and CLI. It is implementation-free and is intended to be precise enough to write tests directly.

## Library API

The package exposes two functions:

- `to_roman(n: int) -> str`
- `from_roman(s: str) -> int`

No other behavior is defined by this contract.

## Integer to Roman Conversion

Signature:

- `to_roman(n: int) -> str`

Behavior:

- Accepts an integer `n`.
- Valid input range is `1..3999` inclusive.
- Returns the canonical uppercase Roman numeral representation of `n`.
- Output must use only these symbols: `I`, `V`, `X`, `L`, `C`, `D`, `M`.
- Output must follow the subtractive-pair rules defined below.

Required examples:

- `to_roman(3) == "III"`
- `to_roman(4) == "IV"`
- `to_roman(1994) == "MCMXCIV"`
- `to_roman(3999) == "MMMCMXCIX"`

Error behavior:

- `to_roman(0)` must raise `ValueError`.
- `to_roman(4000)` must raise `ValueError`.
- Any integer less than `1` or greater than `3999` must raise `ValueError`.

## Roman to Integer Conversion

Signature:

- `from_roman(s: str) -> int`

Behavior:

- Accepts a Roman numeral string `s`.
- Returns the integer value represented by `s`.
- Accepted numerals are canonical uppercase Roman numerals in the range `1..3999` inclusive.
- Parsing is not permissive: malformed or non-canonical numerals are invalid and must not be normalized.

Required examples:

- `from_roman("III") == 3`
- `from_roman("IV") == 4`
- `from_roman("MCMXCIV") == 1994`
- `from_roman("MMMCMXCIX") == 3999`

Error behavior:

- `from_roman("")` must raise `ValueError`.
- `from_roman("IIII")` must raise `ValueError`.
- `from_roman("VX")` must raise `ValueError`.
- Any numeral outside the supported canonical form for `1..3999` must raise `ValueError`.

## Roman Numeral Rules

Symbol values:

- `I = 1`
- `V = 5`
- `X = 10`
- `L = 50`
- `C = 100`
- `D = 500`
- `M = 1000`

The only allowed subtractive pairs are:

- `IV = 4`
- `IX = 9`
- `XL = 40`
- `XC = 90`
- `CD = 400`
- `CM = 900`

No other subtractive form is valid under this contract.

## Canonical Form Requirement

Roman numerals accepted by `from_roman` and produced by `to_roman` must be canonical.

This means:

- Repetition-based malformed forms such as `IIII` are invalid.
- Invalid ordering such as `VX` is invalid.
- The empty string is invalid.
- Inputs must match the same canonical style used by `to_roman`.

A useful test rule is:

- For every valid input `n` in `1..3999`, `from_roman(to_roman(n)) == n`.

## CLI Contract

Entrypoint behavior:

- `romanize 1994` writes `MCMXCIV` to standard output.
- `romanize --from MCMXCIV` writes `1994` to standard output.

Accepted forms:

- Integer-to-Roman mode:
 `romanize <integer>`
- Roman-to-integer mode:
 `romanize --from <roman_numeral>`

Standard output behavior:

- On success, the converted value is written to stdout as a single line.
- Successful output must be the conversion result only.

Required examples:

 romanize 1994
 MCMXCIV

 romanize --from MCMXCIV
 1994

Exit expectations:

- Successful conversion exits with status code `0`.
- Invalid input exits non-zero.

Invalid CLI cases include, at minimum:

- an integer outside `1..3999`
- an invalid Roman numeral such as `IIII`
- an empty Roman numeral input when such input is passed through the CLI interface

Error formatting is not specified by this contract beyond the non-zero exit requirement for invalid input.