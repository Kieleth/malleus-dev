# CC-X03 generic source-boundary RED ledger

Status: formal exploratory RED evidence. No GREEN implementation or policy choice.

## Authority and scope

CC-X03 was reactivated at `17c4c21ee02a80fd2b963f47ba0ff3e37fcfd270`
with `EXPLORATION_ONLY` authority. The first candidate commit is
`4788fdebfa8ad7c46ec7d6b47ab0ab4079a99a8f`, tree
`8e7c6dcbf34958dd7d6376d55b739bf89d2464cc`.

The registered candidate surface is exactly:

- `conformance/contract_kernel/v0/source_boundary/test_source_boundary.py`
- `conformance/contract_kernel/v0/source_boundary/EXPLORATORY_LEDGER.md`
- `conformance/contract_compiler/v0/evidence/CC-X03.json`

The test commit contains only the generic test module. The older quarantined
history at `d32b9c6458a2ec66f591e85299a80f0c3952c6fb` is not part of this candidate
history and supplies no authority. No Quiet Bell or other themed vocabulary is
present.

## Execution context

Observed in `/Users/luis/Projects/malleus-dev/.venv` on 2026-08-26:

- CPython `3.12.9`, Darwin arm64
- `linkml==1.11.1`
- `linkml-runtime==1.11.1`
- `PyYAML==6.0.3`
- `pytest==9.1.1`
- `hbreader==0.9.1`
- `jsonasobj2==1.0.4`

These are observations of the available environment, not new dependency or
release decisions.

## Exact RED

Collection command:

```text
.venv/bin/python -m pytest --collect-only -q conformance/contract_kernel/v0/source_boundary/test_source_boundary.py
```

Result: exit `0`; eight tests collected in `0.15s`. The `boundary` import is
inside the final test, so the module and all controls collect.

Passing-control command:

```text
.venv/bin/python -m pytest -q conformance/contract_kernel/v0/source_boundary/test_source_boundary.py -k 'not future_boundary_seam'
```

Result: exit `0`; `7 passed, 1 deselected in 0.38s`.

Full focused command:

```text
.venv/bin/python -m pytest -q conformance/contract_kernel/v0/source_boundary/test_source_boundary.py
```

Result: exit `1`; `1 failed, 7 passed in 0.38s`.

Exact failing node:

```text
conformance/contract_kernel/v0/source_boundary/test_source_boundary.py::test_future_boundary_seam_is_not_implemented
```

Exact exception and message:

```text
ModuleNotFoundError: No module named 'boundary'
```

This is the only deliberate RED. `boundary` is a test-local name for a future
seam. This evidence does not define that seam's interface or authorize its
implementation.

## Raw LinkML Runtime observations

The seven passing controls observed:

1. `YAMLLoader.loads` passed the exact multi-line `str` object into
   `Loader._read_source`. Object identity and every source character, including
   trailing spaces inside a block scalar, were retained at that call boundary.
   The constructed schema name was `root`.
2. A duplicate top-level `name` key raised exact built-in type `ValueError`,
   args `('Duplicate key: "name"',)`, and message `Duplicate key: "name"`.
3. A temporary local root importing one temporary child produced raw closure
   `['child', 'root']` and reached `builtins.open` twice, first for the supplied
   root and then for a distinct imported path.
4. A root importing `https://network.invalid/child` reached
   `hbreader.urlopen` once. The intercepted raw request URL was
   `https://network.invalid/child.yaml`; the interception raised built-in
   `RuntimeError` with args `('intercepted URL read',)`. No network request was
   executed.
5. The in-memory nested diamond `root -> left, right` and `left, right ->
   common` produced raw closure `['common', 'left', 'right', 'root']`.
6. A missing local import raised exact built-in type `FileNotFoundError`, errno
   `2`, and leading args `(2, 'No such file or directory')`. Its `filename` was
   the temporary missing child path selected by the installed runtime.
7. The in-memory two-module cycle `first -> second -> first` produced raw
   closure `['first', 'second']`.

The in-memory subclass replaces only `SchemaView.load_import` with a dictionary
lookup so `SchemaView.imports_closure` itself remains the code under
observation. The file and URL controls use unmodified `SchemaView.load_import`.

## Inspected call paths

Installed source inspection found these paths:

```text
YAMLLoader.loads
  Loader.load
  YAMLLoader.load_any
  YAMLLoader.load_as_dict
  Loader._read_source
  hbreader.hbread
  yaml.load(StringIO(exact_text), DupCheckYamlLoader)
  Loader._construct_target_class
```

```text
SchemaView.imports_closure
  SchemaView.load_import
  load_schema_wrap
  YAMLLoader.load
  YAMLLoader.load_any
  YAMLLoader.load_as_dict
  Loader._read_source
  hbreader.hbread
  hbreader.hbopen
  builtins.open or hbreader.urlopen
```

The inspected implementations are in
`linkml_runtime/loaders/loader_root.py`,
`linkml_runtime/loaders/yaml_loader.py`,
`linkml_runtime/utils/schemaview.py`, and `hbreader/__init__.py` inside the
observed virtual environment.

## Decisions not taken

These raw results do not assert or select a locator grammar, an import suffix
rule, resolver precedence, import-order meaning, cycle policy, fallback,
stable diagnostic contract, module identity, or semantic winner. They do not
classify any observed behavior as correct or incorrect.

CC-X03 adds no production or GREEN code, ontology or themed vocabulary,
dependency, Docker, release, migration, network fetch, semantic merge, or
import policy. Standard pytest excludes this conformance path by its configured
`testpaths`, so the deliberate RED does not alter the normal regression gate.

## Adjacent validation

The configured standard suite passed with `1655 passed, 2 skipped in 109.60s`.
The overseer ledger check validated 119 entries at `OVR-000119`, the integration
check validated 66 workstreams, 10 cards, and 4 selections, and their focused
test modules passed `74 passed in 23.95s`. Scoped Ruff and `git diff --check`
also passed. The verification report records artifact bytes and the final
candidate is still subject to `validate_candidate_history` against the exact
base, head, tree, and three registered paths after its enclosing commit exists.
