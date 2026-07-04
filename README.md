# romanize

`romanize` is a tiny, dependency-free Python library and command-line tool for converting between integers and Roman numerals.

- Python requirement: 3.10+
- Dependencies: standard library only
- Valid integer range: 1 through 3999

## Install

This project is a small pure-Python package. In a local checkout, install it with:

    pip install .

This makes the library importable and provides the `romanize` command-line tool.

## Library usage

Import the two public functions:

    from romanize import from_roman, to_roman

Convert an integer to a Roman numeral:

    >>> to_roman(1994)
    'MCMXCIV'

Convert a Roman numeral to an integer:

    >>> from_roman("MCMXCIV")
    1994

More examples:

    >>> to_roman(4)
    'IV'
    >>> from_roman("XL")
    40

Invalid inputs raise `ValueError`, including out-of-range integers and invalid Roman numerals.

## CLI usage

Convert an integer to a Roman numeral:

    $ romanize 1994
    MCMXCIV

Convert a Roman numeral to an integer:

    $ romanize --from MCMXCIV
    1994

If the input is invalid, the underlying conversion raises `ValueError` and the CLI reports the error.