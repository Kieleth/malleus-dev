"""Guard the end-to-end producer condition against population-only substitution."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "paper-v4/experiment-v4/run-21"
RUNS = ("sol-e2e-01", "sol-e2e-02")


class EndToEndConditionTests(unittest.TestCase):
    def test_each_run_starts_from_the_original_eight_inputs_and_two_phase_task(self):
        original = json.loads((BASE / "producer-input-manifest.json").read_bytes())
        template = (BASE / "spawn-message.md").read_text()
        for run_id in RUNS:
            with self.subTest(run_id=run_id):
                run = ROOT / "private/paper-v4-answer-demonstration" / run_id
                manifest = json.loads(
                    (run / "producer-input-manifest.json").read_bytes()
                )
                self.assertEqual(manifest["run_id"], run_id)
                self.assertEqual(manifest["core"], original["core"])
                self.assertEqual(
                    manifest["declared_inputs"], original["declared_inputs"]
                )
                self.assertEqual(manifest["producer"]["model_id"], "gpt-5.6-sol")
                self.assertEqual(
                    manifest["producer"]["session"], "FRESH_SINGLE_SESSION"
                )
                self.assertIn(
                    "PRIOR_ONTOLOGY", manifest["producer"]["forbidden_inputs"]
                )
                self.assertEqual(
                    (run / "spawn-message.md").read_text(),
                    template.replace("run-21", run_id).replace(
                        "<PRODUCER_WORKSPACE>", str(run / "producer")
                    ),
                )
                for item in manifest["declared_inputs"]:
                    data = (run / "producer" / item["target"]).read_bytes()
                    self.assertEqual(
                        "sha256:" + sha256(data).hexdigest(), item["sha256"]
                    )
                names = {item["target"] for item in manifest["declared_inputs"]}
                self.assertEqual(len(names), 8)
                self.assertNotIn("inputs/ontology.yaml", names)
                self.assertNotIn("inputs/population-surface.json", names)
                actual = {
                    str(p.relative_to(run / "producer"))
                    for p in (run / "producer").rglob("*")
                    if p.is_file()
                    and p.relative_to(run / "producer").parts[0]
                    in {"inputs", ".claude"}
                }
                self.assertEqual(actual, names)


if __name__ == "__main__":
    unittest.main()
