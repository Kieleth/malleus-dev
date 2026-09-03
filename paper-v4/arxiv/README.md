# arXiv source bundle

Build the manuscript from this directory with the system TeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The resulting `main.pdf` is a build artifact and must not be committed here.

## Reproduce the experiment

Run these commands from the repository root at exact paper reproducer commit `8e818103e6867e326544123a30abe756bdd45117`, tree `455e91e3110d1789fb3db8c8a902bc2e87c4eb04`. That local coordinate contains the v2 experiment, environment lock, and driver. It is based on Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`. The paper coordinate is outside the five experiment identity groups and is not claimed as pushed or public.

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
