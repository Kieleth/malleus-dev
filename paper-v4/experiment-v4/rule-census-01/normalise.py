"""The declared normalisation and the number grammar, declared once.

[README.md](README.md) states both in prose; this file is the only place either
is implemented. Every string this cell compares passes through ``normalise``,
and every number it parses out of text comes from ``numbers_in``. No candidate
declares a normalisation of its own.

Two profiles, because one step of the declared normalisation changes a count
either way and neither reading is preferred:

``GLUED``
    All six steps, including closing a single whitespace character between a
    letter and the digit after it, which is what makes ``CO 2`` match ``CO2``.

``UNGLUED``
    The same without that step, which keeps a standalone number the sentence
    states, such as the ``1`` in ``at 1 km``.
"""

from __future__ import annotations

from decimal import Decimal
import re

GLUED = "GLUED"
UNGLUED = "UNGLUED"
PROFILES = (GLUED, UNGLUED)

# U+FB00 to U+FB06, the ligature block the reading's text layer emits.
LIGATURES = {
    0xFB00: "ff",
    0xFB01: "fi",
    0xFB02: "fl",
    0xFB03: "ffi",
    0xFB04: "ffl",
    0xFB05: "st",
    0xFB06: "st",
}

_WS = "[ \t\n\r\v\f ]"
_HYPHEN_BREAK = re.compile(rf"([A-Za-z])-{_WS}+([A-Za-z])")
_SPACED_POINT = re.compile(rf"(\d){_WS}?([.,]){_WS}?(\d)")
_SPACED_DIGITS = re.compile(rf"(\d){_WS}(\d)")
_LETTER_DIGIT = re.compile(rf"([A-Za-z]){_WS}(\d)")
_WHITESPACE = re.compile(rf"{_WS}+")

# Two readings of "a number in the text", both measured, neither preferred.
# FREE: a digit run the text writes on its own, not against a letter and not
# inside a longer run. ATTACHED: every digit run, wherever it sits, so the 3 of
# a segment name and the 2 of a formula count as numbers too.
_FREE = re.compile(r"(?<![^\W_])\d+(?:\.\d+)?")
_ATTACHED = re.compile(r"(?<!\d)(?<!\.)\d+(?:\.\d+)?")
_PLUS_MINUS = re.compile(r"(\d+(?:\.\d+)?)\s*±\s*(\d+(?:\.\d+)?)")
_SIGNS = ("-", "−")

NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}
_WORD = re.compile(
    "(?<![a-z])(" + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + ")(?![a-z])"
)


def _repeat(pattern: re.Pattern[str], replacement: str, text: str) -> str:
    """Apply one rewrite until it reaches a fixed point."""

    while True:
        rewritten = pattern.sub(replacement, text)
        if rewritten == text:
            return text
        text = rewritten


def normalise(text: str, *, profile: str = GLUED) -> str:
    """The declared normalisation, in the declared order."""

    if profile not in PROFILES:
        raise ValueError(f"unknown normalisation profile: {profile!r}")
    text = str(text).translate(LIGATURES)
    text = _repeat(_HYPHEN_BREAK, r"\1\2", text)
    text = _repeat(_SPACED_POINT, r"\1\2\3", text)
    text = _repeat(_SPACED_DIGITS, r"\1\2", text)
    if profile == GLUED:
        text = _repeat(_LETTER_DIGIT, r"\1\2", text)
    return _WHITESPACE.sub(" ", text).strip().casefold()


def as_decimal(value: object) -> Decimal:
    """A typed numeric slot value as an exact decimal, never as a spelling."""

    if isinstance(value, bool):
        raise TypeError("a boolean is not a numeric slot value")
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(repr(value))
    raise TypeError(f"not a numeric slot value: {value!r}")


def _signed(text: str, match: re.Match[str]) -> Decimal:
    """A leading ``-`` is a sign only where it cannot be a range or a hyphen."""

    magnitude = Decimal(match.group(0))
    start = match.start()
    if start == 0 or text[start - 1] not in _SIGNS:
        return magnitude
    before = text[start - 2] if start >= 2 else ""
    if before.isdigit() or before == ".":
        return magnitude
    return -magnitude


def numbers_in(
    text: str, *, profile: str = UNGLUED, attached: bool = False
) -> frozenset[Decimal]:
    """Every number the declared grammar reads out of one normalised string.

    ``attached`` is the second declared reading: with it, a digit run written
    against a letter is a number too.
    """

    folded = normalise(text, profile=profile)
    token = _ATTACHED if attached else _FREE
    found = {_signed(folded, match) for match in token.finditer(folded)}
    found |= {Decimal(NUMBER_WORDS[match.group(1)]) for match in _WORD.finditer(folded)}
    for left, right in _PLUS_MINUS.findall(folded):
        centre, spread = Decimal(left), Decimal(right)
        found |= {centre, spread, centre - spread, centre + spread}
    return frozenset(found)


def contains(value: str, text: str, *, profile: str = GLUED) -> bool:
    """Substring containment after the declared normalisation of both sides."""

    needle = normalise(value, profile=profile)
    return not needle or needle in normalise(text, profile=profile)
