"""Explicit identifiers and clock offsets for reusable conformance authoring.

No history, record, check result, or interpreter state is rewritten. The default
preserves the original single-action fixture bytes.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class FixtureEpisode:
    label: str
    offset_minutes: int

    def id(self, original):
        return original if self.label == "1" else original + "~" + self.label

    def time(self, original):
        if self.offset_minutes == 0:
            return original
        value = datetime.fromisoformat(original.replace("Z", "+00:00"))
        return (value + timedelta(minutes=self.offset_minutes)).isoformat().replace(
            "+00:00", "Z"
        )


FIRST = FixtureEpisode("1", 0)
