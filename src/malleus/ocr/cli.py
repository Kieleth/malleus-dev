"""Verify a bundle document from the command line.

The library boundary is `verify_bundle`. This is the operator's path to it:
an adapter that emits JSON needs no Python object model to be judged, which is
the difference between a profile and a private module.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from malleus import __version__
from malleus.ocr.bundle import PROFILE_ID, PROFILE_VERSION, Bundle, BundleError
from malleus.ocr.conformance import CASES, load_case
from malleus.ocr.verify import (
    CAPABILITY,
    CHECK_FAILED,
    NOT_CHECKED,
    ONTOLOGY,
    VerificationResult,
    profile_registry,
    verify_bundle,
)
from malleus.ontology import bundled_ontology_path

CONFORMS = 0
REFUSED = 1
UNREADABLE = 2


def _header(stream) -> None:
    registry = profile_registry()
    print(f"MALLEUS OCR :: {PROFILE_ID} {PROFILE_VERSION}, capability {CAPABILITY}", file=stream)
    print(
        f"malleus {__version__}, ontology {bundled_ontology_path(*ONTOLOGY)} "
        f"({registry.content_hash()[:12]}…)",
        file=stream,
    )


def _report(result: VerificationResult, stream) -> int:
    """Two answers, printed as two. Integrity is a bit; coverage is a census.

    Printing only the bit is what made "passed" mean "passed what": a bundle
    that read nothing took the same word as one that read everything.
    """
    account = result.account
    for diagnostic in result.diagnostics:
        print(diagnostic, file=stream)
    integrity = "sound" if result.conforms else (
        f"{len(result.diagnostics)} diagnostic"
        f"{'' if len(result.diagnostics) == 1 else 's'}"
    )
    print(f"integrity: {integrity}", file=stream)
    print(f"claim:     {account.kind}", file=stream)
    for unit in account.units:
        print(f"  {unit.unit}: {unit.outcome} [{unit.disposition}]", file=stream)
    for metric in account.metrics:
        print(f"  {metric}", file=stream)
    if not result.conforms:
        print("REFUSED. The paperwork does not hold together.", file=stream)
        return REFUSED
    if account.kind != "FINISHED_READING":
        print("REGISTERED. The source is held and not read; this is not a reading.",
              file=stream)
        return CONFORMS
    if not account.complete:
        # Two lists, not one. "Unaccounted" was one word for two jobs: a unit
        # nobody fetched is fetched, a unit whose call failed is retried, and
        # an operator handed a single list has to open the bundle to find out
        # which they are looking at.
        never = ", ".join(account.units_with(NOT_CHECKED)) or "none"
        failed = ", ".join(account.units_with(CHECK_FAILED)) or "none"
        print("INCOMPLETE. Paperwork sound, and sound paperwork is not a reading.",
              file=stream)
        print(f"  never checked: {never}", file=stream)
        print(f"  check failed:  {failed}", file=stream)
        return REFUSED
    print(f"COMPLETE. {result.bundle_id} accounts for every declared unit and meets "
          "the thresholds its source class froze before ingest.", file=stream)
    return CONFORMS


def _verify(path: Path, stream) -> int:
    try:
        document = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        print(f"cannot read {path}: {error}", file=stream)
        return UNREADABLE
    try:
        bundle = Bundle.from_document(document)
    except BundleError as error:
        print(f"not a bundle document: {error}", file=stream)
        return UNREADABLE
    return _report(verify_bundle(bundle), stream)


def _conformance(stream) -> int:
    """Run the packaged cases. An adapter runs this to prove the wiring works.

    A verifier that refuses nothing is indistinguishable from one that is not
    running, so the corpus carries refusals as well as an accepted bundle.
    """
    worst = CONFORMS
    for name in CASES:
        case = load_case(name)
        result = verify_bundle(Bundle.from_document(case["document"]))
        observed = sorted(set(result.codes()))
        expected = sorted(case["expect"])
        complete = result.account.complete
        # The census, not only the bit. A case agreeing on diagnostics and on
        # completeness can still disagree about what happened to a unit, and
        # that disagreement is the one this suite exists to catch.
        census = {u.unit: [u.outcome, u.disposition] for u in result.account.units}
        ok = (observed == expected
              and complete == case["expect_complete"]
              and census == case["expect_units"])
        verdict = "ok  " if ok else "FAIL"
        print(f"{verdict} {name}: diagnostics {observed or 'none'} "
              f"(expected {expected or 'none'}), complete={complete} "
              f"(expected {case['expect_complete']})", file=stream)
        if census != case["expect_units"]:
            print(f"     census {census} (expected {case['expect_units']})", file=stream)
        if not ok:
            worst = REFUSED
    print("conformance suite passed" if worst == CONFORMS else "conformance suite FAILED", file=stream)
    return worst


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="malleus-ocr",
        description="Verify a document evidence bundle. This performs no OCR.",
    )
    parser.add_argument(
        "document",
        nargs="?",
        type=Path,
        help="a bundle document to verify",
    )
    parser.add_argument(
        "--conformance",
        action="store_true",
        help="run the packaged conformance cases instead of a document",
    )
    parser.add_argument(
        "--case",
        choices=CASES,
        help="verify one packaged case by name",
    )
    arguments = parser.parse_args(argv)
    chosen = [bool(arguments.document), arguments.conformance, bool(arguments.case)]
    if sum(chosen) != 1:
        parser.error("give exactly one of a document path, --case, or --conformance")
    _header(sys.stdout)
    print("=" * 60)
    if arguments.conformance:
        return _conformance(sys.stdout)
    if arguments.case:
        # A case file wraps a document with its expectation. Naming the case is
        # explicit; sniffing the shape of an arbitrary JSON file would be the
        # reader guessing, which is the habit this profile exists to refuse.
        case = load_case(arguments.case)
        print(f"case {case['case']}: {case['description']}", file=sys.stdout)
        return _report(verify_bundle(Bundle.from_document(case["document"])), sys.stdout)
    return _verify(arguments.document, sys.stdout)


if __name__ == "__main__":
    raise SystemExit(main())
