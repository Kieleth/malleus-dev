# Governed statements brought current, 2026-09-19

The skill and ROADMAP edits of commit 3e262945: the one-call admission's entry named (OVR-000468), ROADMAP F1 and F6 current with the seals and the fix of OVR-000469, the CC-D02 finding from the widened declaration scan recorded under F6. The Overlord seals.

## OVR-000470 draft, unsealed

```json
{
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "ledger": "overseer",
  "entry_type": "DOCUMENT_REVISION",
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "subject": {
    "id": "governed-statements-current-2026-09-19",
    "type": "DOCUMENT"
  },
  "entry_id": "OVR-000470",
  "sequence": 470,
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "summary": "Bring the skill's F1 status and ROADMAP F1 and F6 current with OVR-000468 and OVR-000469.",
  "why": "Two governed documents carried statements made stale by the seals of 2026-09-19 and by the fix recorded at OVR-000469. The malleus-dev skill's paragraph on the one-call admission said 'overseer entry to follow'; it now names OVR-000468. ROADMAP F1 said 'Overseer entry pending'; it now records the seal and that the Shop runner template is migrated while the other two-step consumers are not. ROADMAP F6 recorded the stale-measurement defect as one digest in one script; the fix found three stale measurements across CC-X04, CC-X01 and CC-X02, with the four measurement test files outside testpaths as the root cause of the class, and the widened declaration scan surfaced re-declarations of Claim, Evidence, claim_kind and unit in packs/research.yaml and packs/metrology.yaml for CC-D02. F6 now carries the fix, the corrected attribution and that finding. Skill edits are batched with a governed change because the ledger holds every governed document to its latest digest at render (paper ledger E-0494).",
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "path": ".claude/skills/malleus-dev/SKILL.md",
        "change": "MODIFIED",
        "before_digest": "sha256:a135c1634771ed2a81d1562cbee8b092c51f254f5224f14fed21622bf5abfbb5",
        "after_digest": "sha256:931a230b1f2723ff63f236490bb64ecfbf990289d9d20db2e585563e81d2c5c8"
      },
      {
        "path": "ROADMAP.md",
        "change": "MODIFIED",
        "before_digest": "sha256:ac3e4f66eea1f700ae144b33886314b416c877ea4847450ec70e7090c6733867",
        "after_digest": "sha256:e5c3841991c0c5a910a9d5d0b693551f17cb6142b1338febc5ab94867bf27ced"
      },
      {
        "path": "handover/2026-09-19-governed-statements-current.md",
        "change": "CREATED",
        "after_digest": "<digest of this file once final>"
      }
    ]
  },
  "references": [
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "3e262945e22bb44c5e2bfc9fab8cb8f3fe0fd4da"
    },
    {
      "relation": "AFFECTS",
      "type": "WORKSTREAM",
      "target": "CC-R11"
    }
  ]
}
```

## Sealing note for OVR-000470, 2026-09-20

`entries/OVR-000470.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment,
the previous entry hash where placeholdered, and this file's digest filled in.
