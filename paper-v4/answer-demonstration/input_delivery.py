"""Bounded, exact input display and checks of model-visible tool outputs only."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


CHUNK_CHARS = 6000


def frames(target, data):
    text = data.decode("utf-8")
    identity = sha256(data).hexdigest()
    parts = [text[n : n + CHUNK_CHARS] for n in range(0, len(text), CHUNK_CHARS)]
    if not parts:
        raise ValueError(f"empty required input: {target}")
    return [
        f"BEGIN_INPUT {target} {identity} {n + 1}/{len(parts)}\n{part}\n"
        f"END_INPUT {target} {identity} {n + 1}/{len(parts)}"
        for n, part in enumerate(parts)
    ]


def verify_frames(expected, outputs):
    # Nested tool results can JSON-encode command stdout. Accept exact frames
    # in raw text or either JSON spelling, never just their boundary markers.
    def visible(frame):
        variants = {frame}
        for _ in range(2):
            variants |= {
                json.dumps(value, ensure_ascii=ascii_only)[1:-1]
                for value in tuple(variants)
                for ascii_only in (False, True)
            }
        return any(value in output for value in variants for output in outputs)

    missing = [frame.splitlines()[0] for frame in expected if not visible(frame)]
    if missing:
        raise ValueError("incomplete model-visible delivery: " + "; ".join(missing))


def transcript_evidence(rows, launch):
    identities = [r["payload"]["id"] for r in rows if r["type"] == "session_meta"]
    contexts = [r["payload"] for r in rows if r["type"] == "turn_context"]
    if identities != [launch["thread_id"]] or launch["fork_turns"] != "none":
        raise ValueError("observed producer identity differs from fresh launch")
    if not contexts or any(
        c["model"] != launch["model"] or c["effort"] != launch["reasoning_effort"]
        for c in contexts
    ):
        raise ValueError("observed producer setting differs from explicit launch")
    outputs = [
        r["payload"]["output"]
        for r in rows
        if r["type"] == "response_item"
        and r["payload"]["type"] in {"function_call_output", "custom_tool_call_output"}
    ]
    return [
        output
        if isinstance(output, str)
        else "".join(item["text"] for item in output if item["type"] == "input_text")
        for output in outputs
    ]


def delivery_inputs(run, phase):
    if phase == "initial":
        manifest = json.loads((run / "producer-input-manifest.json").read_bytes())
        return {item["target"]: item["sha256"] for item in manifest["declared_inputs"]}
    if phase != "accepted":
        raise ValueError("delivery phase must be initial or accepted")
    diagnostic_path = run / "producer/accepted/diagnostic.json"
    diagnostic = json.loads(diagnostic_path.read_bytes())
    return {
        "accepted/diagnostic.json": "sha256:"
        + sha256(diagnostic_path.read_bytes()).hexdigest(),
        "accepted/population-surface.json": diagnostic["population_surface_sha256"],
    }


def input_frames(run, phase):
    result = {}
    for target, identity in delivery_inputs(run, phase).items():
        data = (run / "producer" / target).read_bytes()
        if "sha256:" + sha256(data).hexdigest() != identity:
            raise ValueError(f"delivery input changed: {target}")
        result[target] = frames(target, data)
    return result


def verify_delivery(run, phase):
    launch = json.loads((run / "launch.json").read_bytes())
    rows = [
        json.loads(line)
        for line in Path(launch["metadata_source"]).read_text().splitlines()
    ]
    outputs = transcript_evidence(rows, launch)
    expected = input_frames(run, phase)
    verify_frames([frame for group in expected.values() for frame in group], outputs)
    return {
        "status": "EXACT_FRAMES_OBSERVED_IN_TOOL_OUTPUTS",
        "phase": phase,
        "thread_id": launch["thread_id"],
        "model": launch["model"],
        "reasoning_effort": launch["reasoning_effort"],
        "frames_per_input": {name: len(group) for name, group in expected.items()},
        "limit": "Delivery only, not comprehension or semantic capture.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--phase", choices=("initial", "accepted"), required=True)
    parser.add_argument("--target")
    parser.add_argument("--part", type=int)
    args = parser.parse_args()
    content = input_frames(args.run, args.phase)
    if args.target is None and args.part is None:
        print(json.dumps({name: len(group) for name, group in content.items()}))
    elif (
        args.target in content
        and args.part is not None
        and 1 <= args.part <= len(content[args.target])
    ):
        print(content[args.target][args.part - 1])
    else:
        parser.error("select a declared target and a part in its reported range")
