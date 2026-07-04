"""Command-line interface for the romanize package.

Provides a single main() entry point built on argparse. Supports one
positional integer argument for integer-to-Roman conversion, or a
--from flag for Roman-to-integer conversion. Prints only the
converted value to stdout.

Run directly as a script (e.g. `python -m romanize.cli 1994` or
`python romanize/cli.py 1994`) via the standard __main__ guard below.
"""

import argparse
import sys

from romanize.core import from_roman, to_roman


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="romanize",
        description="Convert between integers and Roman numerals.",
    )
    parser.add_argument(
        "number",
        nargs="?",
        type=int,
        help="an integer (1-3999) to convert to a Roman numeral",
    )
    parser.add_argument(
        "--from",
        dest="from_roman",
        metavar="NUMERAL",
        help="a Roman numeral to convert to an integer",
    )
    return parser


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.from_roman is not None and args.number is not None:
        parser.error("provide either a number or --from, not both")

    if args.from_roman is not None:
        return _run(parser, from_roman, args.from_roman)

    if args.number is not None:
        return _run(parser, to_roman, args.number)

    parser.error("provide either a number or --from NUMERAL")
    return 2


def _run(parser: argparse.ArgumentParser, func, value) -> int:
    try:
        result = func(value)
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())