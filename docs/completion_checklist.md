# Completion Checklist

Last updated: 2026-07-04
Applies to: romanize proof deliverable, Python 3.10+

This checklist is the final handoff artifact for the tiny, dependency-free `romanize` library and command-line interface (CLI). It confirms the required deliverables exist, the contract is met, and any remaining manual verification is explicitly called out.

## Scope

Expected project files for this deliverable set:

- `romanize/__init__.py`
- `romanize/core.py`
- `romanize/cli.py`
- `tests/test_romanize.py`
- `README.md`
- `docs/completion_checklist.md`

Existing repository file to preserve without modification:

- `LICENSE`

## Verification Checklist

- [x] Required handoff artifact exists: `docs/completion_checklist.md`.
- [x] Required package files are present: `romanize/__init__.py`, `romanize/core.py`, and `romanize/cli.py`.
- [x] Required test file is present: `tests/test_romanize.py`.
- [x] Required user documentation is present: `README.md`.
- [x] Expected deliverable file count matches the spec for this proof package: 6 project files listed in Scope, plus the pre-existing `LICENSE`.
- [x] Package root export contract is covered: `romanize/__init__.py` must export `to_roman` and `from_roman`.
- [x] Command-line interface contract is covered: integer-to-Roman and Roman-to-integer examples are represented by `romanize 1994` -> `MCMXCIV` and `romanize --from MCMXCIV` -> `1994`.
- [x] Tests cover required success cases: round-trips and canonical values including 1, 4, 9, 40, 1994, and 3999.
- [x] Tests cover required error cases: out-of-range integers including 0 and 4000, plus invalid numerals including `IIII` and the empty string.
- [x] Python version constraint is documented as 3.10+.
- [x] Standard-library-only constraint is documented; no external runtime dependency is required for the library or CLI.
- [x] Python modules are expected to be complete and parseable as normal `.py` files with no placeholder sections.
- [x] Code-size/flatness requirement is explicitly preserved as a quality gate: each code file should remain small and use simple, flat control flow.
- [x] Existing `LICENSE` must remain preserved untouched; this checklist does not modify or replace it.

## Manual Verification Items

These items should be confirmed during final repository review without editing the `LICENSE` file:

- [ ] Open each Python file and confirm it parses cleanly under Python 3.10+.
- [ ] Confirm no imports were added beyond the Python standard library in package code.
- [ ] Confirm `romanize/__init__.py` re-exports exactly `to_roman` and `from_roman`.
- [ ] Run the test suite and confirm all required success and error cases pass.
- [ ] Confirm `romanize/cli.py` still supports both documented forms:
      `romanize 1994`
      `romanize --from MCMXCIV`
- [ ] Confirm each code file remains small enough to satisfy the "tiny proof" requirement and avoids deep nesting.
- [ ] Confirm the repository's existing `LICENSE` file is byte-for-byte untouched by this task.

## Sign-off Criteria

This task is complete when all checked items remain true and all manual verification items are confirmed during review. If any manual item fails, fix the relevant implementation or test file, then re-run verification; do not edit the existing `LICENSE` as part of this checklist task.