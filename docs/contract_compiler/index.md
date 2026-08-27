# Contract compiler documentation

The contract compiler documentation renders validated state and code docstrings.
Executable schemas, source code, tests, and validated manifests remain the
authorities for their respective claims.

Each public frontend adapter documents its implementation and support-profile
versions, supported declarations, refusals, applied defaults, neutral outputs,
and provenance in code docstrings. Sphinx surfaces that contract without
redefining it. The default first-party adapter is pinned LinkML 1.11.1; another
adapter may replace it only behind the same explicit neutral output contract.

```{toctree}
:maxdepth: 1

manifests
```
