# Contract compiler documentation

The contract compiler documentation renders validated state. Executable
schemas, source code, tests, and validated manifests remain the authorities for
their respective claims.

No public frontend adapter or adapter docstring exists yet. Pinned LinkML
1.11.1 is the selected v0 target adapter. When CC-R02 exposes a public adapter,
its code docstrings must document implementation and support-profile versions,
supported declarations, refusals, applied defaults, neutral outputs, and
provenance. Sphinx must surface that contract without redefining it. Another
adapter may replace LinkML only behind the same explicit neutral output
contract.

```{toctree}
:maxdepth: 1

manifests
```
