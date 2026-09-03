"""Stage one ontology attempt: extract, compile, retain the receipt or acceptance.

Usage: stage_ontology.py --run-dir <ontology-run dir> --attempt N --raw <report file>
       --locator <root locator> --malleus <path> --linkml <path>
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from research.ontology_driven_kg_realization.experiments.document_paper.multimodel import (  # noqa: E402
    BEGIN_ONTOLOGY,
    END_ONTOLOGY,
    acceptance_event,
    extract_delimited,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_compile import (  # noqa: E402
    ExactSource,
    OntologyCompileRefusal,
    compile_exact_ontology,
    publish_compilation,
)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _write_new(path: Path, source: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--attempt", required=True, type=int)
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--locator", required=True)
    parser.add_argument("--malleus", required=True, type=Path)
    parser.add_argument("--linkml", required=True, type=Path)
    args = parser.parse_args()

    raw = args.raw.read_bytes()
    ordinal = f"{args.attempt:02d}"
    _write_new(args.run_dir / f"attempt-{ordinal}.raw.md", raw)
    ontology = extract_delimited(raw.decode("utf-8"), BEGIN_ONTOLOGY, END_ONTOLOGY)
    ontology_path = args.run_dir / f"ontology-{ordinal}.yaml"
    _write_new(ontology_path, ontology)
    print(f"ontology-{ordinal}.yaml {len(ontology)} bytes {_digest(ontology)}")

    malleus = args.malleus.read_bytes()
    linkml = args.linkml.read_bytes()
    try:
        result = compile_exact_ontology(
            root=ExactSource(args.locator, ontology, _digest(ontology)),
            malleus=ExactSource("malleus", malleus, _digest(malleus)),
            linkml_types=ExactSource("linkml:types", linkml, _digest(linkml)),
        )
    except OntologyCompileRefusal as refusal:
        receipt = refusal.canonical_receipt_bytes()
        _write_new(args.run_dir / f"compile-attempt-{ordinal}.json", receipt)
        print(f"REFUSED compile-attempt-{ordinal}.json {_digest(receipt)}")
        print(receipt.decode("utf-8"))
        return 1

    publish_compilation(result, args.run_dir / "compilation")
    acceptance = acceptance_event(_digest(ontology))
    _write_new(args.run_dir / "acceptance.jsonl", acceptance)
    print(
        "ACCEPTED facts",
        len(result.compilation.facts) if hasattr(result.compilation, "facts") else "?",
        "| validated-contract",
        _digest(result.validated_contract_bytes),
        "| receipt",
        _digest(result.receipt_bytes),
        "| acceptance",
        _digest(acceptance),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
