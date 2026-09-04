# arXiv source bundle

Build the manuscript from this directory with the system TeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The resulting `main.pdf` is a build artifact and must not be committed here.

## Run the active paper test gate

Use the locked paper interpreter. The manifest excludes superseded and retired
experiment trees by construction and supplies the repository import path:

```sh
malleus_paper_env="$PWD/private/paper-v4-cp312"
"$malleus_paper_env/bin/python" paper-v4/run_active_tests.py
```

## Reproduce the experiment

Run these commands from the repository root at the commit tagged `paper-v4-multimodel-v2`. That coordinate contains the v2 experiment, the two further producer runs, their human ratification records, the environment lock, and the drivers. It is based on Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`. The paper coordinate is outside the five experiment identities.

The ignored publisher PDF must already exist at the path named by `paper-v4/source/source-manifest.json`. The commands require CPython 3.12.9 on macOS arm64. Both output paths must be absent.

```sh
malleus_paper_root="$PWD"
malleus_paper_env="$malleus_paper_root/private/paper-v4-cp312"
malleus_paper_scratch="$malleus_paper_root/private/paper-v4-v2-reproduction"

test ! -e "$malleus_paper_env"
test ! -e "$malleus_paper_scratch"
python3.12 -m venv "$malleus_paper_env"
test "$("$malleus_paper_env/bin/python" -c 'import platform; print(platform.python_version())')" = '3.12.9'
"$malleus_paper_env/bin/python" -m pip install --require-hashes \
  -r "$malleus_paper_root/paper-v4/environment/requirements-cp312-macos-arm64.lock"

PYTHONPATH="$malleus_paper_root:$malleus_paper_root/src" \
"$malleus_paper_env/bin/python" -m research.ontology_driven_kg_realization.experiments.document_paper.text_layer_reading \
  --repo-root "$malleus_paper_root" \
  --source-manifest "$malleus_paper_root/paper-v4/source/source-manifest.json" \
  --output "$malleus_paper_scratch/selected-reading.json"

PYTHONPATH="$malleus_paper_root:$malleus_paper_root/src" \
"$malleus_paper_env/bin/python" -m research.ontology_driven_kg_realization.experiments.document_paper.v2_experiment \
  --repository-root "$malleus_paper_root" \
  --selected-reading "$malleus_paper_scratch/selected-reading.json" \
  --private-run "$malleus_paper_scratch/run" \
  --results "$malleus_paper_scratch/results" \
  --transaction-time '2026-09-03T09:11:42Z'

diff -rq "$malleus_paper_scratch/results" "$malleus_paper_root/paper-v4/experiment-v2/results"
test "$(shasum -a 256 "$malleus_paper_scratch/run/semantic-ledger.jsonl" | cut -d ' ' -f 1)" = \
  'df5327be6abfabfb49342a0663185d81b8a8056211108ca759ea7cac2901e828'
```

## Reproduce the two further producer runs

From the same environment and checkout, each further run is reproduced by the manifest driver with the transaction time retained beside its manifest. Each run manifest names the selected reading at the ignored path `private/paper-v4-text-layer/selected-reading.json`, so the reading produced above is copied there first. Both output paths must be absent.

```sh
mkdir -p "$malleus_paper_root/private/paper-v4-text-layer"
cp "$malleus_paper_scratch/selected-reading.json" "$malleus_paper_root/private/paper-v4-text-layer/selected-reading.json"

for run in claude-sonnet-5 claude-opus-5; do
  run_dir="$malleus_paper_root/paper-v4/experiment-v3/runs/$run"
  scratch="$malleus_paper_root/private/paper-v4-v3-$run-reproduction"
  test ! -e "$scratch"
  mkdir -p "$scratch"
  PYTHONPATH="$malleus_paper_root:$malleus_paper_root/src" \
  "$malleus_paper_env/bin/python" -m research.ontology_driven_kg_realization.experiments.document_paper.multimodel \
    --repository-root "$malleus_paper_root" \
    --manifest "$run_dir/run-manifest.json" \
    --private-run "$scratch/run" \
    --results "$scratch/results" \
    --transaction-time "$(cat "$run_dir/transaction-time.txt")"
  diff -rq "$scratch/results" "$run_dir/results"
done
test "$(shasum -a 256 "$malleus_paper_root/private/paper-v4-v3-claude-sonnet-5-reproduction/run/semantic-ledger.jsonl" | cut -d ' ' -f 1)" = \
  'ce5e890439f93a15daa26c63f54b71fbb044c688ab990ba31f5e7af21d9bbde3'
test "$(shasum -a 256 "$malleus_paper_root/private/paper-v4-v3-claude-opus-5-reproduction/run/semantic-ledger.jsonl" | cut -d ' ' -f 1)" = \
  'ba49c06348d02da215665666109c62c0adc2ca43cc922aa9d3fa9537dec4173a'
```

The manifest-driven harness itself is checked against the v2 run: `paper-v4/experiment-v3/test_v2_fidelity.py` reproduces the v2 recipes, brief, acceptance event, five result files and ledger digest from the v2 manifest.

## The v4 run-02 single-producer run

`paper-v4/experiment-v4/run-02/` holds the fourth run, reported in Section 4.5 of the manuscript. It has no reproducer tag. It lives at the commit that carries that directory, on Core commit `4881b3a040aaafc7600d009a16ae910084ae32c2`, tree `f532210148cc43e84dfcd764742ff5cfffda10a4`. The tag `paper-v4-multimodel-v2` remains the coordinate for the v2 and v3 runs above.

Frozen and public in that directory:

- `run-contract.json`, `producer-input-manifest.json`, `spawn-message.md`: the contract, the eight digest-pinned producer inputs, and the isolation message the producer received.
- `ontology-run/ontology-01.yaml`, `ontology-02.yaml`, `ontology-03.yaml` with `attempt-01-diagnostic.json`, `attempt-02-diagnostic.json`, `attempt-03-diagnostic.json`: the three ontology candidates and the diagnostic each drew.
- `ontology-run/grounding-receipt.json`, `validated-contract.json`, `population-surface.json`, `result.json`: the accepted ontology's grounding receipt, validated contract, population surface of 26 concrete entity and 3 relation record types, and the acquisition record at 3,515 compiled facts.
- `results/census.json` and `results/run-result.json`: the census, 186 of 186 blocks reviewed with 226 assertions fully formalized, 103 partly, none unformalized, and 104 typed gaps; and the run identities, 14 ledger events, 419 entity and 170 relation records, 589 records traced, reopen equal to admitted on receipt and export.
- `results/launch-log.json` and `results/paper-events.json`: the producer launch, the three ontology attempts, the two structural population refusals, and the recorded ontology-acceptance event.
- `results/trace-summary.json` and `results/query-trace-summary.json`: 589 record traces and 126 query witnesses, selected by record id and never by position.
- `results/native-query-binding.json` and `results/transaction-time.txt`: the 21-case type-only binding written after the replay was frozen, and the run's transaction time.
- `results/withheld-artifacts.json`: the digest of every file that is not in this repository.

The query rows are not in this repository. The producer wrote source sentences into `statement` and `description` record properties, so eight files carry reading text and are retained privately under `private/paper-v4-v4-run-02/`: the producer capture `document-population.json`, the retained capture, the population plan, the typed gaps, the ledger `history.jsonl`, the replay receipt, the exported records, and `query/query-result.json`. Each is published by digest in `results/withheld-artifacts.json` and nowhere else. Reopen and replay are reproduced from that retained ledger, not from anything published here.
