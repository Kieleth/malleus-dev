"""Shared pieces of the independent-judge sample tooling.

Four things every script here needs: the repository root, the digest form the
paper records use, the single fenced JSON block a v3 review record carries, and
the shared-run text check the withheld-artifacts method describes. Standard
library only.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parents[3]

SAMPLE_SCHEMA = "malleus.paper-v4.evaluation-sample/v1"
PACKET_SCHEMA = "malleus.paper-v4.evaluation-sample-packet/v1"
JUDGE_RECORD_SCHEMA = "malleus.paper-v4.independent-judge-record/v1"
REVIEW_RECORD_SCHEMA = "malleus.paper-v4.source-grounded-review/v3"

SUPPORT_LABELS = ("SUPPORTED", "PARTIAL", "UNSUPPORTED", "NOT_EVALUABLE")

# paper-v4/experiment-v4/run-23/results/withheld-artifacts.json, check.method
# SHARED_NORMALIZED_CHARACTER_RUN_AGAINST_EVERY_READING_BLOCK with
# UNICODE_WHITESPACE_COLLAPSED_TO_SINGLE_SPACE and the frozen threshold
# NO_PUBLIC_FILE_SHARES_A_60_CHARACTER_RUN.
SHARED_RUN_CHARS = 60

_JSON_BLOCK = re.compile(r"```json\n(?P<record>.*?)\n```", re.DOTALL)


class Refusal(Exception):
    """A named reason to refuse. Never a default, never a repair."""


def refuse(reason: str) -> None:
    raise Refusal(reason)


def digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def read_json(path: Path, subject: str) -> object:
    if not path.exists():
        refuse(f"{subject} is missing: {path}")
    try:
        return json.loads(path.read_bytes())
    except json.JSONDecodeError as error:
        raise Refusal(f"{subject} is not JSON: {path}: {error}") from error


def markdown_record(source: bytes, subject: str) -> dict:
    """The one fenced JSON block of a record, by the rule review.py applies."""

    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Refusal(f"{subject} must be UTF-8 Markdown") from error
    blocks = _JSON_BLOCK.findall(text)
    if len(blocks) != 1:
        refuse(f"{subject} must contain exactly one fenced JSON block")
    try:
        root = json.loads(blocks[0])
    except json.JSONDecodeError as error:
        raise Refusal(f"{subject} JSON block is not JSON: {error}") from error
    if not isinstance(root, dict):
        refuse(f"{subject} JSON block must be an object")
    return root


def write_json(path: Path, value: object) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    source = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(source)
    return source


def normalized(text: str) -> str:
    """Unicode whitespace collapsed to a single space, the withheld-artifacts
    normalization."""

    out = []
    for character in text:
        if character.isspace() or unicodedata.category(character) in {"Zs", "Zl", "Zp"}:
            out.append(" ")
        else:
            out.append(character)
    return re.sub(r" +", " ", "".join(out)).strip()


def runs(text: str, length: int) -> set[str]:
    if len(text) < length:
        return set()
    return {text[index : index + length] for index in range(len(text) - length + 1)}


def reading_run_index(reading: dict, length: int = SHARED_RUN_CHARS) -> set[str]:
    """Every normalized character run of that length in every reading block."""

    index: set[str] = set()
    for page in reading.get("pages", []):
        for block in page.get("blocks", []):
            index |= runs(normalized(block.get("text", "")), length)
    return index


def shared_run(text: str, index: set[str], length: int = SHARED_RUN_CHARS) -> str | None:
    """The first run this text shares with the reading, or None."""

    for run in sorted(runs(normalized(text), length)):
        if run in index:
            return run
    return None


def reading_blocks(reading: dict) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for page in reading.get("pages", []):
        for block in page.get("blocks", []):
            block_id = block.get("id")
            if not isinstance(block_id, str) or not block_id:
                refuse("selected reading carries a block without an id")
            if block_id in blocks:
                refuse(f"selected reading block id is not unique: {block_id}")
            blocks[block_id] = block.get("text", "")
    return blocks


def load_sample(path: Path) -> dict:
    sample = read_json(path, "sample file")
    if not isinstance(sample, dict):
        refuse("sample file must be an object")
    if sample.get("schema") != SAMPLE_SCHEMA:
        refuse(f"sample schema is not {SAMPLE_SCHEMA}: {sample.get('schema')!r}")
    return sample
