"""Display declared inputs using the already frozen exact-frame mechanism."""

import argparse
import hashlib
import json
from pathlib import Path

from input_delivery import frames


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--part", type=int)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_bytes())
    content = {}
    for item in manifest["inputs"]:
        path = root / item["path"]
        if not path.resolve().is_relative_to(root):
            raise ValueError("input escapes packet")
        raw = path.read_bytes()
        if "sha256:" + hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError(f"changed input: {path}")
        content[item["path"]] = frames(item["path"], raw)
    if args.file is None and args.part is None:
        print(json.dumps({name: len(parts) for name, parts in content.items()}))
    elif (
        args.file in content
        and args.part is not None
        and 1 <= args.part <= len(content[args.file])
    ):
        print(content[args.file][args.part - 1])
    else:
        parser.error("select a declared file and valid part")
