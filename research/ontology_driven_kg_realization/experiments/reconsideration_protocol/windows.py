"""The normalised-window measure, for a leak that a substring test cannot find.

When the earlier and the later evidence are two versions of one work, most of
their text is shared and a substring test refuses every honest input. The
measure that works is differential: a run of a fixed width is a leak when the
later text carries it and the earlier one does not. Runs both carry are the
producer's own evidence.

Both sides are cut from the whole text with whitespace collapsed, never from
each block alone. Two readings of one document do not agree on where a block
ends, so a run straddling a join exists in the document and would be missing
from a per-block set; the earlier text's straddling runs then survive the
subtraction and refuse honest output.

The marine document adapter is the consumer of this today, in its exposure
measure and in its assessment containment check. The tracked-file leak gate
uses the same 60-character rule. The Shop adapter measures whole withheld
passages by substring instead and does not use this.
"""

from __future__ import annotations

WIDTH = 60


def plain(text):
    """One normalised run: whitespace collapsed, ends stripped. Nothing else."""
    return " ".join(text.split())


def runs(text, width=WIDTH):
    """Every full-width run of one normalised text, with its offset, in order."""
    for start in range(0, max(1, len(text) - width + 1)):
        piece = text[start : start + width]
        if len(piece) == width:
            yield start, piece


def windows(text, width=WIDTH):
    """The set of runs of one normalised text, for a subtraction or a lookup."""
    return {piece for _, piece in runs(text, width)}


def windows_only_in(later, earlier, width=WIDTH):
    """Runs the later text carries and the earlier one does not.

    Computed from both texts on every call rather than stored: a stored copy
    would itself be a file carrying runs of the later text.
    """
    return windows(plain(later), width) - windows(plain(earlier), width)


def shared_windows(first, second, width=WIDTH):
    """Runs both texts carry. Counted, never refused: this is the honest overlap."""
    return windows(plain(first), width) & windows(plain(second), width)
