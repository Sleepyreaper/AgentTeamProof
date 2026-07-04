# romanize Architecture Baseline

This document fixes the implementation scope for the `romanize` deliverable. Later tasks must follow this contract exactly.

## Constraints

- Python version: 3.10+
- Dependencies: standard library only for library and CLI
- Tests may use `pytest`
- Keep each file small, targeted, and under about 100 lines
- Preserve the existing `LICENSE` exactly as-is: do not edit, move, rename, or replace it

## Package Layout

- `romanize/__init__.py`
- `romanize/core.py`
- `romanize/cli.py`
- `tests/test_romanize.py`
- `README.md`

This task creates only the architecture note and does not create code outside this file.

## Public API Contract

`romanize/__init__.py` must export exactly these public names:

- `to_roman`
- `from_roman`

`romanize/core.py` must define:

- `to_roman(n: int) -> str`
- `from_roman(s: str) -> int`

`romanize/cli.py` must define:

- `main() -> int`

## CLI Contract

Command behavior is fixed as:

- `romanize 1994` prints `MCMXCIV`
- `romanize --from MCMXCIV` prints `1994`

CLI requirements:

- Use `argparse`
- Depend on `romanize.core`
- Write result to standard output
- Exit non-zero on invalid input

## Roman Numeral Rules

Use exactly this rule set:

- Symbols: `I=1`, `V=5`, `X=10`, `L=50`, `C=100`, `D=500`, `M=1000`
- Subtractive pairs: `IV=4`, `IX=9`, `XL=40`, `XC=90`, `CD=400`, `CM=900`
- Valid integer range: `1..3999` inclusive
- Out-of-range integer input must raise `ValueError`
- Invalid Roman numeral input must raise `ValueError`

Pinned examples:

- `to_roman(3) == "III"`
- `to_roman(4) == "IV"`
- `to_roman(1994) == "MCMXCIV"`
- `from_roman("MCMXCIV") == 1994`

Pinned invalid cases:

- `to_roman(0)` raises `ValueError`
- `to_roman(4000)` raises `ValueError`
- `from_roman("")` raises `ValueError`
- `from_roman("IIII")` raises `ValueError`
- `from_roman("VX")` raises `ValueError`

## Validation Baseline

Implementation should stay small and flat:

- no deep nesting
- no oversized files
- no extra modules beyond the listed layout unless a later task explicitly changes scope

Validation should enforce canonical Roman numerals only, so malformed forms are rejected rather than normalized.

## Test Baseline

`tests/test_romanize.py` must cover:

- round-trips for `1`, `4`, `9`, `40`, `1994`, `3999`
- integer error cases for `0` and `4000`
- Roman numeral error cases for `""`, `"IIII"`, and `"VX"`

## Preservation Note

The repository's existing `LICENSE` is in scope for preservation only. It must remain untouched.