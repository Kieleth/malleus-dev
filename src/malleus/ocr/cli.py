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
    if result.conforms:
        print(f"CONFORMS. {result.bundle_id} preserves lineage at {result.capability}.", file=stream)
        return CONFORMS
    for diagnostic in result.diagnostics:
        print(diagnostic, file=stream)
    plural = "" if len(result.diagnostics) == 1 else "s"
    print(f"REFUSED. {len(result.diagnostics)} diagnostic{plural}.", file=stream)
    return REFUSED


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
        ok = observed == expected
        verdict = "ok  " if ok else "FAIL"
        print(f"{verdict} {name}: expected {expected or 'no diagnostics'}, got {observed or 'none'}", file=stream)
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
