"""Prove the Prolog normalisation and number grammar equal the census's Python.

The declared normalisation and the number grammar now exist twice: in
``rule-census-01/normalise.py``, which measured the candidates read-only, and in
``rules.pl``, which is what runs at admission because Core's check contract
admits a pinned Prolog program and nothing else (README.md, "Prolog is the only
admissible check implementation").

One shared fixture table goes through both. The normalised string must be
equal and the set of numbers read must be equal, except on the rows carrying a
bare plus-or-minus, where the Prolog produces exactly the extra negative end
the adopted grammar declares. Numbers are compared as exact rationals, so no
float printing enters the comparison.

Nothing here is tuned to anything. A disagreement on any other row is reported
and stops the cell.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
        paper-v4/experiment-v4/content-rules-doc-02/equivalence.py \
        --private private/paper-v4-content-rules-doc-02
"""

from __future__ import annotations

import argparse
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from malleus.logic import fact_declarations

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CENSUS = ROOT / "paper-v4/experiment-v4/rule-census-01"
sys.path.insert(0, str(CENSUS))

import normalise  # noqa: E402

RULES = HERE / "rules.pl"
# A plus-or-minus with no digit before it, allowing the one space the declared
# normalisation leaves. Both lookbehinds are fixed width on purpose.
BARE_PLUS_MINUS = re.compile("(?<![0-9])(?<![0-9] )\u00b1")
FACT_CONTRACT_VERSION = "3"

# The driver reads its texts from JSON and writes what the pinned rule program
# makes of them. It calls only ``normalised/2`` and ``numbers_of/2``, the two
# predicates rules.pl declares for this purpose, and loads the rule bytes the
# contract pins, unchanged.
DRIVER = r"""
:- use_module(library(http/json)).
:- initialization(equivalence_main).
equivalence_main :-
    current_prolog_flag(argv, [Input|_]),
    setup_call_cleanup(
        open(Input, read, Stream),
        json_read_dict(Stream, Texts),
        close(Stream)
    ),
    dict_pairs(Texts, _, Pairs),
    findall(
        Key-_{normal:Normal, numbers:Numbers},
        (   member(Key-Text, Pairs),
            normalised(Text, Normal),
            numbers_of(Text, Parsed),
            findall([M, S], member(n(M, S), Parsed), Numbers)
        ),
        Results
    ),
    dict_pairs(Out, _, Results),
    json_write_dict(current_output, Out, [width(0)]),
    nl,
    halt.
"""


# Every string rule-census-01/test_normalise.py names, in its own order, plus
# the bare plus-or-minus cases the adopted grammar adds. A fixture is a label
# and a string; the label is what a disagreement is reported by.
FIXTURES: tuple[tuple[str, str], ...] = (
    (
        ("ligature-ff", "ﬀ"),
        ("ligature-fi", "ﬁ"),
        ("ligature-fl", "ﬂ"),
        ("ligature-ffi", "ﬃ"),
        ("ligature-ffl", "ﬄ"),
        ("ligature-ft", "ﬅ"),
        ("ligature-st", "ﬆ"),
        ("ligature-word-five", "ﬁve"),
        ("ligature-word-confirmed", "conﬁrmed"),
        ("hyphen-break-space", "sig- ni"),
        ("hyphen-break-newline", "signi-\nficant"),
        ("hyphen-between-words", "mid-atlantic"),
        ("spaced-point-both", "1 . 5"),
        ("spaced-point-left", "1. 5"),
        ("spaced-point-right", "1 .5"),
        ("spaced-digit-run", "1 5 0"),
        ("formula-co2", "CO 2"),
        ("formula-h2o", "H 2O"),
        ("formula-h-2-o", "H 2 O"),
        ("glued-standalone-number", "at 1 km"),
        ("whitespace-run", "  a\t\n\r\v\f  b  "),
        ("case-mgo", "MgO"),
        ("plain-integer", "a value of 991 metres"),
        ("decimal", "a value of 1.5"),
        ("spaced-decimal", "a value of 1 . 5"),
        ("integral-float-spelling", "a value of 991"),
        ("negative", "a shift of -5 units"),
        ("en-dash-range", "between 1.5–2.0 kilometres"),
        ("em-dash-range", "between 10—20"),
        ("word-range", "from 10 to 20 kilometres"),
        ("plus-or-minus", "4.5 ± 0.3"),
        ("plus-or-minus-spaced-digits", "1 . 5 ± 0 . 2"),
        ("ligature-number-word", "we ran ﬁve iterations"),
        ("word-inside-a-longer-word", "the oneness of it"),
        ("word-tendency", "a tendency"),
        ("compound-word", "twenty-five samples"),
        ("percentage", "a 5% increase"),
        ("unit", "12 km"),
        ("thousands-separator", "1,234 events"),
        ("formula-sentence", "CO 2 uptake"),
        ("attached-segment-name", "segment RC3 of the ridge"),
        ("attached-run-start", "991 metres"),
        ("attached-segment", "segment RC3"),
        ("containment-spaced", "the  MgO   content"),
        ("containment-plain", "the MgO content"),
        ("containment-anything", "anything"),
    )
    + tuple(
        (f"number-word-{word}", f"we ran {word} iterations")
        for word in sorted(normalise.NUMBER_WORDS)
    )
    + (
        # The bare plus-or-minus, the one production this cell adds.
        ("bare-plus-or-minus", "a perturbation of ± 0.3 km/s"),
        ("bare-plus-or-minus-tight", "±2"),
        ("bare-plus-or-minus-leading", "± 0.25 percent"),
        ("bare-plus-or-minus-twice", "of ± 0.3 and ± 1"),
        ("bare-plus-or-minus-after-a-word", "shifts of about ± 12"),
        # A pair is still a pair, including one whose left operand is a digit the
        # gluing welded onto a word.
        ("plus-or-minus-after-a-formula", "CO 2 ± 0.3"),
        ("plus-or-minus-chain", "1 ± 2 ± 3"),
    )
)

# Declared before the run: the rows where the two are expected to differ, and
# by exactly what. A row not named here must agree exactly.
EXPECTED_EXTRA: dict[str, tuple[str, ...]] = {
    "bare-plus-or-minus": ("-0.3",),
    "bare-plus-or-minus-tight": ("-2",),
    "bare-plus-or-minus-leading": ("-0.25",),
    "bare-plus-or-minus-twice": ("-0.3", "-1"),
    "bare-plus-or-minus-after-a-word": ("-12",),
}


def ratio(value: object) -> Fraction:
    """One number as an exact rational, whatever spelling it arrived in.

    A Prolog number is the pair ``n(Mantissa, Scale)`` the rule program carries,
    worth ``Mantissa`` times ten to the minus ``Scale``. A Python number is a
    ``Decimal``. Both become the same rational, so no float printing is
    involved on either side.
    """

    if isinstance(value, (list, tuple)):
        mantissa, scale = int(value[0]), int(value[1])
        return (
            Fraction(mantissa, 10**scale)
            if scale >= 0
            else Fraction(mantissa * 10**-scale)
        )
    return Fraction(*Decimal(value).as_integer_ratio())


def prolog(texts: dict[str, str], rules: Path = RULES) -> dict[str, dict]:
    """Run the pinned rule bytes over these texts, in one fresh process."""

    executable = shutil.which("swipl")
    if executable is None:
        raise RuntimeError("SWI-Prolog executable 'swipl' is not available")
    program = (
        ":- set_prolog_flag(character_escapes, true).\n"
        + fact_declarations(FACT_CONTRACT_VERSION)
        + "\n"
        + DRIVER
        + "\n"
        + rules.read_text(encoding="utf-8").rstrip()
        + "\n"
    )
    with tempfile.TemporaryDirectory(prefix="malleus-equivalence-") as directory:
        root = Path(directory)
        (root / "probe.pl").write_text(program, encoding="utf-8")
        (root / "texts.json").write_bytes(
            json.dumps(texts, ensure_ascii=False).encode("utf-8")
        )
        completed = subprocess.run(
            [
                executable,
                "-q",
                "-f",
                str(root / "probe.pl"),
                "--",
                str(root / "texts.json"),
            ],
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
    if completed.returncode != 0 or not completed.stdout.strip():
        detail = completed.stderr.strip() or "no error detail"
        raise RuntimeError(f"the rule program did not answer: {detail}")
    return json.loads(completed.stdout)


def compare(texts: dict[str, str], rules: Path = RULES) -> list[dict]:
    """One row per fixture: what each implementation made of it."""

    answered = prolog(texts, rules)
    rows = []
    for label, text in texts.items():
        found = answered.get(label)
        if found is None:
            rows.append({"label": label, "agrees": False, "reason": "NO_ANSWER"})
            continue
        python_normal = normalise.normalise(text, profile=normalise.GLUED)
        python_numbers = {
            ratio(value)
            for value in normalise.numbers_in(
                text, profile=normalise.GLUED, attached=True
            )
        }
        prolog_numbers = {ratio(value) for value in found["numbers"]}
        extra = {ratio(value) for value in EXPECTED_EXTRA.get(label, ())}
        surplus = prolog_numbers - python_numbers
        rows.append(
            {
                "label": label,
                # The signature of the one production this grammar adds: the
                # normalised text carries a plus-or-minus with no digit before
                # it, and every number only Prolog read is the negation of one
                # Python read. A disagreement without this signature is a
                # disagreement between the two implementations.
                "carries_a_bare_plus_or_minus": bool(
                    BARE_PLUS_MINUS.search(python_normal)
                ),
                "surplus_are_negations": bool(surplus)
                and all(-item in python_numbers for item in surplus),
                "normal_agrees": found["normal"] == python_normal,
                "numbers_agree": prolog_numbers == python_numbers | extra,
                "agrees": (
                    found["normal"] == python_normal
                    and prolog_numbers == python_numbers | extra
                ),
                "declared_extra": list(EXPECTED_EXTRA.get(label, ())),
                "only_in_prolog": sorted(str(item) for item in surplus),
                "only_in_python": sorted(
                    str(item) for item in python_numbers - prolog_numbers
                ),
            }
        )
    return rows


def fixture_texts() -> dict[str, str]:
    return dict(FIXTURES)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private", required=True, type=Path)
    arguments = parser.parse_args(argv)
    private = arguments.private.resolve()
    private.mkdir(parents=True, exist_ok=True)

    rows = compare(fixture_texts())
    disagreeing = [row for row in rows if not row["agrees"]]
    (private / "equivalence-fixtures.json").write_bytes(
        json.dumps(rows, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    )
    print(f"fixtures {len(rows)} disagreeing {len(disagreeing)}", flush=True)
    for row in disagreeing:
        print("  ", row, flush=True)
    return 1 if disagreeing else 0


if __name__ == "__main__":
    raise SystemExit(main())
