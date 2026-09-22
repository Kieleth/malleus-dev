"""The reconsideration protocol: generic modules plus one adapter per consumer.

One protocol runs a staged acquisition in which a producer is asked, at each
declared evidence boundary, to reconsider what it already recorded. The stages
are: freeze the packets, freeze the obligations, build a producer workspace and
check its exposure, launch it, archive its work, verify and hand off its
output, bind the next boundary, assess the reviews under the governing protocol
file, ratify, index and archive.

Nothing here knows a domain. Every domain term, source id, record type, review
question, path and threshold belongs to an adapter, which fills one
``adapter.Adapter`` and calls these modules. A generic module never imports an
adapter; an adapter imports these. ``census.scan`` measures that rather than
asserting it.

Two adapters exist. The Shop progressive-interpretation harness runs over 21
retained rows of one structured source, three stages in a chain, a given
ontology and two pinned Prolog rules. The marine reconsideration harness runs
over one PDF's reading, two stages plus a control branching off one
predecessor, an ontology the producer authors and the run accepts, and four
composed document-path rules. Both are private; this package is what they
share, and ``tests/`` measures the share against both shapes.
"""

from . import (
    adapter,
    archive,
    assessment,
    census,
    digests,
    exposure,
    freeze,
    handoff,
    index,
    launch,
    obligations,
    packets,
    pin,
    producer,
    windows,
)

__all__ = [
    "adapter",
    "archive",
    "assessment",
    "census",
    "digests",
    "exposure",
    "freeze",
    "handoff",
    "index",
    "launch",
    "obligations",
    "packets",
    "pin",
    "producer",
    "windows",
]
