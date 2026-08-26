#!/usr/bin/env python3
"""Bounded MCP acquisition and offline-verification adapter for CC-002.

The server accepts no locations or commands from the MCP caller.  Every remote
artifact, digest, platform, output path, subprocess argument, and smoke input is
fixed by the accepted OD-012 baseline and this CC-002 implementation.
"""

from __future__ import annotations

import base64
import csv
import email.policy
import hashlib
import io
import json
import lzma
import os
import platform
import shutil
import socket
import socketserver
import stat
import struct
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import zlib
from dataclasses import dataclass
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping, Sequence, TextIO


REPOSITORY = Path(__file__).resolve().parents[1]
ADAPTER_PATH = Path(__file__).resolve()
OUTPUT_TRUSTED_ROOT = REPOSITORY
DESTINATION = (
    REPOSITORY / "conformance" / "contract_compiler" / "v0" / "compiler_environment"
)
INTERNAL_VERIFICATION = DESTINATION / "verification.json"
DESTINATION_LABEL = "conformance/contract_compiler/v0/compiler_environment"
SMOKE_INPUT = REPOSITORY / "ontology" / "malleus.yaml"

SUPPORTED_PROTOCOL_VERSIONS = (
    "2025-06-18",
    "2025-03-26",
    "2024-11-05",
    "2024-10-07",
)
SERVER_NAME = "malleus-cc002"
SERVER_VERSION = "2"

NETWORK_TIMEOUT_SECONDS = 120
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
SUBPROCESS_DIAGNOSTIC_LIMIT = 4096
ALLOWED_HTTPS_HOSTS = frozenset({"files.pythonhosted.org"})
ACQUISITION_HTTPS_HOSTS = frozenset({"pypi.org", "files.pythonhosted.org"})

DOCKER = "docker"
DOCKER_TRANSPORT = "LOCAL_UNIX_SOCKET"
OCI_PLATFORM = "linux/amd64"
OCI_INDEX_DIGEST = (
    "sha256:fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db"
)
OCI_CHILD_DIGEST = (
    "sha256:97983fa8cc88343512862c62307159a82261c3528dc025f79e5a3f7af43e50b4"
)
OCI_CHILD_REFERENCE = f"docker.io/library/python@{OCI_CHILD_DIGEST}"
OCI_AUTH_URL = (
    "https://auth.docker.io/token?service=registry.docker.io&"
    "scope=repository:library/python:pull"
)
OCI_INDEX_PATH = f"/v2/library/python/manifests/{OCI_INDEX_DIGEST}"
OCI_INDEX_URL = f"https://registry-1.docker.io{OCI_INDEX_PATH}"
OCI_AUTH_HTTPS_HOSTS = frozenset({"auth.docker.io"})
OCI_REGISTRY_HTTPS_HOSTS = frozenset({"registry-1.docker.io"})
OCI_AUTH_RESPONSE_LIMIT = 64 * 1024
OCI_INDEX_RESPONSE_LIMIT = 1024 * 1024
OCI_ISSUED_AT_LIMIT = 128
OCI_TOKEN68_BASE = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~+/"
)

PYTHON_TUPLE = {
    "implementation": "CPython",
    "version": "3.12.10",
    "operating_system": "Linux",
    "architecture": "x86_64",
    "abi": "cp312",
}
RELEASE = {
    "tag": "v1.11.1",
    "commit": "a7ed3e4cbb19731f072d0d90b6d52f7d822569ee",
}

SANITIZED_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
SUBPROCESS_ENV_BASE = {
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": SANITIZED_PATH,
    "PYTHONIOENCODING": "utf-8",
}


class CC002Error(RuntimeError):
    """Fail-closed CC-002 operational refusal."""


@dataclass(frozen=True)
class SelectedArtifact:
    """One immutable published artifact selected by OD-012 or CC-002 acquisition."""

    filename: str
    kind: str
    url: str
    byte_length: int
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "filename": self.filename,
            "kind": self.kind,
            "url": self.url,
            "byte_length": self.byte_length,
            "sha256": self.sha256,
        }


SELECTED_ARTIFACTS = (
    SelectedArtifact(
        filename="linkml-1.11.1-py3-none-any.whl",
        kind="WHEEL",
        url="https://files.pythonhosted.org/packages/1f/fb/3068f649cc436be915f51b2f5ac0656c83dc9bcc6d4f8940633e295042c0/linkml-1.11.1-py3-none-any.whl",
        byte_length=483751,
        sha256="d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed",
    ),
    SelectedArtifact(
        filename="linkml_runtime-1.11.1-py3-none-any.whl",
        kind="WHEEL",
        url="https://files.pythonhosted.org/packages/63/1d/600b0dd24aa61f03d35293a2e9a4695add1e94c03d8701436fb52d5daf4f/linkml_runtime-1.11.1-py3-none-any.whl",
        byte_length=654566,
        sha256="b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da",
    ),
    SelectedArtifact(
        filename="linkml-1.11.1.tar.gz",
        kind="SDIST",
        url="https://files.pythonhosted.org/packages/b4/26/38e7340959cd4a87bfe5403cfcf5311d9fe2ff4382fa00e96008a1342760/linkml-1.11.1.tar.gz",
        byte_length=374853,
        sha256="2f6774e13628270cadaeecda3313db0437ecc15cd44ee35c6c2655dbe31c8524",
    ),
    SelectedArtifact(
        filename="linkml_runtime-1.11.1.tar.gz",
        kind="SDIST",
        url="https://files.pythonhosted.org/packages/d0/7c/36332b49226f37d05d0dbfa4fb1c8017963d62ae722102c9c11c1f530696/linkml_runtime-1.11.1.tar.gz",
        byte_length=556549,
        sha256="e71300b596c4f35aeccd9dca096806678402213dbdb2c5e8e68f507e21320754",
    ),
    SelectedArtifact(
        filename="pip-25.0.1-py3-none-any.whl",
        kind="WHEEL",
        url="https://files.pythonhosted.org/packages/c9/bc/b7db44f5f39f9d0494071bddae6880eb645970366d0a200022a1a93d57f5/pip-25.0.1-py3-none-any.whl",
        byte_length=1841526,
        sha256="c46efd13b6aa8279f33f2864459c8ce587ea6a1a59ee20de055868d8f7688f7f",
    ),
)
ROOT_WHEEL_FILENAMES = (
    "linkml-1.11.1-py3-none-any.whl",
    "linkml_runtime-1.11.1-py3-none-any.whl",
)
CFGRAPH_WHEEL_FILENAME = "cfgraph-0.2.1-py3-none-any.whl"
CFGRAPH_WHEEL_BYTE_LENGTH = 2256
CFGRAPH_WHEEL_SHA256 = (
    "28a5bc1292af3c7de137c500da2f9607d66ed27fe787f15ce33e5698fa828f13"
)
CFGRAPH_WHEEL_BYTES = base64.b64decode(
    b"UEsDBBQAAAAIANF6dE1h/LUJUQMAAEAKAAATAAAAQ0ZHcmFwaC9fX2luaXRfXy5weZVWTW/bMAy9+1dw3aF24QXrjgYyYP3EhqHduvYUGIEby606xfIkZVv+/UhK/kictpkPiS2Tj++RFOXK6CW4dSPrB5DLRhsHV8VSlLerRokU7mqp6xTC03Xj8LFQKVyKWpjCaRNFFSGYslLyvkW4NEXziM43n29ElcJX6dAYvU6udIkwN2cXQ6/JQislFgTdApx2KxuG4u9CMAXbGiK/XyvkYu25MchmaI1Bl50mDBxF31fCrG+NRDEw9aJmraaZZ5v3KnetUDpmnZ5gkOdR9OPu5AtieoNWOOvNo28352f0jlejazb0hBaqsJby4UnFfeqTLAK8bAYB+UrXgpeaDAJgt6QzuO6NWtjTC65DzL8B7+DgYJBcuFCFc6Km4rNVxEa9gYXCCDDCrUwtSigsKGmdBV2BY8a2RfWepahgPpe1dPN5bIXCHBwV5sHi39HPP3SXwLuPTNPzYY1oN0EnK0sqy0WhrOhfrhph4mTSoW7j9YEDIx+3A2ivhpSaOtsu5qAnUs51nu9wNqIceFL+8+nh4dhQ3z8N7LAoZMaaux0z68qdciL8b55FHdhb+KSU/gMFOGoF0AZvKfGc90cjBGAHLm3nIKtWHkjLcORDpOHNFA4P6QmZ+Ydsg3TrN4U43KbsmJJDMoxQa7dRqk0cZ9bZKBtblb01KzGyqZAb1rPBgCDrrt5tMQOpZAweaGlShSmd1FLtNmozxAowREzWlTTW8SiaGGHdM/gDd2lRhyvqhYh12NmvOAVHTsLvQq3YcRCb6rQHBF2UJEHc+60ZtpfeE4GutRSqjH2yRfKqm8B9uB84A0NA1i8j74e6L6JQXNnptE8sFHXJpQ6tM3uf81L7+CF/ObxFuNC5tOfmRmsX25dFUZmb/VU1yClFj9lxPlJXSZwc6vXNtDkmx1mllnH/t6M8PddPVLu6f8JuCyOV54JcFE6MRqGfY5qtt+ffVpu3+52pkaQQZN6h29gDbTGkQrcmG2OOqt9Te0aVHRxQg7KyLjwU/H6mOd2R958HdCKkfODmg74ZTTvbWKwJAcfPiaqTZFuPEriNGzwTcYQdj5n7c7c/5vtg1KGNxS6Kdtjja+5H7K52NtKI4x4ZNzb1YtKfPf4Ta/u7KtsVh3n9A1BLAwQUAAAACADVef9cmU2Nb2MBAADXAgAAIAAAAGNmZ3JhcGgtMC4yLjEuZGlzdC1pbmZvL01FVEFEQVRBlVLLTsMwELz7K/wDSUupQLIEorRAkQpUBHHfOJtkJT+C7RT173HaplG49ZLH7Mw+ZvcNAxQQIPlG58kawWfpnL2DRsGXzy8OmpqdQ9N0ll6xrNUa3F5wV5SKci6tUihDZHheKggBDZmKVwft2mpMGqhiujqERkwmFYW6zVNp9aT2VuWOqklfadGG2jrB1+CsKnh2DJ/gBDWQEvwkeji9EzKldRoCSd9lZRuSaHwsuGhA1hgHmrKlAu+pJIzJV7hDZRuNJvAsQGg9F4LPecIfoxkj6pPZkbPmQI2cZRzRKhxRXk2ct8CCL9qC0EjsiKcS0bcR98s2JLt4ZsvwCw5HvUR8Q7kDRziWbZ2NZmrduboBU7XRzo693UdbTPd13T0+jNpfqktvLlbcsk/8acmhT1bkQ38G93fTdJ7O2GpvQJMUHA5L+/9/XOKAynP1Aav7mxkgddzpALi+hyL2MMD+eJvsD1BLAwQUAAAACADmef9cmZh/nVsAAABbAAAAHQAAAGNmZ3JhcGgtMC4yLjEuZGlzdC1pbmZvL1dIRUVMBcExCsMwDAXQXafQ2A4yLlmKL1C6hRDa2YVPEjBSkOUht+973x1o8oH3w7TwI2V6QeE1zAt3xDjDrHW+PaeUU77TYhby7jIPRzt+hcMHaK1b4fOaRE0hVS+iP1BLAwQUAAAACADVef9c2CM+7goAAAAIAAAAJQAAAGNmZ3JhcGgtMC4yLjEuZGlzdC1pbmZvL3RvcF9sZXZlbC50eHRzdnMvSizI4AIAUEsDBBQAAAAIAOZ5/1x6St3C/wAAAHQBAAAeAAAAY2ZncmFwaC0wLjIuMS5kaXN0LWluZm8vUkVDT1JEdcy9coIwAADg3WcJiPEHGBwgCamAegqKsOQsitASoBAJ+vRtB0fn7+5DDm3PTT5mrKgKwZjaPECXn+F8sYQw55bntL70KcWfUV89A32OLveUFr5WDi5BfECcGt4OwAWcjdLs9n8pmgrViXopOqEUVVaP1yS0sBVar/gkHGOj8zSbOn0i6z+W5MAhM2+JidqgoVrL3e6BdvIb6FB/+0YfhPiv1IMLjcTP6nnq3Nje0R++Mo7hQC5FEm96nMjITO3cVNjaAubk7SnqhpXX/lqqYhCvm27jTJrM6+cyLf3DcR3YK/Il7ji64ekZo7umBJ2eNU06A8bbek/Qdo8BGP0CUEsBAhQDFAAAAAgA0Xp0TWH8tQlRAwAAQAoAABMAAAAAAAAAAAAAAKSBAAAAAENGR3JhcGgvX19pbml0X18ucHlQSwECFAMUAAAACADVef9cmU2Nb2MBAADXAgAAIAAAAAAAAAAAAAAApIGCAwAAY2ZncmFwaC0wLjIuMS5kaXN0LWluZm8vTUVUQURBVEFQSwECFAMUAAAACADmef9cmZh/nVsAAABbAAAAHQAAAAAAAAAAAAAApIEjBQAAY2ZncmFwaC0wLjIuMS5kaXN0LWluZm8vV0hFRUxQSwECFAMUAAAACADVef9c2CM+7goAAAAIAAAAJQAAAAAAAAAAAAAApIG5BQAAY2ZncmFwaC0wLjIuMS5kaXN0LWluZm8vdG9wX2xldmVsLnR4dFBLAQIUAxQAAAAIAOZ5/1x6St3C/wAAAHQBAAAeAAAAAAAAAAAAAAC0gQYGAABjZmdyYXBoLTAuMi4xLmRpc3QtaW5mby9SRUNPUkRQSwUGAAAAAAUABQB5AQAAQQcAAAAA",
    validate=True,
)
EMBEDDED_ROOT_ARTIFACTS = {CFGRAPH_WHEEL_FILENAME: CFGRAPH_WHEEL_BYTES}
PIP_WHEEL_FILENAME = "pip-25.0.1-py3-none-any.whl"
ANTLR_SDIST_FILENAME = "antlr4-python3-runtime-4.9.3.tar.gz"
SETUPTOOLS_WHEEL_FILENAME = "setuptools-83.0.0-py3-none-any.whl"
SOURCE_DATE_EPOCH = "315532800"
ANTLR_SDIST_MEMBER_COUNT = 78
ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH = 477312
BUILD_ARTIFACTS = (
    SelectedArtifact(
        filename=ANTLR_SDIST_FILENAME,
        kind="SDIST",
        url="https://files.pythonhosted.org/packages/3e/38/7859ff46355f76f8d19459005ca000b6e7012f2f1ca597746cbcd1fbfe5e/antlr4-python3-runtime-4.9.3.tar.gz",
        byte_length=117034,
        sha256="f224469b4168294902bb1efa80a8bf7855f24c99aef99cbefc1bcd3cce77881b",
    ),
    SelectedArtifact(
        filename=SETUPTOOLS_WHEEL_FILENAME,
        kind="WHEEL",
        url="https://files.pythonhosted.org/packages/5d/40/e1e72872c6354b306daef1703549e8e83b4d43cfea356311bf722a043752/setuptools-83.0.0-py3-none-any.whl",
        byte_length=1008090,
        sha256="29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3",
    ),
)
PREFIXCOMMONS_INPUT_FILENAME = "prefixcommons-0.1.12-py3-none-any.whl"
PREFIXCOMMONS_DERIVED_FILENAME = "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
PREFIXCOMMONS_MEMBER_COUNT = 14
PREFIXCOMMONS_UNCOMPRESSED_BYTE_LENGTH = 109044
PREFIXCOMMONS_DERIVED_UNCOMPRESSED_BYTE_LENGTH = 109064
PREFIXCOMMONS_PACKAGE_MEMBER_COUNT = 10
PREFIXCOMMONS_METADATA_BYTE_LENGTH = 1960
PREFIXCOMMONS_METADATA_SHA256 = (
    "4c6cf90de54fa4ce46d1235551f75c021bacab34b8c9894fd50a8096441a5303"
)
PREFIXCOMMONS_WHEEL_BYTE_LENGTH = 83
PREFIXCOMMONS_WHEEL_SHA256 = (
    "cb778389a15548d4cf6e0cdf367d27627e6d127d5c5fa5ab75eb43950338c56c"
)
PREFIXCOMMONS_LICENSE_BYTE_LENGTH = 1500
PREFIXCOMMONS_LICENSE_SHA256 = (
    "3a9b5b0d46996cdfd82b65429e189904e4ab1908014ce408cbecde9f591f37b4"
)
PREFIXCOMMONS_PACKAGE_MEMBERS = frozenset(
    {
        "prefixcommons/__init__.py",
        "prefixcommons/curie_transformer.py",
        "prefixcommons/curie_util.py",
        "prefixcommons/registry/go_context.jsonld",
        "prefixcommons/registry/go_obo_context.jsonld",
        "prefixcommons/registry/idot_context.jsonld",
        "prefixcommons/registry/monarch_context.jsonld",
        "prefixcommons/registry/obo_context.jsonld",
        "prefixcommons/registry/semweb_context.jsonld",
        "prefixcommons/version.py",
    }
)
DERIVATIVE_INPUTS = (
    SelectedArtifact(
        filename=PREFIXCOMMONS_INPUT_FILENAME,
        kind="WHEEL",
        url="https://files.pythonhosted.org/packages/31/e8/715b09df3dab02b07809d812042dc47a46236b5603d9d3a2572dbd1d8a97/prefixcommons-0.1.12-py3-none-any.whl",
        byte_length=29482,
        sha256="16dbc0a1f775e003c724f19a694fcfa3174608f5c8b0e893d494cf8098ac7f8b",
    ),
)
DERIVATION_INPUT_ROOT = Path("/derivative-inputs")
DERIVATION_OUTPUT_ROOT = Path("/output")
EXPECTED_DERIVATION_CHILD_FACTS = {
    "python": PYTHON_TUPLE,
    "image": {
        "platform": OCI_PLATFORM,
        "child_digest": OCI_CHILD_DIGEST,
    },
    "tool": {
        "implementation": "python-stdlib",
        "generator": "malleus-cc002 (wheel-derivation-v1)",
        "adapter_sha256": "sha256:"
        + hashlib.sha256(ADAPTER_PATH.read_bytes()).hexdigest(),
    },
    "environment": {
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "tz": "UTC",
        "python_hash_seed": "0",
        "umask": "022",
    },
    "isolation": {
        "network": "NONE",
        "read_only_root": True,
        "nonroot": True,
    },
}
RETAINED_DERIVATION_RUN = json.loads(
    json.dumps(EXPECTED_DERIVATION_CHILD_FACTS, sort_keys=True)
)
DERIVATION_PROGRAM = """\
from contract_compiler_environment import _derivation_main

raise SystemExit(_derivation_main())
"""
PIP_IMPORT_ORIGIN = f"/roots/{PIP_WHEEL_FILENAME}/pip/__init__.py"
PROXY_REQUEST_LIMIT = 8192
RESOLVER_PIP_ARGUMENTS = (
    "--isolated",
    "--proxy",
    "{proxy}",
    "download",
    "--no-cache-dir",
    "--index-url",
    "https://pypi.org/simple",
    "--dest",
    "/wheelhouse",
    "--only-binary=:all:",
    "--find-links=/built",
    f"/roots/{ROOT_WHEEL_FILENAMES[0]}",
    f"/roots/{ROOT_WHEEL_FILENAMES[1]}",
    f"/built/{PREFIXCOMMONS_DERIVED_FILENAME}",
    f"/roots/{CFGRAPH_WHEEL_FILENAME}",
)
RESOLVER_PROGRAM = (
    "from contract_compiler_environment import _resolver_main; "
    "raise SystemExit(_resolver_main())"
)
RESOLVER_PIP_PROGRAM = (
    "import runpy; namespace = "
    "runpy.run_path('/adapter/contract_compiler_environment.py'); "
    "raise SystemExit(namespace['_pinned_pip_main']())"
)


def _fail(code: str, message: str) -> None:
    raise CC002Error(f"[{code}] {message}")


def require_repository_cwd() -> None:
    """Refuse execution outside the trusted project selected by MCP ``cwd``."""
    if Path.cwd().resolve() != REPOSITORY:
        _fail(
            "CC002_CWD",
            f"working directory must be the active repository: {REPOSITORY}",
        )


def canonical_json(value: Any) -> str:
    """Return compact deterministic JSON without a transport newline."""
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, UnicodeError) as error:
        _fail("CC002_JSON", f"value is not canonical JSON: {error}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail("CC002_JSON_DUPLICATE", f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def _nonfinite(value: str) -> None:
    _fail("CC002_JSON_NONFINITE", f"nonfinite JSON number '{value}' is forbidden")


def strict_json(source: str | bytes, context: str) -> Any:
    """Decode JSON with duplicate-key and nonfinite-number refusal."""
    try:
        if isinstance(source, bytes):
            source = source.decode("utf-8")
        return json.loads(
            source,
            object_pairs_hook=_unique_object,
            parse_constant=_nonfinite,
        )
    except CC002Error:
        raise
    except (UnicodeError, json.JSONDecodeError) as error:
        _fail("CC002_JSON", f"{context}: invalid JSON: {error}")


def _exact_keys(value: Any, expected: set[str], context: str) -> None:
    if not isinstance(value, Mapping):
        _fail("CC002_OBJECT", f"{context} must be an object")
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        _fail("CC002_REQUIRED", f"{context}: missing fields {missing}")
    if unknown:
        _fail("CC002_UNKNOWN", f"{context}: unknown fields {unknown}")


def _digest(source: bytes) -> str:
    return "sha256:" + hashlib.sha256(source).hexdigest()


def _artifact_record(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        _fail("CC002_SYMLINK", f"symlink artifact is forbidden: {path}")
    if not path.is_file():
        _fail("CC002_FILE", f"required regular file is missing: {path}")
    source = path.read_bytes()
    return {
        "filename": path.name,
        "byte_length": len(source),
        "sha256": _digest(source),
    }


def _output_schema(required: Sequence[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": list(required),
        "additionalProperties": False,
    }


_DIGEST_SCHEMA = {"type": "string", "minLength": 71, "maxLength": 71}
_ACQUIRE_PROPERTIES = {
    "schema": {"const": "malleus.cc002.acquire-result/v4"},
    "state": {"const": "MATERIALIZED"},
    "destination": {"const": DESTINATION_LABEL},
    "artifact_count": {"type": "integer", "minimum": 9, "maximum": 9},
    "built_artifact_count": {"type": "integer", "minimum": 2, "maximum": 2},
    "source_build_record_sha256": _DIGEST_SCHEMA,
    "derivation_record_sha256": _DIGEST_SCHEMA,
    "wheel_count": {"type": "integer", "minimum": 1},
    "lock_sha256": _DIGEST_SCHEMA,
    "wheelhouse_sha256": _DIGEST_SCHEMA,
    "oci_index_digest": {"const": OCI_INDEX_DIGEST},
    "oci_child_digest": {"const": OCI_CHILD_DIGEST},
}
_VERIFY_PROPERTIES = {
    "schema": {"const": "malleus.cc002.verify-result/v4"},
    "state": {"const": "VERIFIED_OFFLINE"},
    "destination": {"const": DESTINATION_LABEL},
    "environment_manifest_sha256": _DIGEST_SCHEMA,
    "verification_sha256": _DIGEST_SCHEMA,
    "generator_output_sha256": _DIGEST_SCHEMA,
    "installed_distribution_count": {"type": "integer", "minimum": 1},
    "lock_sha256": _DIGEST_SCHEMA,
    "wheelhouse_sha256": _DIGEST_SCHEMA,
    "source_build_record_sha256": _DIGEST_SCHEMA,
    "derivation_record_sha256": _DIGEST_SCHEMA,
    "oci_index_digest": {"const": OCI_INDEX_DIGEST},
    "oci_child_digest": {"const": OCI_CHILD_DIGEST},
}
_EMPTY_INPUT = {"type": "object", "properties": {}, "additionalProperties": False}

TOOLS = (
    {
        "name": "cc002_acquire",
        "title": "Acquire sealed CC-002 compiler environment",
        "description": (
            "Acquire the fixed OD-012 artifacts, resolve the exact cp312 wheel "
            "closure, and atomically publish the retained environment."
        ),
        "inputSchema": _EMPTY_INPUT,
        "outputSchema": _output_schema(tuple(_ACQUIRE_PROPERTIES), _ACQUIRE_PROPERTIES),
        "annotations": {
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    },
    {
        "name": "cc002_verify_offline",
        "title": "Verify sealed CC-002 environment offline",
        "description": (
            "Verify retained bytes and prove a fresh network-denied install plus "
            "the generic malleus.yaml JSON Schema generator smoke."
        ),
        "inputSchema": _EMPTY_INPUT,
        "outputSchema": _output_schema(tuple(_VERIFY_PROPERTIES), _VERIFY_PROPERTIES),
        "annotations": {
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    },
)


def _validate_digest(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        _fail("CC002_DIGEST", f"{context} must start with 'sha256:'")
    hexadecimal = value.removeprefix("sha256:")
    if len(hexadecimal) != 64 or any(
        character not in "0123456789abcdef" for character in hexadecimal
    ):
        _fail("CC002_DIGEST", f"{context} must contain 64 lowercase hexadecimal digits")
    return value


def acquire_result(
    *,
    artifact_count: int,
    built_artifact_count: int,
    source_build_record_sha256: str,
    derivation_record_sha256: str,
    lock_sha256: str,
    wheel_count: int,
    wheelhouse_sha256: str,
) -> dict[str, Any]:
    _validate_digest(lock_sha256, "lock_sha256")
    _validate_digest(wheelhouse_sha256, "wheelhouse_sha256")
    _validate_digest(source_build_record_sha256, "source_build_record_sha256")
    _validate_digest(derivation_record_sha256, "derivation_record_sha256")
    if (
        not isinstance(artifact_count, int)
        or isinstance(artifact_count, bool)
        or artifact_count != 9
    ):
        _fail("CC002_RESULT", "artifact_count must be exactly nine")
    if (
        not isinstance(wheel_count, int)
        or isinstance(wheel_count, bool)
        or wheel_count < 1
    ):
        _fail("CC002_RESULT", "wheel_count must be a positive integer")
    if built_artifact_count != 2 or isinstance(built_artifact_count, bool):
        _fail("CC002_RESULT", "built_artifact_count must be exactly two")
    return {
        "schema": "malleus.cc002.acquire-result/v4",
        "state": "MATERIALIZED",
        "destination": DESTINATION_LABEL,
        "artifact_count": artifact_count,
        "built_artifact_count": built_artifact_count,
        "source_build_record_sha256": source_build_record_sha256,
        "derivation_record_sha256": derivation_record_sha256,
        "wheel_count": wheel_count,
        "lock_sha256": lock_sha256,
        "wheelhouse_sha256": wheelhouse_sha256,
        "oci_index_digest": OCI_INDEX_DIGEST,
        "oci_child_digest": OCI_CHILD_DIGEST,
    }


def verify_result(
    *,
    environment_manifest_sha256: str,
    verification_sha256: str,
    generator_output_sha256: str,
    installed_distribution_count: int,
    lock_sha256: str,
    wheelhouse_sha256: str,
    source_build_record_sha256: str,
    derivation_record_sha256: str,
) -> dict[str, Any]:
    for name, value in (
        ("environment_manifest_sha256", environment_manifest_sha256),
        ("verification_sha256", verification_sha256),
        ("generator_output_sha256", generator_output_sha256),
        ("lock_sha256", lock_sha256),
        ("wheelhouse_sha256", wheelhouse_sha256),
        ("source_build_record_sha256", source_build_record_sha256),
        ("derivation_record_sha256", derivation_record_sha256),
    ):
        _validate_digest(value, name)
    if (
        not isinstance(installed_distribution_count, int)
        or isinstance(installed_distribution_count, bool)
        or installed_distribution_count < 1
    ):
        _fail("CC002_RESULT", "installed_distribution_count must be positive")
    return {
        "schema": "malleus.cc002.verify-result/v4",
        "state": "VERIFIED_OFFLINE",
        "destination": DESTINATION_LABEL,
        "environment_manifest_sha256": environment_manifest_sha256,
        "verification_sha256": verification_sha256,
        "generator_output_sha256": generator_output_sha256,
        "installed_distribution_count": installed_distribution_count,
        "lock_sha256": lock_sha256,
        "wheelhouse_sha256": wheelhouse_sha256,
        "source_build_record_sha256": source_build_record_sha256,
        "derivation_record_sha256": derivation_record_sha256,
        "oci_index_digest": OCI_INDEX_DIGEST,
        "oci_child_digest": OCI_CHILD_DIGEST,
    }


@dataclass(frozen=True)
class ToolServices:
    acquire: Callable[[], dict[str, Any]]
    verify: Callable[[], dict[str, Any]]


DEFAULT_SERVICES = ToolServices(
    acquire=lambda: acquire_environment(),
    verify=lambda: verify_environment(),
)


def _response(request_id: int | str, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: int | str | None, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def _valid_id(value: Any) -> bool:
    return (isinstance(value, (int, str)) and not isinstance(value, bool))


def _validate_params(params: Any, context: str) -> dict[str, Any]:
    if not isinstance(params, dict):
        _fail("CC002_PARAMS", f"{context}: params must be an object")
    return params


def _validate_request_meta(params: Mapping[str, Any], context: str) -> None:
    if "_meta" in params and not isinstance(params["_meta"], dict):
        _fail("CC002_PARAMS", f"{context} _meta must be an object")


def _validate_tool_output(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("CC002_RESULT", f"{name} result must be an object")
    properties = _ACQUIRE_PROPERTIES if name == "cc002_acquire" else _VERIFY_PROPERTIES
    if set(value) != set(properties):
        missing = sorted(set(properties) - set(value))
        unknown = sorted(set(value) - set(properties))
        _fail(
            "CC002_RESULT",
            f"{name} result fields mismatch; missing={missing}, unknown={unknown}",
        )
    expected_schema = (
        "malleus.cc002.acquire-result/v4"
        if name == "cc002_acquire"
        else "malleus.cc002.verify-result/v4"
    )
    expected_state = "MATERIALIZED" if name == "cc002_acquire" else "VERIFIED_OFFLINE"
    if value["schema"] != expected_schema or value["state"] != expected_state:
        _fail("CC002_RESULT", f"{name} result schema or state is invalid")
    if value["destination"] != DESTINATION_LABEL:
        _fail("CC002_RESULT", f"{name} result destination is invalid")
    if value["oci_index_digest"] != OCI_INDEX_DIGEST:
        _fail("CC002_RESULT", f"{name} result OCI index identity is invalid")
    if value["oci_child_digest"] != OCI_CHILD_DIGEST:
        _fail("CC002_RESULT", f"{name} result OCI child identity is invalid")
    for field in value:
        if field.endswith("sha256"):
            _validate_digest(value[field], field)
    count_fields = (
        ("artifact_count", "built_artifact_count", "wheel_count")
        if name == "cc002_acquire"
        else ("installed_distribution_count",)
    )
    for field in count_fields:
        if (
            not isinstance(value[field], int)
            or isinstance(value[field], bool)
            or value[field] < 1
        ):
            _fail("CC002_RESULT", f"{field} must be a positive integer")
    if name == "cc002_acquire" and value["artifact_count"] != 9:
        _fail("CC002_RESULT", "artifact_count must be exactly nine")
    if name == "cc002_acquire" and value["built_artifact_count"] != 2:
        _fail("CC002_RESULT", "built_artifact_count must be exactly two")
    return value


def _tool_result(name: str, value: dict[str, Any]) -> dict[str, Any]:
    value = _validate_tool_output(name, value)
    return {
        "content": [{"type": "text", "text": canonical_json(value)}],
        "structuredContent": value,
        "isError": False,
    }


def handle_message(message: Any, services: Any = DEFAULT_SERVICES) -> dict[str, Any] | None:
    """Handle one already-decoded JSON-RPC message."""
    notification_candidate = isinstance(message, dict) and "id" not in message
    if not isinstance(message, dict):
        return _error(None, -32600, "Invalid Request")
    allowed = {"jsonrpc", "id", "method", "params"}
    if set(message) - allowed:
        if notification_candidate:
            return None
        return _error(message.get("id") if _valid_id(message.get("id")) else None, -32600, "Invalid Request")
    if message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
        if notification_candidate:
            return None
        return _error(None, -32600, "Invalid Request")
    notification = "id" not in message
    if not notification and not _valid_id(message["id"]):
        return _error(None, -32600, "Invalid Request")
    request_id = None if notification else message["id"]
    method = message["method"]
    params = message.get("params", {})
    try:
        params = _validate_params(params, method)
        if method == "notifications/initialized":
            if not notification or params:
                _fail("CC002_PARAMS", "notifications/initialized requires empty params")
            return None
        if notification:
            return None
        if method == "initialize":
            _exact_keys(params, {"protocolVersion", "capabilities", "clientInfo"}, method)
            version = params["protocolVersion"]
            if not isinstance(version, str):
                _fail("CC002_PROTOCOL", "protocolVersion must be a string")
            negotiated_version = (
                version
                if version in SUPPORTED_PROTOCOL_VERSIONS
                else SUPPORTED_PROTOCOL_VERSIONS[0]
            )
            if not isinstance(params["capabilities"], dict):
                _fail("CC002_PROTOCOL", "capabilities must be an object")
            client = params["clientInfo"]
            if not isinstance(client, dict):
                _fail("CC002_PROTOCOL", "clientInfo must be an object")
            if not {"name", "version"}.issubset(client) or set(client) - {
                "name",
                "version",
                "title",
            }:
                _fail("CC002_PROTOCOL", "clientInfo fields are invalid")
            if not all(
                isinstance(client[field], str) and client[field]
                for field in {"name", "version"}
            ):
                _fail("CC002_PROTOCOL", "clientInfo name and version must be nonempty strings")
            if "title" in client and (
                not isinstance(client["title"], str) or not client["title"]
            ):
                _fail("CC002_PROTOCOL", "clientInfo title must be a nonempty string")
            return _response(
                request_id,
                {
                    "protocolVersion": negotiated_version,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                },
            )
        if method == "ping":
            if set(params) - {"_meta"}:
                _fail("CC002_PARAMS", "ping accepts only the MCP _meta extension")
            _validate_request_meta(params, method)
            return _response(request_id, {})
        if method == "tools/list":
            if set(params) - {"_meta", "cursor"}:
                _fail(
                    "CC002_PARAMS",
                    "tools/list accepts only cursor and the MCP _meta extension",
                )
            _validate_request_meta(params, method)
            if "cursor" in params:
                _fail("CC002_CURSOR", "tools/list cursor is invalid")
            return _response(request_id, {"tools": list(TOOLS)})
        if method == "tools/call":
            if "name" not in params or set(params) - {"name", "arguments", "_meta"}:
                _fail("CC002_PARAMS", "tools/call requires name and optional arguments")
            _validate_request_meta(params, method)
            name = params["name"]
            arguments = params["arguments"] if "arguments" in params else {}
            if not isinstance(name, str) or name not in {
                "cc002_acquire",
                "cc002_verify_offline",
            }:
                _fail("CC002_TOOL", f"unknown tool: {name!r}")
            if not isinstance(arguments, dict) or arguments:
                _fail("CC002_ARGUMENTS", f"{name} requires exactly an empty object")
            try:
                value = services.acquire() if name == "cc002_acquire" else services.verify()
            except CC002Error as error:
                return _response(
                    request_id,
                    {"content": [{"type": "text", "text": str(error)}], "isError": True},
                )
            except Exception:
                return _response(
                    request_id,
                    {
                        "content": [
                            {
                                "type": "text",
                                "text": "[CC002_INTERNAL] tool execution failed",
                            }
                        ],
                        "isError": True,
                    },
                )
            try:
                result = _tool_result(name, value)
            except CC002Error as error:
                result = {
                    "content": [{"type": "text", "text": str(error)}],
                    "isError": True,
                }
            return _response(request_id, result)
        return _error(request_id, -32601, "Method not found")
    except CC002Error as error:
        if notification:
            return None
        return _error(request_id, -32602, str(error))


def process_line(source: str, services: Any = DEFAULT_SERVICES) -> dict[str, Any] | None:
    try:
        message = strict_json(source, "MCP input")
    except CC002Error:
        return _error(None, -32700, "Parse error")
    return handle_message(message, services)


def serve(
    stdin: TextIO = sys.stdin,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
    services: Any = DEFAULT_SERVICES,
) -> None:
    """Serve newline-delimited MCP JSON-RPC without non-protocol stdout."""
    del stderr
    for line in stdin:
        response = process_line(line, services)
        if response is not None:
            stdout.write(canonical_json(response) + "\n")
            stdout.flush()


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        del req, fp, code, msg, headers, newurl
        return None


def _default_opener():
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())


def _validate_fixed_oci_endpoint(
    url: str,
    hosts: frozenset[str],
    path: str,
    query: str,
) -> None:
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError:
        _fail("CC002_OCI_URL", "fixed OCI endpoint is invalid")
    if len(hosts) != 1:
        _fail("CC002_OCI_URL", "fixed OCI host boundary is invalid")
    expected_host = next(iter(hosts))
    expected_url = urllib.parse.urlunsplit(("https", expected_host, path, query, ""))
    if (
        url != expected_url
        or parsed.scheme != "https"
        or parsed.hostname not in hosts
        or parsed.netloc != expected_host
        or parsed.path != path
        or parsed.query != query
        or parsed.fragment
    ):
        _fail("CC002_OCI_URL", "fixed OCI endpoint is invalid")


def _single_http_header(headers: Any, name: str, context: str) -> str | None:
    get_all = getattr(headers, "get_all", None)
    if callable(get_all):
        values = get_all(name) or []
    else:
        value = headers.get(name)
        values = [] if value is None else [value]
    if len(values) > 1 or any(not isinstance(value, str) for value in values):
        _fail("CC002_OCI_HTTP", f"{context}: invalid {name} header")
    return values[0] if values else None


def _read_fixed_https(
    opener: Any,
    request: urllib.request.Request,
    expected_url: str,
    byte_limit: int,
    context: str,
) -> bytes:
    if request.full_url != expected_url or request.get_method() != "GET":
        _fail("CC002_OCI_URL", f"{context}: fixed request identity changed")
    try:
        with opener.open(request, timeout=NETWORK_TIMEOUT_SECONDS) as response:
            if response.status != 200:
                _fail("CC002_OCI_HTTP", f"{context}: unexpected HTTP status")
            if response.geturl() != expected_url:
                _fail("CC002_OCI_URL", f"{context}: redirect is forbidden")
            encoding = _single_http_header(response.headers, "Content-Encoding", context)
            if encoding not in {None, "identity"}:
                _fail("CC002_OCI_HTTP", f"{context}: encoded response is forbidden")
            length_header = _single_http_header(
                response.headers, "Content-Length", context
            )
            declared_length = None
            if length_header is not None:
                if not length_header or any(
                    character < "0" or character > "9" for character in length_header
                ):
                    _fail("CC002_OCI_SIZE", f"{context}: invalid Content-Length")
                if len(length_header) > len(str(byte_limit)):
                    _fail("CC002_OCI_SIZE", f"{context}: response exceeds byte limit")
                declared_length = int(length_header)
                if declared_length > byte_limit:
                    _fail("CC002_OCI_SIZE", f"{context}: response exceeds byte limit")
            source = bytearray()
            while True:
                chunk = response.read(
                    min(DOWNLOAD_CHUNK_SIZE, byte_limit + 1 - len(source))
                )
                if not chunk:
                    break
                if not isinstance(chunk, bytes):
                    _fail("CC002_OCI_HTTP", f"{context}: response body is not bytes")
                source.extend(chunk)
                if len(source) > byte_limit:
                    _fail("CC002_OCI_SIZE", f"{context}: response exceeds byte limit")
            if declared_length is not None and declared_length != len(source):
                _fail("CC002_OCI_SIZE", f"{context}: Content-Length mismatch")
            return bytes(source)
    except CC002Error:
        raise
    except Exception:
        _fail("CC002_OCI_HTTP", f"{context}: fixed HTTPS request failed")


def _parse_docker_hub_token(source: bytes) -> str:
    try:
        value = strict_json(source, "Docker Hub token response")
    except Exception:
        _fail("CC002_OCI_AUTH", "Docker Hub token response is invalid")
    allowed = {"token", "access_token", "expires_in", "issued_at"}
    if not isinstance(value, dict) or not set(value).issubset(allowed):
        _fail("CC002_OCI_AUTH", "Docker Hub token response is invalid")
    tokens = [value[name] for name in ("token", "access_token") if name in value]
    if (
        not tokens
        or any(not isinstance(token, str) for token in tokens)
        or len(tokens) == 2
        and tokens[0] != tokens[1]
    ):
        _fail("CC002_OCI_AUTH", "Docker Hub token response is invalid")
    token = tokens[0]
    unpadded = token.rstrip("=")
    if (
        not token
        or len(token) > OCI_AUTH_RESPONSE_LIMIT
        or not unpadded
        or any(character not in OCI_TOKEN68_BASE for character in unpadded)
    ):
        _fail("CC002_OCI_AUTH", "Docker Hub token response is invalid")
    expires_in = value.get("expires_in")
    if "expires_in" in value and (
        not isinstance(expires_in, int)
        or isinstance(expires_in, bool)
        or expires_in <= 0
    ):
        _fail("CC002_OCI_AUTH", "Docker Hub token response is invalid")
    issued_at = value.get("issued_at")
    if "issued_at" in value and (
        not isinstance(issued_at, str)
        or not issued_at
        or len(issued_at) > OCI_ISSUED_AT_LIMIT
        or any(character < " " or character > "~" for character in issued_at)
    ):
        _fail("CC002_OCI_AUTH", "Docker Hub token response is invalid")
    return token


def _fetch_selected_oci_index(opener: Any) -> bytes:
    _validate_fixed_oci_endpoint(
        OCI_AUTH_URL,
        OCI_AUTH_HTTPS_HOSTS,
        "/token",
        "service=registry.docker.io&scope=repository:library/python:pull",
    )
    auth_request = urllib.request.Request(
        OCI_AUTH_URL,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "User-Agent": "malleus-cc002/1",
        },
        method="GET",
    )
    token = _parse_docker_hub_token(
        _read_fixed_https(
            opener,
            auth_request,
            OCI_AUTH_URL,
            OCI_AUTH_RESPONSE_LIMIT,
            "Docker Hub authentication",
        )
    )
    _validate_fixed_oci_endpoint(
        OCI_INDEX_URL,
        OCI_REGISTRY_HTTPS_HOSTS,
        OCI_INDEX_PATH,
        "",
    )
    index_request = urllib.request.Request(
        OCI_INDEX_URL,
        headers={
            "Accept": (
                "application/vnd.oci.image.index.v1+json, "
                "application/vnd.docker.distribution.manifest.list.v2+json"
            ),
            "Accept-Encoding": "identity",
            "Authorization": f"Bearer {token}",
            "User-Agent": "malleus-cc002/1",
        },
        method="GET",
    )
    return _read_fixed_https(
        opener,
        index_request,
        OCI_INDEX_URL,
        OCI_INDEX_RESPONSE_LIMIT,
        "OCI index retrieval",
    )


def safe_target(root: Path, relative_name: str) -> Path:
    """Resolve a fixed relative artifact name without traversal or symlink parents."""
    relative = PurePosixPath(relative_name)
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        _fail("CC002_PATH", f"invalid relative filename: {relative_name!r}")
    root = root.resolve()
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            _fail("CC002_SYMLINK", f"symlink parent is forbidden: {current}")
    target = root.joinpath(*relative.parts)
    if target.is_symlink():
        _fail("CC002_SYMLINK", f"symlink target is forbidden: {target}")
    try:
        target.relative_to(root)
    except ValueError:
        _fail("CC002_PATH", f"path escapes fixed root: {target}")
    return target


def _validate_download_url(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https":
        _fail("CC002_URL", f"artifact URL must use https: {url}")
    if parsed.hostname not in ALLOWED_HTTPS_HOSTS:
        _fail("CC002_URL", f"artifact URL host is not allowed: {parsed.hostname!r}")
    if parsed.username is not None or parsed.password is not None or parsed.port is not None:
        _fail("CC002_URL", "artifact URL authority is not allowed")
    if parsed.query or parsed.fragment:
        _fail("CC002_URL", "artifact URL query and fragment are forbidden")


def _existing_matches(path: Path, artifact: SelectedArtifact) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    stat = path.stat()
    if stat.st_size != artifact.byte_length:
        return False
    return hashlib.sha256(path.read_bytes()).hexdigest() == artifact.sha256


def download_artifact(artifact: SelectedArtifact, target: Path, opener: Any = None) -> None:
    """Download one immutable artifact to an atomic same-directory target."""
    _validate_download_url(artifact.url)
    if target.name != artifact.filename:
        _fail("CC002_PATH", f"target filename must be {artifact.filename!r}")
    if target.exists() or target.is_symlink():
        if _existing_matches(target, artifact):
            return
        _fail("CC002_CONFLICT", f"conflicting existing artifact: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target = safe_target(target.parent, target.name)
    partial = safe_target(target.parent, target.name + ".part")
    if partial.exists() or partial.is_symlink():
        _fail("CC002_PARTIAL", f"stale partial artifact is forbidden: {partial}")
    opener = _default_opener() if opener is None else opener
    request = urllib.request.Request(
        artifact.url,
        headers={"Accept-Encoding": "identity", "User-Agent": "malleus-cc002/1"},
        method="GET",
    )
    try:
        with opener.open(request, timeout=NETWORK_TIMEOUT_SECONDS) as response:
            if response.status != 200:
                _fail("CC002_HTTP", f"unexpected HTTP status {response.status}")
            if response.geturl() != artifact.url:
                _fail("CC002_REDIRECT", "artifact redirect is forbidden")
            header = response.headers.get("Content-Length")
            if header is None:
                _fail("CC002_LENGTH", "required Content-Length is missing")
            try:
                declared_length = int(header)
            except ValueError:
                _fail("CC002_LENGTH", f"invalid Content-Length: {header!r}")
            if declared_length != artifact.byte_length:
                _fail(
                    "CC002_LENGTH",
                    f"Content-Length {declared_length} != {artifact.byte_length}",
                )
            digest = hashlib.sha256()
            length = 0
            with partial.open("xb") as stream:
                while True:
                    chunk = response.read(DOWNLOAD_CHUNK_SIZE)
                    if not chunk:
                        break
                    stream.write(chunk)
                    digest.update(chunk)
                    length += len(chunk)
                    if length > artifact.byte_length:
                        _fail(
                            "CC002_LENGTH",
                            f"artifact byte length exceeds {artifact.byte_length}",
                        )
                stream.flush()
                os.fsync(stream.fileno())
            if length != artifact.byte_length:
                _fail("CC002_LENGTH", f"artifact byte length {length} != {artifact.byte_length}")
            if digest.hexdigest() != artifact.sha256:
                _fail("CC002_DIGEST", "artifact SHA-256 does not match selected identity")
            os.replace(partial, target)
    except CC002Error:
        if partial.exists() and not partial.is_symlink():
            partial.unlink()
        raise
    except (OSError, urllib.error.URLError) as error:
        if partial.exists() and not partial.is_symlink():
            partial.unlink()
        _fail("CC002_DOWNLOAD", f"artifact download interrupted: {error}")


def parse_oci_index(
    source: bytes,
    *,
    expected_index_digest: str = OCI_INDEX_DIGEST,
) -> str:
    if _digest(source) != expected_index_digest:
        _fail("CC002_OCI_INDEX", "OCI index digest mismatch")
    value = strict_json(source, "OCI index")
    if not isinstance(value, dict):
        _fail("CC002_OCI_INDEX", "OCI index must be an object")
    manifests = value.get("manifests")
    if not isinstance(manifests, list):
        _fail("CC002_OCI_INDEX", "OCI index manifests are required")
    matches = []
    for manifest in manifests:
        if not isinstance(manifest, dict):
            _fail("CC002_OCI_INDEX", "OCI manifest descriptor must be an object")
        platform = manifest.get("platform")
        if not isinstance(platform, dict):
            continue
        if platform.get("os") == "linux" and platform.get("architecture") == "amd64":
            digest = manifest.get("digest")
            if not isinstance(digest, str):
                _fail("CC002_OCI_INDEX", "linux/amd64 descriptor digest is required")
            matches.append(digest)
    if len(matches) != 1:
        _fail("CC002_OCI_PLATFORM", "OCI index must contain exactly one linux/amd64 child")
    if matches[0] != OCI_CHILD_DIGEST:
        _fail("CC002_OCI_CHILD", "OCI linux/amd64 child digest mismatch")
    return matches[0]


def image_pull_command() -> list[str]:
    return [DOCKER, "pull", "--platform", OCI_PLATFORM, OCI_CHILD_REFERENCE]


def image_inspect_command() -> list[str]:
    return [DOCKER, "image", "inspect", OCI_CHILD_REFERENCE, "--format", "{{json .}}"]


def docker_version_command() -> list[str]:
    return [DOCKER, "version", "--format", "{{json .Client.Version}}"]


def _validated_host_ownership(value: Any) -> dict[str, int]:
    if not isinstance(value, dict):
        _fail("CC002_HOST_USER", "host ownership tuple must be an object")
    _exact_keys(value, {"uid", "gid"}, "host ownership tuple")
    if any(
        not isinstance(value[field], int)
        or isinstance(value[field], bool)
        or value[field] <= 0
        for field in ("uid", "gid")
    ):
        _fail("CC002_HOST_USER", "host UID:GID must be nonroot positive integers")
    return {"uid": value["uid"], "gid": value["gid"]}


def host_ownership() -> dict[str, int]:
    """Return the runtime host ownership tuple used for bind-mount writes."""
    return _validated_host_ownership({"uid": os.getuid(), "gid": os.getgid()})


def _docker_user_argument(value: Mapping[str, Any] | None = None) -> str:
    ownership = host_ownership() if value is None else _validated_host_ownership(value)
    return f"{ownership['uid']}:{ownership['gid']}"


def _resolved_paths_overlap(first: Path, second: Path) -> bool:
    first = first.resolve()
    second = second.resolve()
    return first == second or first in second.parents or second in first.parents


def _resolver_pip_arguments(proxy_url: str) -> list[str]:
    if not isinstance(proxy_url, str):
        _fail("CC002_PROXY", "resolver proxy URL must be a string")
    try:
        parsed = urllib.parse.urlsplit(proxy_url)
        port = parsed.port
    except ValueError as error:
        _fail("CC002_PROXY", f"resolver proxy URL is invalid: {error}")
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or port is None
        or not 1 <= port <= 65535
        or parsed.netloc != f"127.0.0.1:{port}"
        or parsed.path
        or parsed.query
        or parsed.fragment
        or parsed.username is not None
        or parsed.password is not None
    ):
        _fail("CC002_PROXY", "resolver proxy must be an exact loopback HTTP authority")
    return [argument.format(proxy=proxy_url) for argument in RESOLVER_PIP_ARGUMENTS]


def _validated_resolver_pip_arguments(arguments: Any) -> list[str]:
    if (
        not isinstance(arguments, Sequence)
        or isinstance(arguments, (str, bytes))
        or not all(isinstance(argument, str) for argument in arguments)
    ):
        _fail("CC002_PIP_ARGUMENTS", "pinned pip arguments must be a string array")
    proxy_index = RESOLVER_PIP_ARGUMENTS.index("{proxy}")
    if len(arguments) != len(RESOLVER_PIP_ARGUMENTS):
        _fail("CC002_PIP_ARGUMENTS", "pinned pip argument count changed")
    expected = _resolver_pip_arguments(arguments[proxy_index])
    if list(arguments) != expected:
        _fail("CC002_PIP_ARGUMENTS", "pinned pip arguments changed")
    return expected


def _install_direct_dependency_guard(
    install_requirement: type, installation_error: type[Exception]
) -> type[Exception]:
    original_init = install_requirement.__init__

    class DirectDependencyReferenceError(installation_error):
        pass

    def guarded_direct_dependency_init(
        self: Any, req: Any, comes_from: Any, *args: Any, **kwargs: Any
    ) -> None:
        if comes_from is not None and req is not None and req.url:
            raise DirectDependencyReferenceError(
                f"direct dependency references are forbidden: {req}"
            )
        original_init(self, req, comes_from, *args, **kwargs)

    install_requirement.__init__ = guarded_direct_dependency_init
    return DirectDependencyReferenceError


def _self_test_direct_dependency_guard(
    direct_reference_error: type[Exception],
) -> None:
    from pip._internal.req.constructors import (
        install_req_from_line,
        install_req_from_req_string,
    )

    parent = install_req_from_line(
        f"/roots/{ROOT_WHEEL_FILENAMES[0]}", comes_from=None
    )
    direct_references = (
        "Beta @ https://example.invalid/beta.whl",
        "Beta @ git+file:///definitely-missing@abc",
        "Beta @ file:///definitely-missing.tar.gz",
    )
    for requirement in direct_references:
        try:
            install_req_from_req_string(requirement, comes_from=parent)
        except direct_reference_error:
            continue
        _fail(
            "CC002_PIP_GUARD",
            f"pinned pip direct-reference self-test did not refuse {requirement!r}",
        )
    ordinary = install_req_from_req_string("Beta>=3", comes_from=parent)
    if ordinary.req is None or ordinary.req.url:
        _fail("CC002_PIP_GUARD", "ordinary dependency self-test is invalid")


def _pinned_pip_main(arguments: Sequence[str] | None = None) -> int:
    fixed_arguments = _validated_resolver_pip_arguments(
        sys.argv[1:] if arguments is None else arguments
    )
    import pip

    try:
        version = pip.__version__
        origin = pip.__file__
    except AttributeError:
        _fail("CC002_PIP_IDENTITY", "pinned pip version and origin are required")
    if version != "25.0.1":
        _fail("CC002_PIP_IDENTITY", f"pinned pip must be 25.0.1, observed {version!r}")
    if not isinstance(origin, str) or os.path.normpath(origin) != PIP_IMPORT_ORIGIN:
        _fail(
            "CC002_PIP_IDENTITY",
            f"pinned pip must load from the retained root wheel: {origin!r}",
        )
    from pip._internal.exceptions import InstallationError
    from pip._internal.req.req_install import InstallRequirement

    direct_reference_error = _install_direct_dependency_guard(
        InstallRequirement, InstallationError
    )
    _self_test_direct_dependency_guard(direct_reference_error)
    from pip._internal.cli.main import main

    return main(fixed_arguments)


def parse_connect_request(source: bytes) -> tuple[str, int]:
    """Validate one bounded HTTP CONNECT request against the fixed host allowlist."""
    if not source or len(source) > PROXY_REQUEST_LIMIT:
        _fail("CC002_PROXY_SIZE", "CONNECT request is empty or exceeds the byte limit")
    if not source.endswith(b"\r\n\r\n") or source.count(b"\r\n\r\n") != 1:
        _fail("CC002_PROXY_REQUEST", "CONNECT request headers are incomplete")
    try:
        lines = source[:-4].decode("ascii").split("\r\n")
    except UnicodeDecodeError:
        _fail("CC002_PROXY_REQUEST", "CONNECT request must be ASCII")
    if not lines or any(not line for line in lines):
        _fail("CC002_PROXY_REQUEST", "CONNECT request contains an empty header line")
    request_line = lines[0].split(" ")
    if len(request_line) != 3 or request_line[0] != "CONNECT":
        _fail("CC002_PROXY_METHOD", "only the CONNECT method is permitted")
    authority, protocol = request_line[1:]
    if protocol != "HTTP/1.1":
        _fail("CC002_PROXY_PROTOCOL", "CONNECT requires HTTP/1.1")
    if (
        authority.count(":") != 1
        or any(character in authority for character in "@/?#\\")
    ):
        _fail("CC002_PROXY_AUTHORITY", "CONNECT authority must be host:port")
    host, port_source = authority.split(":")
    if host not in ACQUISITION_HTTPS_HOSTS or port_source != "443":
        _fail("CC002_PROXY_HOST", "CONNECT destination is outside the acquisition allowlist")
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            _fail("CC002_PROXY_HEADER", "CONNECT header is malformed")
        name, value = line.split(":", 1)
        normalized = name.casefold()
        if (
            not name
            or not all(character.isalnum() or character == "-" for character in name)
            or normalized in headers
        ):
            _fail("CC002_PROXY_HEADER", "CONNECT header name is invalid or duplicated")
        headers[normalized] = value.strip()
    if headers.get("host") != authority:
        _fail("CC002_PROXY_HOST", "CONNECT Host header must equal its authority")
    return host, 443


def _relay_socket(source: socket.socket, destination: socket.socket) -> None:
    try:
        while True:
            block = source.recv(64 * 1024)
            if not block:
                break
            destination.sendall(block)
    except OSError:
        pass
    finally:
        try:
            destination.shutdown(socket.SHUT_WR)
        except OSError:
            pass


class _ConnectProxyHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        request = bytearray()
        try:
            while b"\r\n\r\n" not in request:
                block = self.request.recv(min(4096, PROXY_REQUEST_LIMIT + 1 - len(request)))
                if not block:
                    break
                request.extend(block)
                if len(request) > PROXY_REQUEST_LIMIT:
                    break
            host, port = parse_connect_request(bytes(request))
        except CC002Error:
            self.request.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n")
            return
        try:
            upstream = socket.create_connection((host, port), timeout=NETWORK_TIMEOUT_SECONDS)
        except OSError:
            self.request.sendall(b"HTTP/1.1 502 Bad Gateway\r\nConnection: close\r\n\r\n")
            return
        with upstream:
            self.request.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            outbound = threading.Thread(
                target=_relay_socket,
                args=(self.request, upstream),
                daemon=True,
            )
            outbound.start()
            _relay_socket(upstream, self.request)
            outbound.join()


class _ConnectProxy(socketserver.ThreadingTCPServer):
    allow_reuse_address = False
    daemon_threads = True


def _resolver_child_environment(home: Path) -> dict[str, str]:
    if not home.is_absolute():
        _fail("CC002_HOME", "resolver child HOME must be an absolute controlled path")
    return {
        "ALL_PROXY": "",
        "HOME": str(home),
        "HTTP_PROXY": "",
        "HTTPS_PROXY": "",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "NO_PROXY": "",
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONPATH": f"/roots/{PIP_WHEEL_FILENAME}",
    }


def _resolver_main() -> int:
    """Run pinned pip behind the in-container fixed CONNECT allowlist."""
    home = Path("/tmp/cc002-home")
    home.mkdir(mode=0o700, exist_ok=True)
    environment = _resolver_child_environment(home)
    with _ConnectProxy(("127.0.0.1", 0), _ConnectProxyHandler) as proxy:
        host, port = proxy.server_address
        proxy_url = f"http://{host}:{port}"
        arguments = [
            "python",
            "-c",
            RESOLVER_PIP_PROGRAM,
            *_resolver_pip_arguments(proxy_url),
        ]
        worker = threading.Thread(target=proxy.serve_forever, daemon=True)
        worker.start()
        try:
            result = subprocess.run(
                arguments,
                cwd="/wheelhouse",
                env=environment,
                shell=False,
                check=False,
            )
        finally:
            proxy.shutdown()
            worker.join()
    return result.returncode


def resolve_command(
    roots: Path,
    wheelhouse: Path,
    *,
    built: Path,
    host_user: Mapping[str, Any] | None = None,
) -> list[str]:
    roots_resolved = roots.resolve()
    built_resolved = built.resolve()
    wheelhouse_resolved = wheelhouse.resolve()
    adapter_resolved = ADAPTER_PATH.resolve()
    mount_sources = (
        roots_resolved,
        built_resolved,
        wheelhouse_resolved,
        adapter_resolved,
    )
    if any(
        _resolved_paths_overlap(mount_sources[left], mount_sources[right])
        for left in range(len(mount_sources))
        for right in range(left + 1, len(mount_sources))
    ):
        _fail("CC002_RESOLVER_MOUNTS", "resolver mount paths must not overlap")
    return [
        DOCKER,
        "run",
        "--rm",
        "--pull=never",
        "--platform",
        OCI_PLATFORM,
        "--network",
        "bridge",
        "--read-only",
        "--user",
        _docker_user_argument(host_user),
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,nodev",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--env",
        "HTTP_PROXY=",
        "--env",
        "HTTPS_PROXY=",
        "--env",
        "ALL_PROXY=",
        "--env",
        "NO_PROXY=",
        "--env",
        "HOME=/tmp/cc002-home",
        "--env",
        "PYTHONPATH=/adapter",
        "-v",
        f"{roots_resolved}:/roots:ro",
        "-v",
        f"{built_resolved}:/built:ro",
        "-v",
        f"{wheelhouse_resolved}:/wheelhouse:rw",
        "-v",
        f"{adapter_resolved}:/adapter/contract_compiler_environment.py:ro",
        OCI_CHILD_REFERENCE,
        "python",
        "-c",
        RESOLVER_PROGRAM,
    ]


BUILD_PROGRAM = """\
import importlib.metadata
import json
import os
import pathlib
import platform
import subprocess
import sys
import sysconfig
import tarfile

facts = {
    'implementation': platform.python_implementation(),
    'version': platform.python_version(),
    'operating_system': platform.system(),
    'architecture': platform.machine(),
    'abi': f'cp{sys.version_info.major}{sys.version_info.minor}',
}
os.umask(0o022)
expected = {'implementation': 'CPython', 'version': '3.12.10',
            'operating_system': 'Linux', 'architecture': 'x86_64', 'abi': 'cp312'}
if facts != expected or sys.implementation.name != 'cpython':
    raise RuntimeError(f'unexpected Python tuple: {facts!r}')
if not str(sysconfig.get_config_var('SOABI')).startswith('cpython-312-'):
    raise RuntimeError('unexpected SOABI')
source = pathlib.Path('/tmp/source')
source.mkdir(mode=0o700)
home = pathlib.Path('/tmp/home')
home.mkdir(mode=0o700)
with tarfile.open('/inputs/antlr4-python3-runtime-4.9.3.tar.gz', 'r:gz') as archive:
    archive.extractall(source, filter='data')
project = source / 'antlr4-python3-runtime-4.9.3'
target = pathlib.Path('/tmp/cc002-backend')
if target.exists() or target.is_symlink():
    raise RuntimeError('backend target must initially be absent')
pip_wheel = '/pip/pip-25.0.1-py3-none-any.whl'
expected_pip_origin = '/pip/pip-25.0.1-py3-none-any.whl/pip/__init__.py'
sys.path.insert(0, pip_wheel)
import pip
if pip.__version__ != '25.0.1' or pip.__file__ != expected_pip_origin:
    raise RuntimeError(f'unexpected pip identity: {pip.__version__!r} {pip.__file__!r}')
environment = {
    'ALL_PROXY': '', 'HOME': '/tmp/home', 'HTTP_PROXY': '', 'HTTPS_PROXY': '',
    'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'NO_PROXY': '',
    'PATH': '/usr/local/bin:/usr/bin:/bin', 'PIP_DISABLE_PIP_VERSION_CHECK': '1',
    'PIP_NO_INPUT': '1', 'PYTHONDONTWRITEBYTECODE': '1',
    'PYTHONHASHSEED': '0', 'PYTHONIOENCODING': 'utf-8',
    'PYTHONNOUSERSITE': '1', 'PYTHONSAFEPATH': '1',
    'SOURCE_DATE_EPOCH': '315532800', 'TZ': 'UTC',
    'PYTHONPATH': pip_wheel,
}
subprocess.run([
    'python', '-P', '-S', '-m', 'pip', 'install', '--isolated', '--no-index', '--no-deps',
    '--no-cache-dir', '--no-compile', '--target=/tmp/cc002-backend',
    '/inputs/setuptools-83.0.0-py3-none-any.whl'],
    cwd='/tmp', env=environment, shell=False, check=True)
if not target.is_dir() or not any(target.iterdir()):
    raise RuntimeError('backend target was not populated')
if any(item.is_symlink() for item in target.rglob('*')):
    raise RuntimeError('backend target contains a symlink')
distributions = sorted(
    (item.metadata['Name'], item.version)
    for item in importlib.metadata.distributions(path=[str(target)]))
if distributions != [('setuptools', '83.0.0')]:
    raise RuntimeError(f'unexpected build distributions: {distributions!r}')
dist_infos = list(target.glob('setuptools-83.0.0.dist-info'))
if len(dist_infos) != 1:
    raise RuntimeError(f'unexpected setuptools dist-info set: {dist_infos!r}')
sys.path.insert(1, str(target))
import setuptools
import setuptools.build_meta
if setuptools.__version__ != '83.0.0' or not pathlib.Path(setuptools.__file__).is_relative_to(target):
    raise RuntimeError(f'unexpected setuptools identity: {setuptools.__version__!r} {setuptools.__file__!r}')
if not hasattr(setuptools.build_meta, '__legacy__'):
    raise RuntimeError('setuptools legacy PEP 517 backend is missing')
if not pathlib.Path(setuptools.build_meta.__file__).is_relative_to(target):
    raise RuntimeError(f'unexpected build_meta origin: {setuptools.build_meta.__file__!r}')
build_environment = dict(environment)
build_environment['PYTHONPATH'] = '/pip/pip-25.0.1-py3-none-any.whl:/tmp/cc002-backend'
subprocess.run([
    'python', '-P', '-S', '-m', 'pip', 'wheel', '--isolated', '--no-index', '--no-deps',
    '--no-cache-dir', '--no-build-isolation', '--use-pep517',
    '--wheel-dir', '/output', str(project)],
    cwd='/tmp', env=build_environment, shell=False, check=True)
facts = {
    'schema': 'malleus.cc002.source-build-child/v1',
    'python': facts,
    'preflight_pip': {'version': pip.__version__, 'origin': pip.__file__},
    'preflight_backend_distributions': [{'name': name, 'version': version} for name, version in distributions],
    'preflight_setuptools': {'version': setuptools.__version__, 'origin_root': str(target)},
    'source_date_epoch': int(build_environment['SOURCE_DATE_EPOCH']),
    'configuration': {'backend_interface': 'setuptools.build_meta:__legacy__',
                      'no_build_isolation': True},
    'tz': 'UTC',
    'python_hash_seed': '0',
    'umask': '022',
}
pathlib.Path('/output/.cc002-build-facts.json').write_text(
    json.dumps(facts, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\\n',
    encoding='utf-8')
"""

EXPECTED_BUILD_CHILD_FACTS = {
    "schema": "malleus.cc002.source-build-child/v1",
    "python": PYTHON_TUPLE,
    "preflight_pip": {"version": "25.0.1", "origin": "/pip/pip-25.0.1-py3-none-any.whl/pip/__init__.py"},
    "preflight_backend_distributions": [{"name": "setuptools", "version": "83.0.0"}],
    "preflight_setuptools": {"version": "83.0.0", "origin_root": "/tmp/cc002-backend"},
    "source_date_epoch": 315532800,
    "configuration": {"backend_interface": "setuptools.build_meta:__legacy__", "no_build_isolation": True},
    "tz": "UTC",
    "python_hash_seed": "0",
    "umask": "022",
}

RETAINED_BUILD_RUN = {
    "schema": "malleus.cc002.source-build-run/v1",
    "python": PYTHON_TUPLE,
    "preflight_pip": {"version": "25.0.1", "origin": PIP_WHEEL_FILENAME},
    "preflight_backend_distributions": [{"name": "setuptools", "version": "83.0.0"}],
    "preflight_setuptools": {"version": "83.0.0", "origin": SETUPTOOLS_WHEEL_FILENAME},
    "source_date_epoch": 315532800,
    "configuration": {"backend_interface": "setuptools.build_meta:__legacy__", "no_build_isolation": True},
    "tz": "UTC",
    "python_hash_seed": "0",
    "umask": "022",
}


def retained_build_run(value: Any) -> dict[str, Any]:
    if value != EXPECTED_BUILD_CHILD_FACTS:
        _fail("CC002_BUILD_FACTS", "cannot retain unvalidated source-build child facts")
    return json.loads(canonical_json(RETAINED_BUILD_RUN))


def build_command(
    build_inputs: Path,
    roots: Path,
    output: Path,
    *,
    host_user: Mapping[str, Any] | None = None,
) -> list[str]:
    build_inputs_resolved = build_inputs.resolve()
    roots_resolved = roots.resolve()
    output_resolved = output.resolve()
    mount_sources = (build_inputs_resolved, roots_resolved, output_resolved)
    if any(
        _resolved_paths_overlap(mount_sources[left], mount_sources[right])
        for left in range(len(mount_sources))
        for right in range(left + 1, len(mount_sources))
    ):
        _fail("CC002_BUILD_MOUNTS", "source-build mount paths must not overlap")
    return [
        DOCKER, "run", "--rm", "--pull=never", "--platform", OCI_PLATFORM,
        "--network", "none", "--read-only", "--user", _docker_user_argument(host_user),
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--env", f"SOURCE_DATE_EPOCH={SOURCE_DATE_EPOCH}", "--env", "TZ=UTC",
        "--env", "PYTHONHASHSEED=0", "--env", "HOME=/tmp/home",
        "--env", "HTTP_PROXY=", "--env", "HTTPS_PROXY=", "--env", "ALL_PROXY=",
        "--env", "NO_PROXY=", "-v", f"{build_inputs_resolved}:/inputs:ro",
        "-v", f"{(roots_resolved / PIP_WHEEL_FILENAME).resolve()}:/pip/{PIP_WHEEL_FILENAME}:ro",
        "-v", f"{output_resolved}:/output:rw", OCI_CHILD_REFERENCE,
        "python", "-c", BUILD_PROGRAM,
    ]


VERIFIER_PROGRAM = """\
import json
import pathlib
import platform
import subprocess
import sys
import sysconfig
import venv

work = pathlib.Path('/work')
python_facts = {
    'implementation': platform.python_implementation(),
    'version': platform.python_version(),
    'operating_system': platform.system(),
    'architecture': platform.machine(),
    'abi': f'cp{sys.version_info.major}{sys.version_info.minor}',
}
expected_python = {
    'implementation': 'CPython',
    'version': '3.12.10',
    'operating_system': 'Linux',
    'architecture': 'x86_64',
    'abi': 'cp312',
}
if sys.implementation.name != 'cpython' or python_facts != expected_python:
    raise RuntimeError(f'unexpected Python tuple: {python_facts!r}')
soabi = sysconfig.get_config_var('SOABI')
if not isinstance(soabi, str) or not soabi.startswith('cpython-312-'):
    raise RuntimeError(f'unexpected SOABI: {soabi!r}')
venv_path = work / 'venv'
venv.EnvBuilder(with_pip=False, clear=True, symlinks=False).create(venv_path)
python = str(venv_path / 'bin' / 'python')
base_env = {
    'HOME': '/work/home',
    'LANG': 'C.UTF-8',
    'LC_ALL': 'C.UTF-8',
    'PATH': '/usr/local/bin:/usr/bin:/bin',
    'PIP_DISABLE_PIP_VERSION_CHECK': '1',
    'PIP_NO_INPUT': '1',
    'PYTHONDONTWRITEBYTECODE': '1',
    'PYTHONIOENCODING': 'utf-8',
}
bootstrap_env = dict(base_env)
bootstrap_env['PYTHONPATH'] = '/wheelhouse/pip-25.0.1-py3-none-any.whl'
install = [
    python, '-m', 'pip', 'install', '--no-index', '--find-links=/wheelhouse',
    '--require-hashes', '-r', '/bundle/requirements.lock',
]
subprocess.run(install, cwd='/work', env=bootstrap_env, shell=False, check=True)
subprocess.run(
    [python, '-m', 'pip', 'check'],
    cwd='/work', env=base_env, shell=False, check=True,
)
subprocess.run(
    [python, '-c', '''\
import antlr4
import linkml
import linkml_runtime
from linkml_runtime.utils.namespaces import Namespaces
from prefixcommons import contract_uri, expand_uri
from pyshex.shex_evaluator import CFGraph
from rdflib import BNode, RDF, URIRef

if CFGraph.__module__ != 'CFGraph' or CFGraph.__name__ != 'CFGraph':
    raise RuntimeError(
        f'unexpected PyShEx CFGraph seam: {CFGraph.__module__}.{CFGraph.__name__}'
    )
graph = CFGraph()
subject = URIRef('urn:malleus:subject')
predicate = URIRef('urn:malleus:items')
head = BNode()
tail = BNode()
first = URIRef('urn:malleus:first')
second = URIRef('urn:malleus:second')
graph.add((subject, predicate, head))
graph.add((head, RDF.first, first))
graph.add((head, RDF.rest, tail))
graph.add((tail, RDF.first, second))
graph.add((tail, RDF.rest, RDF.nil))
flattened = sorted(
    (str(subject), str(predicate), str(item))
    for item in graph.objects(subject, predicate)
)
expected_flattened = [
    ('urn:malleus:subject', 'urn:malleus:items', 'urn:malleus:first'),
    ('urn:malleus:subject', 'urn:malleus:items', 'urn:malleus:second'),
]
if flattened != expected_flattened:
    raise RuntimeError(f'unexpected CFGraph collection flattening: {flattened!r}')

expanded = expand_uri('GO:0008150', strict=True)
if expanded != 'http://purl.obolibrary.org/obo/GO_0008150':
    raise RuntimeError(f'unexpected prefixcommons expansion: {expanded!r}')
contracted = contract_uri(expanded, strict=True)
if contracted != ['GO:0008150']:
    raise RuntimeError(f'unexpected prefixcommons contraction: {contracted!r}')
namespaces = Namespaces()
namespaces['ex'] = 'https://example.org/'
curie = namespaces.curie_for('https://example.org/item')
if curie != 'ex:item':
    raise RuntimeError(f'unexpected Namespaces CURIE: {curie!r}')
'''],
    cwd='/work', env=base_env, shell=False, check=True,
    capture_output=True, text=True,
)
generator_path = work / 'malleus.schema.json'
with generator_path.open('wb') as output:
    subprocess.run(
        [python, '-m', 'linkml.generators.jsonschemagen',
         '/input/malleus.yaml'],
        cwd='/work', env=base_env, shell=False, check=True, stdout=output,
    )
with generator_path.open(encoding='utf-8') as stream:
    generated = json.load(stream)
if not isinstance(generated, dict) or '$defs' not in generated:
    raise RuntimeError('generator output lacks required $defs object')
listed = subprocess.run(
    [python, '-m', 'pip', 'list', '--format=json'],
    cwd='/work', env=base_env, shell=False, check=True,
    capture_output=True, text=True,
)
distributions = json.loads(listed.stdout)
result = {
    'schema': 'malleus.cc002.container-verification/v1',
    'installed_distributions': distributions,
    'generator_output': '/work/malleus.schema.json',
    'python': python_facts,
}
(work / 'result.json').write_text(
    json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\\n',
    encoding='utf-8',
)
"""


LOCK_REPORT_PROGRAM = """\
import subprocess

environment = {
    'HOME': '/work/home',
    'LANG': 'C.UTF-8',
    'LC_ALL': 'C.UTF-8',
    'PATH': '/usr/local/bin:/usr/bin:/bin',
    'PIP_DISABLE_PIP_VERSION_CHECK': '1',
    'PIP_NO_INPUT': '1',
    'PYTHONDONTWRITEBYTECODE': '1',
    'PYTHONIOENCODING': 'utf-8',
    'PYTHONPATH': '/wheelhouse/pip-25.0.1-py3-none-any.whl',
}
subprocess.run(
    [
        'python', '-m', 'pip', 'install', '--dry-run', '--ignore-installed',
        '--no-index', '--find-links=/wheelhouse',
        '/wheelhouse/linkml-1.11.1-py3-none-any.whl',
        '/wheelhouse/linkml_runtime-1.11.1-py3-none-any.whl',
        '/wheelhouse/prefixcommons-0.1.12+malleus.1-py3-none-any.whl',
        '/wheelhouse/cfgraph-0.2.1-py3-none-any.whl',
        '--report', '/work/pip-report.json',
    ],
    cwd='/work', env=environment, shell=False, check=True,
)
"""


def lock_report_command(
    bundle: Path,
    work: Path,
    *,
    host_user: Mapping[str, Any] | None = None,
) -> list[str]:
    return [
        DOCKER,
        "run",
        "--rm",
        "--pull=never",
        "--platform",
        OCI_PLATFORM,
        "--network",
        "none",
        "--read-only",
        "--user",
        _docker_user_argument(host_user),
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,nodev",
        "-v",
        f"{(bundle / 'wheelhouse').resolve()}:/wheelhouse:ro",
        "-v",
        f"{work.resolve()}:/work:rw",
        OCI_CHILD_REFERENCE,
        "python",
        "-c",
        LOCK_REPORT_PROGRAM,
    ]


def verify_command(
    bundle: Path,
    work: Path,
    *,
    host_user: Mapping[str, Any] | None = None,
) -> list[str]:
    return [
        DOCKER,
        "run",
        "--rm",
        "--pull=never",
        "--platform",
        OCI_PLATFORM,
        "--network",
        "none",
        "--read-only",
        "--user",
        _docker_user_argument(host_user),
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,nodev",
        "-v",
        f"{(bundle / 'wheelhouse').resolve()}:/wheelhouse:ro",
        "-v",
        f"{(bundle / 'requirements.lock').resolve()}:/bundle/requirements.lock:ro",
        "-v",
        f"{SMOKE_INPUT.resolve()}:/input/malleus.yaml:ro",
        "-v",
        f"{work.resolve()}:/work:rw",
        OCI_CHILD_REFERENCE,
        "python",
        "-c",
        VERIFIER_PROGRAM,
    ]


def validated_docker_host() -> str:
    """Return the exact safe local Unix Docker endpoint supplied by Codex."""
    endpoint = os.environ.get("DOCKER_HOST")
    prefix = "unix://"
    if endpoint is None or endpoint == "":
        _fail(
            "CC002_DOCKER_HOST",
            "DOCKER_HOST is required; set it in the machine "
            "[mcp_servers.cc002.env] table, follow .codex/README.md, and restart Codex",
        )
    if not isinstance(endpoint, str) or not endpoint.startswith(prefix):
        _fail("CC002_DOCKER_HOST", "DOCKER_HOST must be a canonical local Unix URI")
    path_text = endpoint[len(prefix) :]
    if (
        not path_text.startswith("/")
        or path_text.startswith("//")
        or any(character in endpoint for character in ("?", "#", "%", "\\"))
        or not all(character.isprintable() for character in endpoint)
    ):
        _fail("CC002_DOCKER_HOST", "DOCKER_HOST must be a canonical local Unix URI")
    components = path_text.split("/")
    if (
        components[0] != ""
        or not components[1:]
        or any(component in {"", ".", ".."} for component in components[1:])
        or PurePosixPath(path_text).as_posix() != path_text
    ):
        _fail("CC002_DOCKER_HOST", "DOCKER_HOST path is not canonical")
    socket_path = Path(path_text)
    if not socket_path.is_absolute() or endpoint != prefix + socket_path.as_posix():
        _fail("CC002_DOCKER_HOST", "DOCKER_HOST path is not canonical")

    current_uid = os.getuid()
    candidates = [*reversed(socket_path.parents), socket_path]
    for candidate in candidates:
        try:
            metadata = os.lstat(candidate)
        except OSError as error:
            _fail(
                "CC002_DOCKER_HOST",
                f"DOCKER_HOST component is missing or unreadable: {candidate}: {error}",
            )
        if stat.S_ISLNK(metadata.st_mode):
            _fail("CC002_DOCKER_HOST", f"DOCKER_HOST component is a symlink: {candidate}")
        if candidate != socket_path:
            if not stat.S_ISDIR(metadata.st_mode):
                _fail("CC002_DOCKER_HOST", f"DOCKER_HOST parent is not a directory: {candidate}")
            if metadata.st_uid not in {0, current_uid}:
                _fail("CC002_DOCKER_HOST", f"DOCKER_HOST parent has an unsafe owner: {candidate}")
            if stat.S_IMODE(metadata.st_mode) & 0o022:
                _fail("CC002_DOCKER_HOST", f"DOCKER_HOST parent is group/world writable: {candidate}")
            continue
        if not stat.S_ISSOCK(metadata.st_mode):
            _fail("CC002_DOCKER_HOST", f"DOCKER_HOST target is not a socket: {candidate}")
        if metadata.st_uid != current_uid:
            _fail("CC002_DOCKER_HOST", f"DOCKER_HOST socket has an unsafe owner: {candidate}")
        if stat.S_IMODE(metadata.st_mode) != 0o600:
            _fail("CC002_DOCKER_HOST", f"DOCKER_HOST socket mode must be exactly 0600: {candidate}")
    return endpoint


def run_fixed(
    arguments: Sequence[str],
    operation_root: Path,
    *,
    docker_executable: str | None = None,
) -> subprocess.CompletedProcess[bytes]:
    if not arguments or arguments[0] != DOCKER or not all(isinstance(item, str) for item in arguments):
        _fail("CC002_COMMAND", "only fixed Docker argument vectors are permitted")
    if len(arguments) > 1 and arguments[1] == "run":
        if arguments.count("--user") != 1:
            _fail("CC002_HOST_USER", "every Docker run requires one host ownership tuple")
        user_index = arguments.index("--user")
        if user_index + 1 >= len(arguments) or arguments[user_index + 1] != _docker_user_argument():
            _fail("CC002_HOST_USER", "Docker run host ownership tuple changed")
    operation_root = operation_root.resolve()
    if operation_root.is_symlink() or not operation_root.is_dir():
        _fail("CC002_HOME", f"operation root must be a regular directory: {operation_root}")
    docker_host = validated_docker_host()
    resolved_executable = _resolved_docker()
    if docker_executable is not None and docker_executable != resolved_executable:
        _fail("CC002_DOCKER", "resolved Docker executable changed before subprocess")
    executable = resolved_executable
    if not isinstance(executable, str) or not Path(executable).is_absolute():
        _fail("CC002_DOCKER", "resolved Docker executable must be an absolute path")
    with tempfile.TemporaryDirectory(
        prefix=".cc002-home-", dir=operation_root
    ) as home_name:
        environment = {
            "DOCKER_HOST": docker_host,
            "HOME": home_name,
            **SUBPROCESS_ENV_BASE,
        }
        return subprocess.run(
            list(arguments),
            cwd=REPOSITORY,
            env=environment,
            shell=False,
            check=False,
            capture_output=True,
            executable=executable,
        )


def _run_checked(
    arguments: Sequence[str],
    context: str,
    operation_root: Path,
    *,
    docker_executable: str,
) -> bytes:
    result = run_fixed(
        arguments, operation_root, docker_executable=docker_executable
    )
    if result.returncode != 0:
        diagnostic = _subprocess_diagnostic(result.stderr, result.stdout)
        _fail(
            "CC002_SUBPROCESS",
            f"{context} failed with {result.returncode}: {diagnostic}",
        )
    return result.stdout


def _subprocess_diagnostic(stderr: bytes, stdout: bytes) -> str:
    sections = []
    for label, source in (("stderr", stderr), ("stdout", stdout)):
        decoded = source.decode("utf-8", errors="replace").strip()
        if not decoded:
            continue
        decoded = decoded.replace(
            "Traceback (most recent call last):", "[stack trace marker omitted]"
        )
        safe = "".join(
            character
            if character in "\n\t" or character.isprintable()
            else "\N{REPLACEMENT CHARACTER}"
            for character in decoded
        )
        sections.append(f"{label}: {safe}")
    diagnostic = "\n".join(sections) or "<no diagnostic output>"
    marker = "\n[truncated]\n"
    if len(diagnostic) > SUBPROCESS_DIAGNOSTIC_LIMIT:
        retained = SUBPROCESS_DIAGNOSTIC_LIMIT - len(marker)
        head = (retained + 1) // 2
        tail = retained - head
        diagnostic = diagnostic[:head] + marker + diagnostic[-tail:]
    return diagnostic


def _verify_local_image(source: bytes) -> None:
    value = strict_json(source, "Docker image inspect")
    if not isinstance(value, dict):
        _fail("CC002_IMAGE", "Docker image inspection must be an object")
    if value.get("Architecture") != "amd64" or value.get("Os") != "linux":
        _fail("CC002_IMAGE", "local image platform is not linux/amd64")
    digests = value.get("RepoDigests")
    if not isinstance(digests, list) or not all(isinstance(item, str) for item in digests):
        _fail("CC002_IMAGE", "local image RepoDigests are required")
    if not any(item.partition("@")[2] == OCI_CHILD_DIGEST for item in digests):
        _fail("CC002_IMAGE", "local image does not bind the selected child digest")


def _docker_version(source: bytes) -> str:
    value = strict_json(source, "Docker client version")
    if not isinstance(value, str) or not value.strip():
        _fail("CC002_DOCKER_VERSION", "Docker client version must be a nonempty string")
    return value


def _resolved_docker() -> str:
    executable = shutil.which(DOCKER, path=SANITIZED_PATH)
    if executable is None:
        _fail("CC002_DOCKER", f"docker is not executable on sanitized PATH {SANITIZED_PATH}")
    path = Path(executable)
    if not path.is_absolute() or not path.is_file() or not os.access(path, os.X_OK):
        _fail("CC002_DOCKER", f"resolved Docker executable is unsafe: {executable}")
    return str(path.resolve())


def _canonical_name(name: str) -> str:
    if not name or not all(character.isalnum() or character in "-_." for character in name):
        _fail("CC002_WHEEL_NAME", f"invalid distribution name: {name!r}")
    output: list[str] = []
    separator = False
    for character in name.casefold():
        if character in "-_.":
            if not separator:
                output.append("-")
            separator = True
        else:
            output.append(character)
            separator = False
    result = "".join(output).strip("-")
    if not result:
        _fail("CC002_WHEEL_NAME", f"invalid distribution name: {name!r}")
    return result


def _validate_archive_member_name(
    raw_name: Any,
    topology: dict[str, bool],
    error_code: str,
    *,
    is_directory: bool,
) -> PurePosixPath:
    """Validate one raw POSIX archive name without parser normalization."""
    if not isinstance(raw_name, str) or not raw_name:
        _fail(error_code, "archive member name must be a nonempty string")
    segments = raw_name.split("/")
    if is_directory and segments[-1] == "":
        segments = segments[:-1]
    segmented = "/".join(segments)
    canonical_spellings = {segmented}
    if is_directory:
        canonical_spellings.add(segmented + "/")
    if (
        any(not segment or segment in (".", "..") for segment in segments)
        or "\\" in raw_name
        or any(ord(character) < 32 or ord(character) == 127 for character in raw_name)
        or raw_name not in canonical_spellings
    ):
        _fail(error_code, f"unsafe noncanonical archive member: {raw_name!r}")
    normalized = PurePosixPath(*segments).as_posix()
    if normalized != segmented or normalized in topology:
        _fail(error_code, f"archive member normalization collision: {raw_name!r}")
    parts = normalized.split("/")
    ancestors = ("/".join(parts[:index]) for index in range(1, len(parts)))
    if any(ancestor in topology and not topology[ancestor] for ancestor in ancestors):
        _fail(error_code, f"non-directory archive member is an ancestor: {raw_name!r}")
    if not is_directory and any(name.startswith(normalized + "/") for name in topology):
        _fail(error_code, f"archive member conflicts with an existing descendant: {raw_name!r}")
    topology[normalized] = is_directory
    return PurePosixPath(*segments)


def _zip_extra_contains_zip64(source: bytes) -> bool:
    offset = 0
    while offset < len(source):
        if offset + 4 > len(source):
            return True
        header = int.from_bytes(source[offset : offset + 2], "little")
        size = int.from_bytes(source[offset + 2 : offset + 4], "little")
        offset += 4
        if offset + size > len(source):
            return True
        if header == 1:
            return True
        offset += size
    return False


_ZIP_END = struct.Struct("<4s4H2LH")
_ZIP_CENTRAL = struct.Struct("<4s4B4HL2L5H2L")
_ZIP_LOCAL = struct.Struct("<4s2B4HL2L2H")


def _validate_prefixcommons_zip_layout(
    path: Path,
    members: Sequence[zipfile.ZipInfo],
    error_code: str,
    *,
    exact_derived: bool,
) -> None:
    if len(members) > zipfile.ZIP_FILECOUNT_LIMIT or any(
        member.file_size > zipfile.ZIP64_LIMIT
        or member.compress_size > zipfile.ZIP64_LIMIT
        for member in members
    ):
        _fail(error_code, "archive capacity would require ZIP64")
    source = path.read_bytes()
    if len(source) < _ZIP_END.size:
        _fail(error_code, "truncated ZIP end record")
    try:
        end = _ZIP_END.unpack_from(source, len(source) - _ZIP_END.size)
    except struct.error as error:
        _fail(error_code, f"invalid ZIP end record: {error}")
    (
        signature,
        disk_number,
        central_disk,
        disk_entries,
        total_entries,
        central_size,
        central_offset,
        comment_length,
    ) = end
    if signature != b"PK\x05\x06" or comment_length != 0:
        _fail(error_code, "ZIP end record or archive comment changed")
    if (
        disk_number != 0
        or central_disk != 0
        or disk_entries != total_entries
        or total_entries != len(members)
    ):
        _fail(error_code, "multi-disk or inconsistent ZIP directory is forbidden")
    if (
        total_entries == 0xFFFF
        or central_size == 0xFFFFFFFF
        or central_offset == 0xFFFFFFFF
        or central_offset + central_size != len(source) - _ZIP_END.size
    ):
        _fail(error_code, "ZIP64 or non-canonical ZIP directory is forbidden")

    offset = central_offset
    local_end = 0
    raw_names: list[str] = []
    for member in members:
        if offset + _ZIP_CENTRAL.size > central_offset + central_size:
            _fail(error_code, "truncated central-directory entry")
        try:
            central = _ZIP_CENTRAL.unpack_from(source, offset)
        except struct.error as error:
            _fail(error_code, f"invalid central-directory entry: {error}")
        if central[0] != b"PK\x01\x02":
            _fail(error_code, "central-directory signature changed")
        name_length, extra_length, member_comment_length = central[12:15]
        variable_start = offset + _ZIP_CENTRAL.size
        variable_end = (
            variable_start + name_length + extra_length + member_comment_length
        )
        if variable_end > central_offset + central_size:
            _fail(error_code, "truncated central-directory member")
        name_source = source[variable_start : variable_start + name_length]
        central_extra = source[
            variable_start + name_length : variable_start + name_length + extra_length
        ]
        central_comment = source[
            variable_start + name_length + extra_length : variable_end
        ]
        try:
            name = name_source.decode("ascii")
        except UnicodeError as error:
            _fail(error_code, f"non-ASCII wheel member name: {error}")
        raw_names.append(name)
        local_offset = central[18]
        if (
            central[10] == 0xFFFFFFFF
            or central[11] == 0xFFFFFFFF
            or local_offset == 0xFFFFFFFF
            or central[15] == 0xFFFF
            or _zip_extra_contains_zip64(central_extra)
        ):
            _fail(error_code, f"ZIP64 member is forbidden: {name}")
        if local_offset + _ZIP_LOCAL.size > central_offset:
            _fail(error_code, f"invalid local-header offset: {name}")
        try:
            local = _ZIP_LOCAL.unpack_from(source, local_offset)
        except struct.error as error:
            _fail(error_code, f"invalid local header: {error}")
        if local[0] != b"PK\x03\x04":
            _fail(error_code, f"local-header signature changed: {name}")
        local_name_length, local_extra_length = local[10:12]
        local_variable = local_offset + _ZIP_LOCAL.size
        local_data = local_variable + local_name_length + local_extra_length
        local_name_source = source[local_variable : local_variable + local_name_length]
        local_extra = source[local_variable + local_name_length : local_data]
        if (
            local_data + central[10] > central_offset
            or local_name_source != name_source
            or local[1:5] != central[3:7]
            or local[5:10] != central[7:12]
            or _zip_extra_contains_zip64(local_extra)
        ):
            _fail(error_code, f"local and central ZIP headers disagree: {name}")
        if member.header_offset != local_offset or member.filename != name:
            _fail(error_code, f"decoded ZIP member disagrees with raw headers: {name}")
        if (
            member.CRC != central[9]
            or member.compress_size != central[10]
            or member.file_size != central[11]
            or member.extract_version != central[3]
            or member.reserved != central[4]
            or member.flag_bits != central[5]
            or member.compress_type != central[6]
            or member.create_version != central[1]
            or member.create_system != central[2]
            or member.volume != central[15]
            or member.internal_attr != central[16]
            or member.external_attr != central[17]
            or member.extra != central_extra
            or member.comment != central_comment
        ):
            _fail(
                error_code, f"decoded ZIP metadata disagrees with raw headers: {name}"
            )
        if exact_derived and (
            central[1:9] != (20, 3, 20, 0, 0, 0, 0, 33)
            or central[15:18] != (0, 0, 0o100644 << 16)
            or central_extra != b""
            or central_comment != b""
            or local[1:7] != (20, 0, 0, 0, 0, 33)
            or local_extra != b""
            or local_offset != local_end
        ):
            _fail(error_code, f"derived raw ZIP metadata changed: {name}")
        local_end = local_data + central[10]
        offset = variable_end
    if offset != central_offset + central_size or local_end != central_offset:
        _fail(error_code, "ZIP offsets are not exact consequences of member bytes")
    if raw_names != [member.filename for member in members]:
        _fail(error_code, "raw central-directory order changed")


def _canonical_wheel_record(sources: Mapping[str, bytes], record_name: str) -> bytes:
    rows = []
    for name in sorted((*sources, record_name)):
        if name == record_name:
            rows.append((name, "", ""))
            continue
        digest = base64.urlsafe_b64encode(
            hashlib.sha256(sources[name]).digest()
        ).rstrip(b"=")
        rows.append(
            (
                name,
                "sha256=" + digest.decode("ascii"),
                str(len(sources[name])),
            )
        )
    output = io.StringIO(newline="")
    writer = csv.writer(
        output,
        delimiter=",",
        quotechar='"',
        doublequote=True,
        escapechar=None,
        lineterminator="\n",
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def _prefixcommons_archive_sources(
    path: Path,
    *,
    dist_info: str,
    error_code: str,
    exact_derived: bool = False,
) -> tuple[list[zipfile.ZipInfo], dict[str, bytes]]:
    if path.is_symlink() or not path.is_file():
        _fail(error_code, f"wheel must be a regular file: {path}")
    try:
        try:
            archive_context = zipfile.ZipFile(path)
        except NotImplementedError as error:
            _fail(error_code, f"unsupported prefixcommons wheel archive: {error}")
        with archive_context as archive:
            members = archive.infolist()
            if archive.comment:
                _fail(error_code, "archive comment is forbidden")
            names = [member.filename for member in members]
            if len(names) != len(set(names)):
                _fail(error_code, "duplicate archive member name")
            topology: dict[str, bool] = {}
            for member in members:
                mode = member.external_attr >> 16
                _validate_archive_member_name(
                    member.filename,
                    topology,
                    error_code,
                    is_directory=False,
                )
                if (
                    member.filename.endswith("/")
                    or stat.S_IFMT(mode) not in (0, stat.S_IFREG)
                    or bool(member.flag_bits & 0x1)
                ):
                    _fail(error_code, f"non-regular wheel member: {member.filename}")
                if exact_derived and mode != stat.S_IFREG | 0o644:
                    _fail(error_code, f"derived wheel mode changed: {member.filename}")
            expected_names = set(PREFIXCOMMONS_PACKAGE_MEMBERS) | {
                f"{dist_info}/METADATA",
                f"{dist_info}/WHEEL",
                f"{dist_info}/LICENSE",
                f"{dist_info}/RECORD",
            }
            expected_expansion = (
                PREFIXCOMMONS_DERIVED_UNCOMPRESSED_BYTE_LENGTH
                if exact_derived
                else PREFIXCOMMONS_UNCOMPRESSED_BYTE_LENGTH
            )
            if set(names) != expected_names:
                _fail(error_code, "prefixcommons member inventory changed")
            if (
                len(members) != PREFIXCOMMONS_MEMBER_COUNT
                or len(PREFIXCOMMONS_PACKAGE_MEMBERS)
                != PREFIXCOMMONS_PACKAGE_MEMBER_COUNT
                or sum(member.file_size for member in members) != expected_expansion
            ):
                _fail(error_code, "prefixcommons member count or expansion changed")
            if exact_derived:
                expected_archive_size = (
                    expected_expansion
                    + _ZIP_END.size
                    + sum(
                        _ZIP_LOCAL.size
                        + _ZIP_CENTRAL.size
                        + 2 * len(name.encode("ascii"))
                        for name in names
                    )
                )
                if path.stat().st_size != expected_archive_size:
                    _fail(
                        error_code,
                        "derived archive size is not an exact consequence of members",
                    )
            _validate_prefixcommons_zip_layout(
                path,
                members,
                error_code,
                exact_derived=exact_derived,
            )
            try:
                sources = {
                    member.filename: archive.read(member) for member in members
                }
            except (NotImplementedError, zlib.error, lzma.LZMAError) as error:
                _fail(error_code, f"unreadable prefixcommons wheel member: {error}")
            if not exact_derived:
                _validate_record_rows(
                    archive,
                    members,
                    f"{dist_info}/RECORD",
                    error_code + "_RECORD",
                )
    except CC002Error:
        raise
    except (OSError, KeyError, UnicodeError, zipfile.BadZipFile) as error:
        _fail(error_code, f"invalid prefixcommons wheel archive: {error}")
    record_name = f"{dist_info}/RECORD"
    without_record = {
        name: source for name, source in sources.items() if name != record_name
    }
    if exact_derived and sources[record_name] != _canonical_wheel_record(
        without_record, record_name
    ):
        _fail(error_code + "_RECORD", "prefixcommons RECORD changed")
    return members, sources


def validate_prefixcommons_input(path: Path) -> dict[str, Any]:
    artifact = DERIVATIVE_INPUTS[0]
    expected_identity = {
        "filename": artifact.filename,
        "byte_length": artifact.byte_length,
        "sha256": "sha256:" + artifact.sha256,
    }
    if (
        path.is_symlink()
        or not path.is_file()
        or path.stat().st_size != artifact.byte_length
        or _artifact_record(path) != expected_identity
    ):
        _fail("CC002_PREFIXCOMMONS_INPUT", "upstream wheel identity mismatch")
    dist_info = "prefixcommons-0.1.12.dist-info"
    _members, sources = _prefixcommons_archive_sources(
        path,
        dist_info=dist_info,
        error_code="CC002_PREFIXCOMMONS_ARCHIVE",
    )
    metadata = sources[f"{dist_info}/METADATA"]
    wheel = sources[f"{dist_info}/WHEEL"]
    license_source = sources[f"{dist_info}/LICENSE"]
    facts = (
        (metadata, PREFIXCOMMONS_METADATA_BYTE_LENGTH, PREFIXCOMMONS_METADATA_SHA256),
        (wheel, PREFIXCOMMONS_WHEEL_BYTE_LENGTH, PREFIXCOMMONS_WHEEL_SHA256),
        (
            license_source,
            PREFIXCOMMONS_LICENSE_BYTE_LENGTH,
            PREFIXCOMMONS_LICENSE_SHA256,
        ),
    )
    if any(
        len(source) != expected_length
        or hashlib.sha256(source).hexdigest() != expected_digest
        for source, expected_length, expected_digest in facts
    ):
        _fail(
            "CC002_PREFIXCOMMONS_INPUT", "upstream metadata or license identity changed"
        )
    requirement = b"Requires-Dist: pytest-logging (>=2015.11.4,<2016.0.0)\n"
    if (
        metadata.count(b"Name: prefixcommons\n") != 1
        or metadata.count(b"Version: 0.1.12\n") != 1
        or metadata.count(requirement) != 1
        or wheel
        != b"Wheel-Version: 1.0\nGenerator: poetry 1.0.7\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
        or not license_source.startswith(b"BSD 3-Clause License")
    ):
        _fail("CC002_PREFIXCOMMONS_INPUT", "upstream semantic targets changed")
    return expected_identity


def _transformed_prefixcommons_sources(path: Path) -> dict[str, bytes]:
    upstream_dist = "prefixcommons-0.1.12.dist-info"
    derived_dist = "prefixcommons-0.1.12+malleus.1.dist-info"
    _members, upstream = _prefixcommons_archive_sources(
        path,
        dist_info=upstream_dist,
        error_code="CC002_PREFIXCOMMONS_ARCHIVE",
    )
    requirement = b"Requires-Dist: pytest-logging (>=2015.11.4,<2016.0.0)\n"
    sources: dict[str, bytes] = {}
    for name, source in upstream.items():
        if name == f"{upstream_dist}/RECORD":
            continue
        target_name = (
            derived_dist + name[len(upstream_dist) :]
            if name.startswith(upstream_dist + "/")
            else name
        )
        if name == f"{upstream_dist}/METADATA":
            source = source.replace(
                b"Version: 0.1.12\n",
                b"Version: 0.1.12+malleus.1\n",
                1,
            ).replace(requirement, b"", 1)
        elif name == f"{upstream_dist}/WHEEL":
            source = source.replace(
                b"Generator: poetry 1.0.7\n",
                b"Generator: malleus-cc002 (wheel-derivation-v1)\n",
                1,
            )
        sources[target_name] = source
    record_name = f"{derived_dist}/RECORD"
    sources[record_name] = _canonical_wheel_record(sources, record_name)
    return sources


def _fixed_zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.create_version = 20
    info.extract_version = 20
    info.reserved = 0
    info.flag_bits = 0
    info.volume = 0
    info.internal_attr = 0
    info.external_attr = 0o100644 << 16
    info.extra = b""
    info.comment = b""
    return info


def derive_prefixcommons_wheel(input_path: Path, output_path: Path) -> dict[str, Any]:
    validate_prefixcommons_input(input_path)
    if input_path.resolve() == output_path.resolve():
        _fail("CC002_DERIVATION", "input and output wheel paths must be distinct")
    if output_path.is_symlink() or output_path.exists():
        _fail("CC002_DERIVATION", "derived wheel output must initially be absent")
    if output_path.name != PREFIXCOMMONS_DERIVED_FILENAME:
        _fail("CC002_DERIVATION", "derived wheel filename changed")
    sources = _transformed_prefixcommons_sources(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(
            output_path,
            "x",
            compression=zipfile.ZIP_STORED,
            allowZip64=False,
        ) as archive:
            archive.comment = b""
            for name in sorted(sources):
                archive.writestr(_fixed_zip_info(name), sources[name])
        return _validate_prefixcommons_derivation(input_path, output_path)
    except zipfile.LargeZipFile as error:
        if output_path.exists() and not output_path.is_symlink():
            output_path.unlink()
        _fail("CC002_DERIVATION", f"ZIP64 output is forbidden: {error}")
    except Exception:
        if output_path.exists() and not output_path.is_symlink():
            output_path.unlink()
        raise


def validate_derived_prefixcommons_wheel(path: Path) -> dict[str, Any]:
    if path.name != PREFIXCOMMONS_DERIVED_FILENAME:
        _fail("CC002_DERIVED_ARCHIVE", "derived wheel filename changed")
    dist_info = "prefixcommons-0.1.12+malleus.1.dist-info"
    members, sources = _prefixcommons_archive_sources(
        path,
        dist_info=dist_info,
        error_code="CC002_DERIVED_ARCHIVE",
        exact_derived=True,
    )
    names = [member.filename for member in members]
    if names != sorted(names) or any(
        name.encode("ascii").decode("ascii") != name for name in names
    ):
        _fail("CC002_DERIVED_ARCHIVE", "derived member order or spelling changed")
    for member in members:
        source = sources[member.filename]
        if (
            member.date_time != (1980, 1, 1, 0, 0, 0)
            or member.compress_type != zipfile.ZIP_STORED
            or member.create_system != 3
            or member.create_version != 20
            or member.extract_version != 20
            or member.reserved != 0
            or member.flag_bits != 0
            or member.volume != 0
            or member.internal_attr != 0
            or member.external_attr != 0o100644 << 16
            or member.extra != b""
            or member.comment != b""
            or member.compress_size != len(source)
            or member.file_size != len(source)
            or member.CRC != zlib.crc32(source)
        ):
            _fail(
                "CC002_DERIVED_ARCHIVE",
                f"derived ZIP metadata changed: {member.filename}",
            )
    metadata = sources[f"{dist_info}/METADATA"]
    wheel = sources[f"{dist_info}/WHEEL"]
    license_source = sources[f"{dist_info}/LICENSE"]
    removed = b"Requires-Dist: pytest-logging (>=2015.11.4,<2016.0.0)\n"
    if (
        metadata.count(b"Name: prefixcommons\n") != 1
        or metadata.count(b"Version: 0.1.12+malleus.1\n") != 1
        or b"Version: 0.1.12\n" in metadata
        or removed in metadata
        or wheel
        != b"Wheel-Version: 1.0\nGenerator: malleus-cc002 (wheel-derivation-v1)\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
        or len(license_source) != PREFIXCOMMONS_LICENSE_BYTE_LENGTH
        or hashlib.sha256(license_source).hexdigest() != PREFIXCOMMONS_LICENSE_SHA256
        or not license_source.startswith(b"BSD 3-Clause License")
    ):
        _fail("CC002_DERIVED_ARCHIVE", "derived metadata or license changed")
    record = _artifact_record(path)
    record.update({"distribution": "prefixcommons", "version": "0.1.12+malleus.1"})
    return record


def _validate_prefixcommons_derivation(
    upstream_path: Path,
    derived_path: Path,
) -> dict[str, Any]:
    try:
        validate_prefixcommons_input(upstream_path)
        record = validate_derived_prefixcommons_wheel(derived_path)
    except CC002Error as error:
        _fail(
            "CC002_DERIVATION_IDENTITY",
            f"prefixcommons derivation validation failed: {error}",
        )
    expected = _transformed_prefixcommons_sources(upstream_path)
    derived_dist = "prefixcommons-0.1.12+malleus.1.dist-info"
    _members, observed = _prefixcommons_archive_sources(
        derived_path,
        dist_info=derived_dist,
        error_code="CC002_DERIVED_ARCHIVE",
        exact_derived=True,
    )
    if observed != expected:
        _fail(
            "CC002_DERIVATION_IDENTITY",
            "derived wheel bytes exceed the governed metadata-only transformation",
        )
    return record


def _observe_derivation_child() -> dict[str, Any]:
    return {
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "operating_system": platform.system(),
            "architecture": platform.machine(),
            "abi": f"cp{sys.version_info.major}{sys.version_info.minor}",
        },
        "implementation_name": sys.implementation.name,
        "soabi": sysconfig.get_config_var("SOABI"),
        "effective_uid": os.geteuid(),
        "environment": {
            "source_date_epoch": os.environ.get("SOURCE_DATE_EPOCH"),
            "tz": os.environ.get("TZ"),
            "python_hash_seed": os.environ.get("PYTHONHASHSEED"),
        },
        "adapter_sha256": _digest(ADAPTER_PATH.read_bytes()),
    }


def _derivation_main() -> int:
    os.umask(0o022)
    observed = _observe_derivation_child()
    _exact_keys(
        observed,
        {
            "python",
            "implementation_name",
            "soabi",
            "effective_uid",
            "environment",
            "adapter_sha256",
        },
        "prefixcommons derivation observations",
    )
    if (
        observed["python"] != PYTHON_TUPLE
        or observed["implementation_name"] != "cpython"
        or not isinstance(observed["soabi"], str)
        or not observed["soabi"].startswith("cpython-312-")
        or not isinstance(observed["effective_uid"], int)
        or isinstance(observed["effective_uid"], bool)
        or observed["effective_uid"] <= 0
        or observed["environment"]
        != {
            "source_date_epoch": SOURCE_DATE_EPOCH,
            "tz": "UTC",
            "python_hash_seed": "0",
        }
        or observed["adapter_sha256"]
        != EXPECTED_DERIVATION_CHILD_FACTS["tool"]["adapter_sha256"]
    ):
        _fail(
            "CC002_DERIVATION_FACTS",
            f"selected derivation child observations changed: {observed!r}",
        )
    input_root = DERIVATION_INPUT_ROOT
    output_root = DERIVATION_OUTPUT_ROOT
    if (
        input_root.is_symlink()
        or output_root.is_symlink()
        or not input_root.is_dir()
        or not output_root.is_dir()
        or input_root.resolve() == output_root.resolve()
    ):
        _fail("CC002_DERIVATION", "derivation mount roots must be distinct directories")
    input_members = {member.name: member for member in input_root.iterdir()}
    if set(input_members) != {PREFIXCOMMONS_INPUT_FILENAME}:
        _fail("CC002_DERIVATION", "derivative input directory membership changed")
    if any(output_root.iterdir()):
        _fail("CC002_DERIVATION", "derivation output directory must initially be empty")
    upstream = input_members[PREFIXCOMMONS_INPUT_FILENAME]
    derived = output_root / PREFIXCOMMONS_DERIVED_FILENAME
    facts_path = output_root / ".cc002-derivation-facts.json"
    try:
        derive_prefixcommons_wheel(upstream, derived)
        facts = json.loads(canonical_json(EXPECTED_DERIVATION_CHILD_FACTS))
        facts["output"] = _artifact_record(derived)
        with facts_path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(canonical_json(facts) + "\n")
    except Exception:
        for path in (facts_path, derived):
            if path.exists() and not path.is_symlink():
                path.unlink()
        raise
    return 0


def validate_derivation_outputs(first: Path, second: Path) -> dict[str, Any]:
    if (
        first.is_symlink()
        or second.is_symlink()
        or not first.is_dir()
        or not second.is_dir()
        or first.resolve() == second.resolve()
    ):
        _fail(
            "CC002_DERIVATION_OUTPUT",
            "independent derivation output directories must be distinct",
        )
    wheels: list[Path] = []
    facts_values: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    expected_names = {
        PREFIXCOMMONS_DERIVED_FILENAME,
        ".cc002-derivation-facts.json",
    }
    for output in (first, second):
        members = {member.name: member for member in output.iterdir()}
        if set(members) != expected_names:
            _fail(
                "CC002_DERIVATION_OUTPUT",
                "each derivation must produce one wheel and one child-facts record",
            )
        wheel = members[PREFIXCOMMONS_DERIVED_FILENAME]
        facts_path = members[".cc002-derivation-facts.json"]
        try:
            record = validate_derived_prefixcommons_wheel(wheel)
        except CC002Error as error:
            _fail(
                "CC002_DERIVATION_OUTPUT",
                f"derived wheel validation failed: {error}",
            )
        output_identity = _artifact_record(wheel)
        facts, _source = _load_json_file(
            facts_path,
            "prefixcommons derivation child facts",
        )
        if facts != {**EXPECTED_DERIVATION_CHILD_FACTS, "output": output_identity}:
            _fail("CC002_DERIVATION_FACTS", "derivation child facts changed")
        wheels.append(wheel)
        facts_values.append(facts)
        records.append(record)
    if facts_values[0] != facts_values[1]:
        _fail("CC002_DERIVATION_FACTS", "independent derivation facts differ")
    if records[0] != records[1] or wheels[0].read_bytes() != wheels[1].read_bytes():
        _fail(
            "CC002_DERIVATION_REPRODUCIBILITY",
            "independent prefixcommons derivations are not byte-identical",
        )
    return records[0]


def derivation_command(
    derivative_inputs: Path,
    output: Path,
    *,
    host_user: Mapping[str, Any] | None = None,
) -> list[str]:
    if (
        derivative_inputs.is_symlink()
        or output.is_symlink()
        or not derivative_inputs.is_dir()
        or not output.is_dir()
    ):
        _fail("CC002_DERIVATION_MOUNTS", "derivation mount sources must be directories")
    inputs_resolved = derivative_inputs.resolve()
    output_resolved = output.resolve()
    adapter_resolved = ADAPTER_PATH.resolve()
    if _resolved_paths_overlap(
        inputs_resolved, output_resolved
    ) or _resolved_paths_overlap(output_resolved, adapter_resolved):
        _fail("CC002_DERIVATION_MOUNTS", "derivation mount sources must not overlap")
    return [
        DOCKER,
        "run",
        "--rm",
        "--pull=never",
        "--platform",
        OCI_PLATFORM,
        "--network",
        "none",
        "--read-only",
        "--user",
        _docker_user_argument(host_user),
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,nodev",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--env",
        f"SOURCE_DATE_EPOCH={SOURCE_DATE_EPOCH}",
        "--env",
        "TZ=UTC",
        "--env",
        "PYTHONHASHSEED=0",
        "--env",
        "HOME=/tmp/home",
        "--env",
        "PYTHONPATH=/adapter",
        "--env",
        "HTTP_PROXY=",
        "--env",
        "HTTPS_PROXY=",
        "--env",
        "ALL_PROXY=",
        "--env",
        "NO_PROXY=",
        "-v",
        f"{inputs_resolved}:/derivative-inputs:ro",
        "-v",
        f"{output_resolved}:/output:rw",
        "-v",
        f"{adapter_resolved}:/adapter/contract_compiler_environment.py:ro",
        OCI_CHILD_REFERENCE,
        "python",
        "-c",
        DERIVATION_PROGRAM,
    ]


def validate_antlr_sdist(path: Path) -> dict[str, Any]:
    """Refuse unsafe or semantically wrong ANTLR source archives before execution."""
    artifact = BUILD_ARTIFACTS[0]
    if _artifact_record(path) != {
        "filename": artifact.filename,
        "byte_length": artifact.byte_length,
        "sha256": "sha256:" + artifact.sha256,
    }:
        _fail("CC002_BUILD_INPUT", "ANTLR sdist identity mismatch")
    try:
        with tarfile.open(path, "r:gz") as archive:
            members = archive.getmembers()
            names: set[str] = set()
            regular_files: set[str] = set()
            normalized_names: dict[str, bool] = {}
            top_levels: set[str] = set()
            total = 0
            pkg_info = None
            for member in members:
                pure = _validate_archive_member_name(
                    member.name,
                    normalized_names,
                    "CC002_SDIST_SAFETY",
                    is_directory=member.isdir(),
                )
                if (
                    not (member.isfile() or member.isdir())
                ):
                    _fail("CC002_SDIST_SAFETY", f"unsafe sdist member: {member.name!r}")
                names.add(member.name)
                top_levels.add(pure.parts[0])
                if member.isfile():
                    total += member.size
                    regular_files.add(member.name)
                if pure.name == "PKG-INFO" and len(pure.parts) == 2 and member.isfile():
                    extracted = archive.extractfile(member)
                    pkg_info = extracted.read() if extracted is not None else None
            expected_root = "antlr4-python3-runtime-4.9.3"
            if top_levels != {expected_root}:
                _fail("CC002_SDIST_LAYOUT", "ANTLR sdist must have one exact top-level directory")
            if f"{expected_root}/setup.py" not in regular_files or f"{expected_root}/pyproject.toml" in names:
                _fail("CC002_SDIST_LAYOUT", "ANTLR sdist legacy build layout changed")
            if pkg_info is None:
                _fail("CC002_SDIST_METADATA", "ANTLR sdist PKG-INFO is missing")
    except (tarfile.TarError, OSError) as error:
        _fail("CC002_SDIST", f"invalid ANTLR sdist: {error}")
    metadata = BytesParser(policy=email.policy.default).parsebytes(pkg_info)
    if metadata.get_all("Name") != ["antlr4-python3-runtime"] or metadata.get_all("Version") != ["4.9.3"]:
        _fail("CC002_SDIST_METADATA", "ANTLR sdist name/version mismatch")
    if len(members) != ANTLR_SDIST_MEMBER_COUNT or total != ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH:
        _fail("CC002_SDIST_LIMIT", "ANTLR sdist member count or expansion changed")
    return {"member_count": len(members), "uncompressed_byte_length": total}


def validate_setuptools_wheel(path: Path) -> None:
    artifact = BUILD_ARTIFACTS[1]
    if _artifact_record(path) != {
        "filename": artifact.filename,
        "byte_length": artifact.byte_length,
        "sha256": "sha256:" + artifact.sha256,
    }:
        _fail("CC002_BUILD_INPUT", "setuptools wheel identity mismatch")
    try:
        name, version = _wheel_metadata(path)
    except CC002Error as error:
        _fail("CC002_BUILD_INPUT", f"setuptools wheel structure is invalid: {error}")
    if _canonical_name(name) != "setuptools" or version != "83.0.0":
        _fail("CC002_BUILD_INPUT", "setuptools wheel metadata mismatch")
    _validate_setuptools_archive(path)


def _safe_wheel_members(
    archive: zipfile.ZipFile,
    error_code: str,
    *,
    enforce_build_limits: bool,
) -> list[zipfile.ZipInfo]:
    members = archive.infolist()
    names: set[str] = set()
    normalized_names: dict[str, bool] = {}
    expanded = 0
    for member in members:
        mode = member.external_attr >> 16
        file_type = stat.S_IFMT(mode)
        name_is_directory = member.filename.endswith("/")
        if file_type and name_is_directory != stat.S_ISDIR(mode):
            _fail(error_code, f"wheel member name/type mismatch: {member.filename!r}")
        _validate_archive_member_name(
            member.filename,
            normalized_names,
            error_code,
            is_directory=name_is_directory or stat.S_ISDIR(mode),
        )
        if (
            bool(member.flag_bits & 0x1)
            or stat.S_ISLNK(mode)
            or (file_type and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)))
        ):
            _fail(error_code, f"unsafe wheel member: {member.filename!r}")
        names.add(member.filename)
        expanded += member.file_size
        if enforce_build_limits and (
            len(members) > 1000 or expanded > 16 * 1024 * 1024
        ):
            _fail(error_code, "wheel member count or expansion exceeds its bound")
    return members


def _validate_record_rows(
    archive: zipfile.ZipFile, members: Sequence[zipfile.ZipInfo], record_name: str, context: str
) -> None:
    names = {member.filename for member in members}
    try:
        rows = list(csv.reader(io.StringIO(archive.read(record_name).decode("utf-8"))))
    except (KeyError, UnicodeError, csv.Error) as error:
        _fail(context, f"wheel RECORD is invalid: {error}")
    if len(rows) != len(members) or any(len(row) != 3 for row in rows):
        _fail(context, "wheel RECORD is incomplete")
    records = {row[0]: row[1:] for row in rows}
    if set(records) != names or records.get(record_name) != ["", ""]:
        _fail(context, "wheel RECORD membership mismatch")
    for name in names - {record_name}:
        digest, length = records[name]
        source = archive.read(name)
        encoded = base64.urlsafe_b64encode(hashlib.sha256(source).digest()).rstrip(b"=").decode("ascii")
        if digest != "sha256=" + encoded or length != str(len(source)):
            _fail(context, f"wheel RECORD mismatch: {name}")


def validate_embedded_cfgraph_wheel(path: Path) -> dict[str, Any]:
    """Validate the exact provisional CFGraph root and return its wheel record."""
    expected_content = {
        "filename": CFGRAPH_WHEEL_FILENAME,
        "byte_length": CFGRAPH_WHEEL_BYTE_LENGTH,
        "sha256": "sha256:" + CFGRAPH_WHEEL_SHA256,
    }
    if _artifact_record(path) != expected_content:
        _fail("CC002_CFGRAPH_IDENTITY", "embedded CFGraph wheel identity mismatch")
    dist_info = "cfgraph-0.2.1.dist-info"
    expected_names = [
        "CFGraph/__init__.py",
        f"{dist_info}/METADATA",
        f"{dist_info}/WHEEL",
        f"{dist_info}/top_level.txt",
        f"{dist_info}/RECORD",
    ]
    try:
        with zipfile.ZipFile(path) as archive:
            members = _safe_wheel_members(
                archive,
                "CC002_CFGRAPH_SAFETY",
                enforce_build_limits=True,
            )
            names = [member.filename for member in members]
            if archive.comment or names != expected_names or any(
                member.is_dir() for member in members
            ):
                _fail(
                    "CC002_CFGRAPH_SAFETY",
                    "embedded CFGraph wheel member inventory changed",
                )
            license_prefixes = ("license", "licence", "copying", "notice")
            if any(
                PurePosixPath(name).name.casefold().startswith(license_prefixes)
                for name in names
            ):
                _fail(
                    "CC002_CFGRAPH_LICENSE",
                    "embedded CFGraph wheel unexpectedly contains license-like bytes",
                )
            metadata = BytesParser(policy=email.policy.default).parsebytes(
                archive.read(f"{dist_info}/METADATA")
            )
            wheel = BytesParser(policy=email.policy.default).parsebytes(
                archive.read(f"{dist_info}/WHEEL")
            )
            if (
                metadata.get_all("Name") != ["CFGraph"]
                or metadata.get_all("Version") != ["0.2.1"]
                or metadata.get_all("Requires-Dist") != ["rdflib>=0.4.2"]
                or metadata.get_all("License") != ["Apache 2.0"]
            ):
                _fail(
                    "CC002_CFGRAPH_METADATA",
                    "embedded CFGraph package metadata changed",
                )
            if (
                wheel.get_all("Wheel-Version") != ["1.0"]
                or wheel.get_all("Generator") != ["setuptools (83.0.0)"]
                or wheel.get_all("Root-Is-Purelib") != ["true"]
                or wheel.get_all("Tag") != ["py3-none-any"]
            ):
                _fail(
                    "CC002_CFGRAPH_METADATA",
                    "embedded CFGraph wheel metadata changed",
                )
            _validate_record_rows(
                archive,
                members,
                f"{dist_info}/RECORD",
                "CC002_CFGRAPH_RECORD",
            )
    except CC002Error:
        raise
    except (OSError, KeyError, UnicodeError, zipfile.BadZipFile) as error:
        _fail("CC002_CFGRAPH_WHEEL", f"invalid embedded CFGraph wheel: {error}")
    return {**expected_content, "distribution": "CFGraph", "version": "0.2.1"}


def _validate_setuptools_archive(path: Path) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            members = _safe_wheel_members(
                archive, "CC002_BUILD_INPUT", enforce_build_limits=True
            )
            names = {member.filename for member in members}
            dist_info = "setuptools-83.0.0.dist-info"
            if {PurePosixPath(name).parts[0] for name in names if PurePosixPath(name).parts[0].endswith(".dist-info")} != {dist_info}:
                _fail("CC002_BUILD_INPUT", "setuptools dist-info membership mismatch")
            metadata_name = f"{dist_info}/METADATA"
            wheel_name = f"{dist_info}/WHEEL"
            record_name = f"{dist_info}/RECORD"
            if not {metadata_name, wheel_name, record_name}.issubset(names):
                _fail("CC002_BUILD_INPUT", "setuptools wheel metadata is incomplete")
            metadata = BytesParser(policy=email.policy.default).parsebytes(archive.read(metadata_name))
            wheel = BytesParser(policy=email.policy.default).parsebytes(archive.read(wheel_name))
            if metadata.get_all("Name") != ["setuptools"] or metadata.get_all("Version") != ["83.0.0"]:
                _fail("CC002_BUILD_INPUT", "setuptools metadata headers changed")
            if wheel.get_all("Root-Is-Purelib") != ["true"] or wheel.get_all("Tag") != ["py3-none-any"]:
                _fail("CC002_BUILD_INPUT", "setuptools wheel tag changed")
            _validate_record_rows(archive, members, record_name, "CC002_BUILD_INPUT")
    except (OSError, zipfile.BadZipFile) as error:
        _fail("CC002_BUILD_INPUT", f"setuptools wheel archive is invalid: {error}")


def validate_built_antlr_wheel(path: Path) -> dict[str, Any]:
    """Validate the deterministic wheel contract and return its closed record."""
    expected_filename = "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    if path.is_symlink() or not path.is_file() or path.name != expected_filename:
        _fail("CC002_BUILT_WHEEL", "build must produce the exact pure wheel filename")
    try:
        with zipfile.ZipFile(path) as archive:
            members = _safe_wheel_members(
                archive, "CC002_BUILT_WHEEL_SAFETY", enforce_build_limits=True
            )
            names = {member.filename for member in members}
            dist_info = "antlr4_python3_runtime-4.9.3.dist-info"
            dist_infos = {PurePosixPath(name).parts[0] for name in names if PurePosixPath(name).parts[0].endswith(".dist-info")}
            if dist_infos != {dist_info}:
                _fail("CC002_BUILT_WHEEL_METADATA", "built wheel dist-info membership mismatch")
            required = {f"{dist_info}/METADATA", f"{dist_info}/WHEEL", f"{dist_info}/RECORD"}
            if not required.issubset(names):
                _fail("CC002_BUILT_WHEEL", "built wheel metadata files are incomplete")
            metadata = BytesParser(policy=email.policy.default).parsebytes(archive.read(f"{dist_info}/METADATA"))
            wheel = BytesParser(policy=email.policy.default).parsebytes(archive.read(f"{dist_info}/WHEEL"))
            if metadata.get_all("Name") != ["antlr4-python3-runtime"] or metadata.get_all("Version") != ["4.9.3"]:
                _fail("CC002_BUILT_WHEEL_METADATA", "built wheel name/version mismatch")
            if wheel.get_all("Wheel-Version") != ["1.0"] or wheel.get_all("Root-Is-Purelib") != ["true"]:
                _fail("CC002_BUILT_WHEEL_METADATA", "built wheel is not pure Wheel-Version 1.0")
            if wheel.get_all("Tag") != ["py3-none-any"] or wheel.get_all("Generator") != ["setuptools (83.0.0)"]:
                _fail("CC002_BUILT_WHEEL_METADATA", "built wheel tag or generator mismatch")
            record_name = f"{dist_info}/RECORD"
            _validate_record_rows(archive, members, record_name, "CC002_BUILT_WHEEL_RECORD")
    except (zipfile.BadZipFile, UnicodeError, csv.Error, OSError) as error:
        _fail("CC002_BUILT_WHEEL", f"invalid built wheel: {error}")
    record = _artifact_record(path)
    record.update({"distribution": "antlr4-python3-runtime", "version": "4.9.3"})
    return record


def validate_build_outputs(first: Path, second: Path) -> dict[str, Any]:
    if first.is_symlink() or second.is_symlink() or not first.is_dir() or not second.is_dir():
        _fail("CC002_BUILD_OUTPUT", "build outputs must be regular directories")
    if first.resolve() == second.resolve():
        _fail("CC002_BUILD_OUTPUT", "independent build output directories must be distinct")
    paths = []
    observed_facts = []
    for output in (first, second):
        members = {member.name: member for member in output.iterdir()}
        fact_path = members.pop(".cc002-build-facts.json", None)
        wheels = [member for member in members.values() if member.name.endswith(".whl")]
        if fact_path is None or len(members) != 1 or len(wheels) != 1:
            _fail("CC002_BUILD_OUTPUT", "each build must produce one wheel and one child-facts record")
        paths.append(wheels[0])
        facts, _source = _load_json_file(fact_path, "source build child facts")
        if facts != EXPECTED_BUILD_CHILD_FACTS:
            _fail("CC002_BUILD_FACTS", "source build child facts changed")
        observed_facts.append(facts)
    records = [validate_built_antlr_wheel(path) for path in paths]
    if observed_facts[0] != observed_facts[1]:
        _fail("CC002_BUILD_FACTS", "independent source-build child facts differ")
    if records[0] != records[1] or paths[0].read_bytes() != paths[1].read_bytes():
        _fail("CC002_BUILD_REPRODUCIBILITY", "independent ANTLR builds are not byte-identical")
    return records[0]


def _wheel_metadata(path: Path) -> tuple[str, str]:
    if path.is_symlink() or not path.is_file():
        _fail("CC002_WHEEL", f"wheel must be a regular file: {path}")
    try:
        with zipfile.ZipFile(path) as archive:
            infos = _safe_wheel_members(
                archive, "CC002_WHEEL", enforce_build_limits=False
            )
            metadata_names = []
            for info in infos:
                member = PurePosixPath(info.filename)
                if len(member.parts) == 2 and member.parts[0].endswith(".dist-info") and member.parts[1] == "METADATA":
                    metadata_names.append(info.filename)
            if len(metadata_names) != 1:
                _fail("CC002_WHEEL", f"wheel must contain exactly one METADATA: {path.name}")
            metadata = BytesParser(policy=email.policy.default).parsebytes(
                archive.read(metadata_names[0])
            )
    except CC002Error:
        raise
    except (OSError, zipfile.BadZipFile, KeyError) as error:
        _fail("CC002_WHEEL", f"invalid wheel {path.name}: {error}")
    names = metadata.get_all("Name")
    versions = metadata.get_all("Version")
    if not isinstance(names, list) or len(names) != 1 or not isinstance(names[0], str) or not names[0].strip():
        _fail("CC002_WHEEL", f"wheel Name is required: {path.name}")
    if not isinstance(versions, list) or len(versions) != 1 or not isinstance(versions[0], str) or not versions[0].strip():
        _fail("CC002_WHEEL", f"wheel Version is required: {path.name}")
    name = names[0]
    version = versions[0]
    parts = path.name.removesuffix(".whl").split("-")
    if len(parts) < 5:
        _fail("CC002_WHEEL", f"malformed wheel filename: {path.name}")
    if _canonical_name(parts[0]) != _canonical_name(name) or parts[1] != version:
        _fail("CC002_WHEEL", f"wheel filename and METADATA disagree: {path.name}")
    return name, version


def build_lock(wheelhouse: Path) -> tuple[str, list[dict[str, Any]]]:
    """Build a deterministic one-wheel-per-distribution hash lock."""
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        _fail("CC002_WHEELHOUSE", f"wheelhouse must be a regular directory: {wheelhouse}")
    paths = sorted(wheelhouse.iterdir(), key=lambda path: path.name)
    if not paths:
        _fail("CC002_WHEELHOUSE", "wheelhouse is empty")
    if any(path.suffix != ".whl" for path in paths):
        _fail("CC002_WHEELHOUSE", "wheelhouse contains a non-wheel entry")
    by_name: dict[str, tuple[str, dict[str, Any]]] = {}
    for path in paths:
        name, version = _wheel_metadata(path)
        normalized = _canonical_name(name)
        if normalized in by_name:
            _fail("CC002_WHEELHOUSE", f"duplicate distribution in wheelhouse: {name}")
        record = _artifact_record(path)
        record.update({"distribution": name, "version": version})
        by_name[normalized] = (version, record)
    lines = []
    records = []
    for normalized, (version, record) in by_name.items():
        lines.append(f"{normalized}=={version} --hash={record['sha256']}")
        records.append(record)
    lines.sort(key=str.casefold)
    records.sort(key=lambda item: item["filename"])
    return "\n".join(lines) + "\n", records


_PIP_REPORT_ENVIRONMENT = {
    "implementation_name": "cpython",
    "implementation_version": "3.12.10",
    "python_full_version": "3.12.10",
    "python_version": "3.12",
    "platform_machine": "x86_64",
    "platform_system": "Linux",
}


def _validate_runtime_distribution_policy(
    wheel_records: Sequence[Mapping[str, Any]],
) -> None:
    forbidden = {"pytest", "pytest-logging", "py"}
    for record in wheel_records:
        name = _canonical_name(record["distribution"])
        if name in forbidden:
            _fail(
                "CC002_FORBIDDEN_RUNTIME",
                f"test-only distribution is forbidden from runtime closure: {name}",
            )
        filename = record["filename"]
        digest = record["sha256"]
        is_cfgraph = (
            name == "cfgraph"
            or filename.casefold().startswith(("cfgraph-", "cf_graph-"))
            or digest == "sha256:" + CFGRAPH_WHEEL_SHA256
        )
        if is_cfgraph and (
            record["distribution"] != "CFGraph"
            or record["version"] != "0.2.1"
            or filename != CFGRAPH_WHEEL_FILENAME
            or record["byte_length"] != CFGRAPH_WHEEL_BYTE_LENGTH
            or digest != "sha256:" + CFGRAPH_WHEEL_SHA256
        ):
            _fail(
                "CC002_CFGRAPH_RUNTIME",
                "runtime CFGraph must be the exact embedded provisional wheel",
            )
        if name == "prefixcommons" and (
            record["version"] != "0.1.12+malleus.1"
            or record["filename"] != PREFIXCOMMONS_DERIVED_FILENAME
        ):
            _fail(
                "CC002_PREFIXCOMMONS_RUNTIME",
                "runtime prefixcommons must be the exact governed derived wheel",
            )


def validate_resolution_report(
    report: Any, wheel_records: Sequence[Mapping[str, Any]]
) -> list[Mapping[str, Any]]:
    """Cross-check pip 25.0.1's selected-tuple resolution against retained wheels."""
    wheel_records = _validated_wheel_records(wheel_records)
    _validate_runtime_distribution_policy(wheel_records)
    if not isinstance(report, dict):
        _fail("CC002_PIP_REPORT", "pip report must be an object")
    _exact_keys(
        report,
        {"version", "pip_version", "install", "environment"},
        "pip report",
    )
    if report["version"] != "1" or report["pip_version"] != "25.0.1":
        _fail("CC002_PIP_REPORT", "pip report version or pip identity mismatch")
    environment = report["environment"]
    if not isinstance(environment, dict):
        _fail("CC002_PIP_REPORT", "pip report environment must be an object")
    for key, expected in _PIP_REPORT_ENVIRONMENT.items():
        if environment.get(key) != expected:
            _fail("CC002_PYTHON_TUPLE", f"pip report {key} != {expected!r}")
    records_by_identity: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    for record in wheel_records:
        distribution = record["distribution"]
        version = record["version"]
        digest = record["sha256"]
        identity = (_canonical_name(distribution), version, digest.removeprefix("sha256:"))
        if identity in records_by_identity:
            _fail("CC002_PIP_REPORT", f"duplicate wheel identity: {identity[0]}")
        if not (identity[0] == "pip" and version == "25.0.1"):
            records_by_identity[identity] = record
    installs = report["install"]
    if not isinstance(installs, list):
        _fail("CC002_PIP_REPORT", "pip report install must be an array")
    observed: dict[tuple[str, str, str], str] = {}
    for install in installs:
        if not isinstance(install, dict):
            _fail("CC002_PIP_REPORT", "pip install record must be an object")
        download = install.get("download_info")
        metadata = install.get("metadata")
        if not isinstance(download, dict) or not isinstance(metadata, dict):
            _fail("CC002_PIP_REPORT", "pip install download_info and metadata are required")
        name = metadata.get("name")
        version = metadata.get("version")
        if not isinstance(name, str) or not isinstance(version, str) or not name or not version:
            _fail("CC002_PIP_REPORT", "pip install name and version are required")
        url = download.get("url")
        if not isinstance(url, str):
            _fail("CC002_PIP_REPORT", "pip install URL is required")
        parsed = urllib.parse.urlsplit(url)
        path = PurePosixPath(urllib.parse.unquote(parsed.path))
        if (
            parsed.scheme != "file"
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or path.parent != PurePosixPath("/wheelhouse")
        ):
            _fail("CC002_PIP_REPORT", f"pip selected nonlocal wheel URL: {url}")
        archive = download.get("archive_info")
        if not isinstance(archive, dict):
            _fail("CC002_PIP_REPORT", "pip archive_info is required")
        hashes = archive.get("hashes")
        if not isinstance(hashes, dict) or set(hashes) != {"sha256"}:
            _fail("CC002_PIP_REPORT", "pip report must contain exactly one SHA-256")
        hexadecimal = hashes["sha256"]
        _validate_digest("sha256:" + str(hexadecimal), "pip report wheel")
        identity = (_canonical_name(name), version, str(hexadecimal))
        expected = records_by_identity.get(identity)
        if expected is None or expected["filename"] != path.name:
            _fail("CC002_PIP_REPORT", f"pip selected an unretained wheel: {path.name}")
        if identity in observed:
            _fail("CC002_PIP_REPORT", f"pip selected duplicate distribution: {name}")
        observed[identity] = path.name
    if set(observed) != set(records_by_identity):
        missing = sorted(set(records_by_identity) - set(observed))
        extra = sorted(set(observed) - set(records_by_identity))
        _fail("CC002_PIP_REPORT", f"pip closure mismatch; missing={missing}, extra={extra}")
    return list(wheel_records)


def _validate_installed_closure(
    distributions: Any, wheel_records: Sequence[Mapping[str, Any]]
) -> list[dict[str, str]]:
    wheel_records = _validated_wheel_records(wheel_records)
    _validate_runtime_distribution_policy(wheel_records)
    if not isinstance(distributions, list) or not distributions:
        _fail("CC002_VERIFY", "installed distribution closure is empty")
    observed: set[tuple[str, str]] = set()
    for distribution in distributions:
        if not isinstance(distribution, dict):
            _fail("CC002_VERIFY", "installed distribution must be an object")
        _exact_keys(distribution, {"name", "version"}, "installed distribution")
        if not all(
            isinstance(distribution[key], str) and distribution[key]
            for key in distribution
        ):
            _fail("CC002_VERIFY", "installed name and version must be nonempty strings")
        identity = (_canonical_name(distribution["name"]), distribution["version"])
        if identity in observed:
            _fail("CC002_VERIFY", f"duplicate installed distribution: {identity[0]}")
        observed.add(identity)
    expected = set()
    for record in wheel_records:
        name = record["distribution"]
        version = record["version"]
        expected.add((_canonical_name(name), version))
    if observed != expected:
        _fail(
            "CC002_VERIFY",
            f"installed closure mismatch; expected={sorted(expected)}, observed={sorted(observed)}",
        )
    return distributions


def _validate_internal_verification(
    value: Any,
    manifest: Mapping[str, Any],
    wheel_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("CC002_VERIFY", "internal verification must be an object")
    _exact_keys(
        value,
        {
            "schema",
            "workstream_id",
            "acquisition_manifest_sha256",
            "lock_sha256",
            "wheelhouse_sha256",
            "resolution_report_sha256",
            "source_build_record_sha256",
            "derivation_record_sha256",
            "docker",
            "oci_index_digest",
            "oci_child_digest",
            "platform",
            "network",
            "wheelhouse_mount",
            "python",
            "smoke_input",
            "generator_output_sha256",
            "installed_distributions",
        },
        "internal verification",
    )
    if value["schema"] != "malleus.cc002.internal-verification/v4":
        _fail("CC002_VERIFY", "unknown internal verification schema")
    if value["workstream_id"] != "CC-002":
        _fail("CC002_VERIFY", "internal verification workstream mismatch")
    for field in (
        "acquisition_manifest_sha256",
        "lock_sha256",
        "wheelhouse_sha256",
        "resolution_report_sha256",
        "source_build_record_sha256",
        "derivation_record_sha256",
        "generator_output_sha256",
    ):
        _validate_digest(value[field], field)
    fixed = {
        "lock_sha256": manifest["lock"]["sha256"],
        "wheelhouse_sha256": manifest["wheelhouse"]["sha256"],
        "resolution_report_sha256": manifest["resolution_report"]["sha256"],
        "source_build_record_sha256": manifest["build_record"]["sha256"],
        "derivation_record_sha256": manifest["derivation_record"]["sha256"],
        "docker": manifest["docker"],
        "oci_index_digest": OCI_INDEX_DIGEST,
        "oci_child_digest": OCI_CHILD_DIGEST,
        "platform": OCI_PLATFORM,
        "network": "DENIED",
        "wheelhouse_mount": "READ_ONLY",
        "python": PYTHON_TUPLE,
        "smoke_input": manifest["smoke_input"],
    }
    for field, expected in fixed.items():
        if value[field] != expected:
            _fail("CC002_VERIFY", f"internal verification {field} mismatch")
    _validate_installed_closure(value["installed_distributions"], wheel_records)
    return value


def verify_artifact_directory(directory: Path, manifest: Mapping[str, Any]) -> None:
    if directory.is_symlink() or not directory.is_dir():
        _fail("CC002_DIRECTORY", f"artifact directory is missing or unsafe: {directory}")
    _exact_keys(manifest, {"artifacts"}, "artifact manifest")
    records = manifest["artifacts"]
    if not isinstance(records, list):
        _fail("CC002_MANIFEST", "artifact records must be an array")
    expected: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            _fail("CC002_MANIFEST", "artifact record must be an object")
        _exact_keys(record, {"filename", "byte_length", "sha256"}, "artifact record")
        filename = record["filename"]
        if not isinstance(filename, str) or filename in expected:
            _fail("CC002_MANIFEST", f"invalid or duplicate artifact filename: {filename!r}")
        expected[filename] = record
    actual_names = {path.name for path in directory.iterdir()}
    missing = sorted(set(expected) - actual_names)
    unexpected = sorted(actual_names - set(expected))
    if missing:
        _fail("CC002_MISSING", f"missing artifacts: {missing}")
    if unexpected:
        _fail("CC002_UNEXPECTED", f"unexpected artifacts: {unexpected}")
    for filename, record in expected.items():
        path = safe_target(directory, filename)
        actual = _artifact_record(path)
        if actual["byte_length"] != record["byte_length"]:
            _fail("CC002_LENGTH", f"{filename}: byte length mismatch")
        if actual["sha256"] != record["sha256"]:
            _fail("CC002_DIGEST", f"{filename}: SHA-256 mismatch")


def _tree_identity(root: Path) -> str:
    if root.is_symlink() or not root.is_dir():
        _fail("CC002_DIRECTORY", f"unsafe directory: {root}")
    records = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        if path.is_symlink():
            _fail("CC002_SYMLINK", f"symlink in environment: {path}")
        if path.is_file():
            record = _artifact_record(path)
            record["filename"] = path.relative_to(root).as_posix()
            records.append(record)
        elif not path.is_dir():
            _fail("CC002_FILE", f"unsupported filesystem entry: {path}")
    return _digest(canonical_json(records).encode("utf-8"))


def _require_safe_ancestors(target: Path, trusted_root: Path) -> None:
    trusted = Path(os.path.abspath(trusted_root))
    lexical_target = Path(os.path.abspath(target))
    if trusted.is_symlink() or not trusted.is_dir():
        _fail("CC002_TRUSTED_ROOT", f"trusted root is missing or unsafe: {trusted}")
    try:
        relative = lexical_target.relative_to(trusted)
    except ValueError:
        _fail("CC002_TRUSTED_ROOT", f"output is outside the trusted root: {target}")
    if not relative.parts:
        _fail("CC002_TRUSTED_ROOT", "output cannot replace the trusted root")
    current = trusted
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            _fail("CC002_SYMLINK", f"symlink output ancestor is forbidden: {current}")
        if current.exists() and not current.is_dir():
            _fail("CC002_PATH", f"output ancestor is not a directory: {current}")
    try:
        lexical_target.parent.resolve().relative_to(trusted.resolve())
    except ValueError:
        _fail("CC002_TRUSTED_ROOT", f"output parent escapes the trusted root: {target}")


def publish_directory(staging: Path, destination: Path, trusted_root: Path) -> bool:
    """Publish a complete directory once, accepting only byte-identical reruns."""
    staging_identity = _tree_identity(staging)
    if destination.is_symlink():
        _fail("CC002_CONFLICT", "conflicting existing environment")
    _require_safe_ancestors(destination, trusted_root)
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() or not destination.is_dir():
            _fail("CC002_CONFLICT", "conflicting existing environment")
        if _tree_identity(destination) == staging_identity:
            return False
        _fail("CC002_CONFLICT", "conflicting existing environment")
    destination.parent.mkdir(parents=True, exist_ok=True)
    _require_safe_ancestors(destination, trusted_root)
    os.replace(staging, destination)
    return True


def _write_atomic(path: Path, source: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        _fail("CC002_SYMLINK", f"refusing symlink output: {path}")
    if path.exists():
        if path.is_file() and path.read_bytes() == source:
            return
        _fail("CC002_CONFLICT", f"conflicting existing output: {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(source)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists() and not temporary.is_symlink():
            temporary.unlink()


def _replace_atomic(
    path: Path, expected: bytes, replacement: bytes, trusted_root: Path
) -> None:
    _require_safe_ancestors(path, trusted_root)
    if path.is_symlink() or not path.is_file():
        _fail("CC002_CONFLICT", f"concurrent or unsafe output replacement: {path}")
    current = path.read_bytes()
    if current == replacement:
        return
    if current != expected:
        _fail("CC002_CONFLICT", f"concurrent or unsafe output replacement: {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        current = path.read_bytes()
        if current == replacement:
            return
        if current != expected:
            _fail("CC002_CONFLICT", f"output changed during replacement: {path}")
        os.replace(temporary, path)
    finally:
        if temporary.exists() and not temporary.is_symlink():
            temporary.unlink()


def _load_json_file(path: Path, context: str) -> tuple[dict[str, Any], bytes]:
    if path.is_symlink() or not path.is_file():
        _fail("CC002_FILE", f"required {context} is missing: {path}")
    source = path.read_bytes()
    value = strict_json(source, context)
    if not isinstance(value, dict):
        _fail("CC002_JSON", f"{context} root must be an object")
    return value, source


def _validated_wheel_record(value: Any) -> dict[str, Any]:
    _exact_keys(
        value,
        {"filename", "byte_length", "sha256", "distribution", "version"},
        "wheel record",
    )
    filename = value["filename"]
    byte_length = value["byte_length"]
    digest = value["sha256"]
    distribution = value["distribution"]
    version = value["version"]
    if (
        not isinstance(filename, str)
        or not filename
        or not filename.endswith(".whl")
        or "/" in filename
        or "\\" in filename
    ):
        _fail("CC002_WHEEL_RECORD", "wheel record filename must be a local wheel name")
    if (
        not isinstance(byte_length, int)
        or isinstance(byte_length, bool)
        or byte_length <= 0
    ):
        _fail("CC002_WHEEL_RECORD", "wheel record byte_length must be a positive integer")
    _validate_digest(digest, f"wheel record {filename} sha256")
    if not isinstance(distribution, str) or not distribution:
        _fail("CC002_WHEEL_RECORD", "wheel record distribution must be a nonempty string")
    if not isinstance(version, str) or not version:
        _fail("CC002_WHEEL_RECORD", "wheel record version must be a nonempty string")
    return {
        "filename": filename,
        "byte_length": byte_length,
        "sha256": digest,
        "distribution": distribution,
        "version": version,
    }


def _validated_wheel_records(records: Any) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        _fail("CC002_WHEEL_RECORD", "wheel records must be an array")
    return [_validated_wheel_record(record) for record in records]


def _wheelhouse_identity(records: Any) -> str:
    validated = _validated_wheel_records(records)
    return _digest(canonical_json(validated).encode("utf-8"))


def _content_record(record: Any) -> dict[str, Any]:
    record = _validated_wheel_record(record)
    return {
        "filename": record["filename"],
        "byte_length": record["byte_length"],
        "sha256": record["sha256"],
    }


def _manifest_from_staging(
    staging: Path,
    lock: bytes,
    wheel_records: list[dict[str, Any]],
    *,
    docker_client_version: str,
) -> dict[str, Any]:
    roots = [
        _artifact_record(staging / "roots" / item.filename)
        for item in SELECTED_ARTIFACTS
    ]
    roots.extend(
        _artifact_record(staging / "roots" / filename)
        for filename in EMBEDDED_ROOT_ARTIFACTS
    )
    build_inputs = [
        _artifact_record(staging / "build-inputs" / item.filename)
        for item in BUILD_ARTIFACTS
    ]
    derivative_inputs = [
        _artifact_record(staging / "derivative-inputs" / item.filename)
        for item in DERIVATIVE_INPUTS
    ]
    built = [
        _artifact_record(
            staging / "built" / "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
        ),
        _artifact_record(staging / "built" / PREFIXCOMMONS_DERIVED_FILENAME),
    ]
    smoke = _artifact_record(SMOKE_INPUT)
    smoke["filename"] = "ontology/malleus.yaml"
    return {
        "schema": "malleus.cc002.compiler-environment/v4",
        "docker": {
            "command": DOCKER,
            "client_version": docker_client_version,
            "transport": DOCKER_TRANSPORT,
        },
        "release": RELEASE,
        "python": PYTHON_TUPLE,
        "image": {
            "tag": "python:3.12.10-slim-bookworm",
            "platform": OCI_PLATFORM,
            "index_digest": OCI_INDEX_DIGEST,
            "child_digest": OCI_CHILD_DIGEST,
        },
        "roots": {"artifacts": roots},
        "build_inputs": {"artifacts": build_inputs},
        "derivative_inputs": {"artifacts": derivative_inputs},
        "built": {"artifacts": built},
        "build_record": _artifact_record(staging / "build-record.json"),
        "derivation_record": _artifact_record(staging / "derivation-record.json"),
        "wheelhouse": {
            "artifacts": wheel_records,
            "sha256": _wheelhouse_identity(wheel_records),
        },
        "lock": {
            "filename": "requirements.lock",
            "byte_length": len(lock),
            "sha256": _digest(lock),
        },
        "resolution_report": _artifact_record(staging / "resolution-report.json"),
        "verification": {"state": "PENDING"},
        "smoke_input": smoke,
    }


def _remove_recoverable_manifest_temps(path: Path) -> None:
    prefixes = (".manifest.json.", ".verification.json.")
    for member in path.iterdir():
        if not any(member.name.startswith(prefix) for prefix in prefixes):
            continue
        if member.is_symlink() or not member.is_file():
            _fail("CC002_SYMLINK", f"unsafe crash residue: {member}")
        member.unlink()


def _require_exact_bundle_members(path: Path, *, has_verification: bool) -> None:
    expected = {
        "manifest.json",
        "requirements.lock",
        "resolution-report.json",
        "roots",
        "build-inputs",
        "derivative-inputs",
        "built",
        "build-record.json",
        "derivation-record.json",
        "wheelhouse",
    }
    if has_verification:
        expected.add("verification.json")
    actual = {member.name for member in path.iterdir()}
    unexpected = sorted(actual - expected)
    missing = sorted(expected - actual)
    if missing or unexpected:
        _fail(
            "CC002_TOP_LEVEL",
            f"bundle top-level membership mismatch; missing={missing}, unexpected={unexpected}",
        )


def _pending_manifest_source(manifest: Mapping[str, Any]) -> bytes:
    pending = dict(manifest)
    pending["verification"] = {"state": "PENDING"}
    return (canonical_json(pending) + "\n").encode("utf-8")


def _bind_selected_wheels(
    path: Path,
    records: Sequence[Mapping[str, Any]],
    root_records: Sequence[Mapping[str, Any]],
) -> None:
    wheel_records = {record["filename"]: record for record in records}
    retained_roots = {record["filename"]: record for record in root_records}
    expected_metadata = {
        ROOT_WHEEL_FILENAMES[0]: ("linkml", "1.11.1"),
        ROOT_WHEEL_FILENAMES[1]: ("linkml-runtime", "1.11.1"),
        PIP_WHEEL_FILENAME: ("pip", "25.0.1"),
        CFGRAPH_WHEEL_FILENAME: ("CFGraph", "0.2.1"),
    }
    root_wheels = {
        artifact.filename: {
            "filename": artifact.filename,
            "byte_length": artifact.byte_length,
            "sha256": "sha256:" + artifact.sha256,
        }
        for artifact in SELECTED_ARTIFACTS
        if artifact.kind == "WHEEL"
    }
    root_wheels[CFGRAPH_WHEEL_FILENAME] = {
        "filename": CFGRAPH_WHEEL_FILENAME,
        "byte_length": CFGRAPH_WHEEL_BYTE_LENGTH,
        "sha256": "sha256:" + CFGRAPH_WHEEL_SHA256,
    }
    if set(root_wheels) != set(expected_metadata):
        _fail("CC002_SELECTED_WHEEL", "selected wheel root membership is invalid")
    embedded_record = validate_embedded_cfgraph_wheel(
        path / "roots" / CFGRAPH_WHEEL_FILENAME
    )
    for filename, expected_content in root_wheels.items():
        record = wheel_records.get(filename)
        root_record = retained_roots.get(filename)
        if record is None or root_record != expected_content:
            _fail(
                "CC002_SELECTED_WHEEL",
                f"selected wheel is missing from its retained root: {filename}",
            )
        if _content_record(record) != expected_content:
            _fail(
                "CC002_SELECTED_WHEEL",
                f"selected wheelhouse copy differs from retained root: {filename}",
            )
        distribution, version = expected_metadata[filename]
        if record.get("distribution") != distribution or record.get("version") != version:
            _fail(
                "CC002_SELECTED_WHEEL",
                f"selected wheel metadata is invalid: {filename}",
            )
        if filename == CFGRAPH_WHEEL_FILENAME and record != embedded_record:
            _fail(
                "CC002_CFGRAPH_BINDING",
                "embedded CFGraph wheel record differs from runtime wheel",
            )
        if (path / "roots" / filename).read_bytes() != (
            path / "wheelhouse" / filename
        ).read_bytes():
            _fail(
                "CC002_SELECTED_WHEEL",
                f"selected wheel bytes differ from retained root: {filename}",
            )


def _bind_built_wheel(
    path: Path,
    records: Sequence[Mapping[str, Any]],
    built_record: Mapping[str, Any],
) -> None:
    _exact_keys(built_record, {"filename", "byte_length", "sha256"}, "built wheel record")
    built_record = dict(built_record)
    _validate_digest(built_record["sha256"], "built wheel sha256")
    matching = [record for record in records if record.get("filename") == built_record["filename"]]
    if len(matching) != 1 or _content_record(matching[0]) != built_record:
        _fail("CC002_BUILT_BINDING", "built ANTLR wheel is not exactly bound into wheelhouse")
    built_path = path / "built" / built_record["filename"]
    runtime_path = path / "wheelhouse" / built_record["filename"]
    if (
        built_path.is_symlink()
        or runtime_path.is_symlink()
        or not built_path.is_file()
        or not runtime_path.is_file()
        or built_path.read_bytes() != runtime_path.read_bytes()
    ):
        _fail("CC002_BUILT_BINDING", "built and runtime ANTLR wheel bytes differ")


def _validate_derivation_record(
    path: Path,
    manifest: Mapping[str, Any],
    retained_output: Mapping[str, Any],
) -> dict[str, Any]:
    identity = manifest["derivation_record"]
    if _artifact_record(path / "derivation-record.json") != identity:
        _fail("CC002_DERIVATION_RECORD", "derivation record byte identity mismatch")
    value, _source = _load_json_file(
        path / "derivation-record.json",
        "prefixcommons derivation record",
    )
    try:
        _exact_keys(
            value,
            {
                "schema",
                "input",
                "runs",
                "outputs",
                "byte_equal",
                "retained_output",
                "license",
                "tool",
            },
            "prefixcommons derivation record",
        )
    except CC002Error as error:
        _fail("CC002_DERIVATION_RECORD", str(error))
    output = _content_record(retained_output)
    expected_run = {**RETAINED_DERIVATION_RUN, "output": output}
    expected_license = {
        "upstream_member": "prefixcommons-0.1.12.dist-info/LICENSE",
        "derived_member": "prefixcommons-0.1.12+malleus.1.dist-info/LICENSE",
        "byte_length": PREFIXCOMMONS_LICENSE_BYTE_LENGTH,
        "sha256": "sha256:" + PREFIXCOMMONS_LICENSE_SHA256,
    }
    if (
        value["schema"] != "malleus.cc002.wheel-derivation/v1"
        or value["input"] != manifest["derivative_inputs"]["artifacts"][0]
        or value["runs"] != [expected_run, expected_run]
        or value["outputs"] != [output, output]
        or value["byte_equal"] is not True
        or value["retained_output"] != output
        or value["license"] != expected_license
        or value["tool"] != EXPECTED_DERIVATION_CHILD_FACTS["tool"]
    ):
        _fail(
            "CC002_DERIVATION_RECORD",
            "derivation record does not bind the governed transformation",
        )
    return value


def _bind_derived_prefixcommons(
    path: Path,
    records: Sequence[Mapping[str, Any]],
    built_record: Mapping[str, Any],
    upstream_path: Path,
) -> None:
    matching = [
        record
        for record in records
        if record.get("filename") == PREFIXCOMMONS_DERIVED_FILENAME
    ]
    if len(matching) != 1 or _content_record(matching[0]) != built_record:
        _fail(
            "CC002_DERIVATION_BINDING",
            "derived prefixcommons wheel is not exactly bound into wheelhouse",
        )
    built_path = path / "built" / PREFIXCOMMONS_DERIVED_FILENAME
    runtime_path = path / "wheelhouse" / PREFIXCOMMONS_DERIVED_FILENAME
    if built_path.read_bytes() != runtime_path.read_bytes():
        _fail(
            "CC002_DERIVATION_BINDING",
            "built and runtime prefixcommons wheel bytes differ",
        )
    _validate_prefixcommons_derivation(upstream_path, runtime_path)


def _validated_environment(path: Path | None = None) -> tuple[dict[str, Any], bytes]:
    path = DESTINATION if path is None else path
    if path.is_symlink() or not path.is_dir():
        _fail("CC002_DIRECTORY", f"environment must be a regular directory: {path}")
    _remove_recoverable_manifest_temps(path)
    manifest, source = _load_json_file(path / "manifest.json", "environment manifest")
    _exact_keys(
        manifest,
        {
            "schema",
            "docker",
            "release",
            "python",
            "image",
            "roots",
            "build_inputs",
            "derivative_inputs",
            "built",
            "build_record",
            "derivation_record",
            "wheelhouse",
            "lock",
            "resolution_report",
            "verification",
            "smoke_input",
        },
        "environment manifest",
    )
    if manifest["schema"] != "malleus.cc002.compiler-environment/v4":
        _fail("CC002_MANIFEST", "unknown environment schema")
    docker = manifest["docker"]
    if not isinstance(docker, dict):
        _fail("CC002_MANIFEST", "Docker execution identity must be an object")
    _exact_keys(
        docker,
        {"command", "client_version", "transport"},
        "Docker identity",
    )
    if docker["command"] != DOCKER or docker["transport"] != DOCKER_TRANSPORT:
        _fail("CC002_MANIFEST", "Docker command identity mismatch")
    if not all(
        isinstance(docker[key], str) and docker[key]
        for key in ("command", "client_version", "transport")
    ):
        _fail("CC002_MANIFEST", "Docker execution identity fields must be nonempty strings")
    if manifest["release"] != RELEASE or manifest["python"] != PYTHON_TUPLE:
        _fail("CC002_MANIFEST", "environment baseline does not match OD-012")
    if manifest["image"] != {
        "tag": "python:3.12.10-slim-bookworm",
        "platform": OCI_PLATFORM,
        "index_digest": OCI_INDEX_DIGEST,
        "child_digest": OCI_CHILD_DIGEST,
    }:
        _fail("CC002_MANIFEST", "environment image does not match OD-012")
    verify_artifact_directory(path / "roots", manifest["roots"])
    verify_artifact_directory(path / "build-inputs", manifest["build_inputs"])
    verify_artifact_directory(
        path / "derivative-inputs",
        manifest["derivative_inputs"],
    )
    verify_artifact_directory(path / "built", manifest["built"])
    expected_build_inputs = {
        item.filename: {
            "filename": item.filename,
            "byte_length": item.byte_length,
            "sha256": "sha256:" + item.sha256,
        }
        for item in BUILD_ARTIFACTS
    }
    if {item["filename"]: item for item in manifest["build_inputs"]["artifacts"]} != expected_build_inputs:
        _fail("CC002_BUILD_INPUT", "retained build inputs do not match authorization")
    derivative_records = manifest["derivative_inputs"]["artifacts"]
    if len(derivative_records) != 1:
        _fail(
            "CC002_PREFIXCOMMONS_INPUT",
            "retained derivative input set must contain exactly one wheel",
        )
    upstream_path = path / "derivative-inputs" / PREFIXCOMMONS_INPUT_FILENAME
    upstream_record = validate_prefixcommons_input(upstream_path)
    if derivative_records[0] != upstream_record:
        _fail(
            "CC002_PREFIXCOMMONS_INPUT",
            "retained derivative input identity mismatch",
        )
    built_records = manifest["built"]["artifacts"]
    built_by_name = {record["filename"]: record for record in built_records}
    antlr_filename = "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    if set(built_by_name) != {antlr_filename, PREFIXCOMMONS_DERIVED_FILENAME}:
        _fail("CC002_BUILT_WHEEL", "retained built set must contain two exact wheels")
    built_record = validate_built_antlr_wheel(path / "built" / antlr_filename)
    if _content_record(built_record) != built_by_name[antlr_filename]:
        _fail("CC002_BUILT_WHEEL", "retained built wheel identity mismatch")
    derived_record = _validate_prefixcommons_derivation(
        upstream_path,
        path / "built" / PREFIXCOMMONS_DERIVED_FILENAME,
    )
    if _content_record(derived_record) != built_by_name[PREFIXCOMMONS_DERIVED_FILENAME]:
        _fail("CC002_DERIVATION_IDENTITY", "retained derived wheel identity mismatch")
    _validate_derivation_record(path, manifest, derived_record)
    build_record_identity = manifest["build_record"]
    if _artifact_record(path / "build-record.json") != build_record_identity:
        _fail("CC002_BUILD_RECORD", "build record byte identity mismatch")
    build_record, _build_record_source = _load_json_file(path / "build-record.json", "source build record")
    _exact_keys(build_record, {"schema", "source_date_epoch", "python", "image", "frontend", "backend", "backend_interface", "post_build", "isolation", "environment", "inputs", "sdist", "runs", "builds", "byte_equal", "retained_output"}, "source build record")
    expected_output = _content_record(built_record)
    if (
        build_record["schema"] != "malleus.cc002.source-build/v1"
        or build_record["source_date_epoch"] != 315532800
        or build_record["python"] != PYTHON_TUPLE
        or build_record["image"] != {"platform": OCI_PLATFORM, "child_digest": OCI_CHILD_DIGEST}
        or build_record["frontend"] != {"distribution": "pip", "version": "25.0.1", "origin": PIP_WHEEL_FILENAME}
        or build_record["backend"] != {"distribution": "setuptools", "version": "83.0.0", "origin": SETUPTOOLS_WHEEL_FILENAME}
        or build_record["backend_interface"] != "setuptools.build_meta:__legacy__"
        or build_record["post_build"] != {"wheel_generator": "setuptools (83.0.0)"}
        or build_record["isolation"] != {"build_count": 2, "network": "NONE", "read_only_root": True, "nonroot": True}
        or build_record["environment"] != {"source_date_epoch": 315532800, "tz": "UTC", "python_hash_seed": "0", "umask": "022", "no_build_isolation": True}
        or build_record["inputs"] != manifest["build_inputs"]["artifacts"]
        or build_record["sdist"] != {"member_count": ANTLR_SDIST_MEMBER_COUNT, "uncompressed_byte_length": ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH}
        or build_record["runs"] != [RETAINED_BUILD_RUN, RETAINED_BUILD_RUN]
        or build_record["builds"] != [expected_output, expected_output]
        or build_record["byte_equal"] is not True
        or build_record["retained_output"] != expected_output
    ):
        _fail("CC002_BUILD_RECORD", "source build record does not bind the governed build")
    wheelhouse = manifest["wheelhouse"]
    if not isinstance(wheelhouse, dict):
        _fail("CC002_MANIFEST", "wheelhouse manifest must be an object")
    _exact_keys(wheelhouse, {"artifacts", "sha256"}, "wheelhouse manifest")
    records = wheelhouse["artifacts"]
    records = _validated_wheel_records(records)
    verify_artifact_directory(
        path / "wheelhouse", {"artifacts": [_content_record(record) for record in records]}
    )
    if wheelhouse["sha256"] != _wheelhouse_identity(wheelhouse["artifacts"]):
        _fail("CC002_MANIFEST", "wheelhouse identity mismatch")
    rebuilt_lock, rebuilt_records = build_lock(path / "wheelhouse")
    if rebuilt_records != records:
        _fail("CC002_MANIFEST", "wheelhouse metadata does not match retained wheel bytes")
    lock = manifest["lock"]
    if not isinstance(lock, dict):
        _fail("CC002_MANIFEST", "lock manifest must be an object")
    _exact_keys(lock, {"filename", "byte_length", "sha256"}, "lock manifest")
    if lock["filename"] != "requirements.lock":
        _fail("CC002_MANIFEST", "lock filename mismatch")
    lock_record = _artifact_record(path / "requirements.lock")
    if lock_record != lock:
        _fail("CC002_MANIFEST", "lock byte identity mismatch")
    if (path / "requirements.lock").read_text(encoding="utf-8") != rebuilt_lock:
        _fail("CC002_MANIFEST", "requirements lock does not match retained wheel bytes")
    resolution_record = manifest["resolution_report"]
    if not isinstance(resolution_record, dict):
        _fail("CC002_MANIFEST", "resolution report identity must be an object")
    _exact_keys(
        resolution_record,
        {"filename", "byte_length", "sha256"},
        "resolution report identity",
    )
    if resolution_record["filename"] != "resolution-report.json":
        _fail("CC002_MANIFEST", "resolution report filename mismatch")
    if _artifact_record(path / "resolution-report.json") != resolution_record:
        _fail("CC002_MANIFEST", "resolution report byte identity mismatch")
    resolution, _resolution_source = _load_json_file(
        path / "resolution-report.json", "pip resolution report"
    )
    validate_resolution_report(resolution, rebuilt_records)
    expected_roots = {
        artifact.filename: {
            "filename": artifact.filename,
            "byte_length": artifact.byte_length,
            "sha256": "sha256:" + artifact.sha256,
        }
        for artifact in SELECTED_ARTIFACTS
    }
    expected_roots[CFGRAPH_WHEEL_FILENAME] = {
        "filename": CFGRAPH_WHEEL_FILENAME,
        "byte_length": CFGRAPH_WHEEL_BYTE_LENGTH,
        "sha256": "sha256:" + CFGRAPH_WHEEL_SHA256,
    }
    for record in manifest["roots"]["artifacts"]:
        selected = expected_roots.get(record["filename"])
        if selected is None:
            _fail("CC002_MANIFEST", "root retention membership mismatch")
        if record != selected:
            _fail(
                "CC002_MANIFEST",
                f"selected root identity mismatch: {record['filename']}",
            )
    if len(manifest["roots"]["artifacts"]) != len(expected_roots):
        _fail("CC002_MANIFEST", "root retention count mismatch")
    if len(manifest["roots"]["artifacts"]) != 6:
        _fail(
            "CC002_MANIFEST", "root retention set must contain exactly six artifacts"
        )
    _bind_selected_wheels(path, rebuilt_records, manifest["roots"]["artifacts"])
    _bind_built_wheel(path, rebuilt_records, built_by_name[antlr_filename])
    _bind_derived_prefixcommons(
        path,
        rebuilt_records,
        built_by_name[PREFIXCOMMONS_DERIVED_FILENAME],
        upstream_path,
    )
    verification = manifest["verification"]
    if not isinstance(verification, dict):
        _fail("CC002_MANIFEST", "verification state must be an object")
    if verification == {"state": "PENDING"}:
        verification_path = path / "verification.json"
        if verification_path.is_symlink():
            _fail("CC002_SYMLINK", "internal verification cannot be a symlink")
        if verification_path.exists():
            internal, _internal_source = _load_json_file(
                verification_path, "recoverable internal offline verification"
            )
            _validate_internal_verification(internal, manifest, rebuilt_records)
            if internal["acquisition_manifest_sha256"] != _digest(
                _pending_manifest_source(manifest)
            ):
                _fail(
                    "CC002_VERIFY",
                    "recoverable verification lineage does not bind the pending manifest",
                )
    else:
        _exact_keys(
            verification,
            {"state", "filename", "byte_length", "sha256"},
            "verification identity",
        )
        if verification["state"] != "COMPLETE" or verification["filename"] != "verification.json":
            _fail("CC002_MANIFEST", "completed verification identity is invalid")
        if _artifact_record(path / "verification.json") != {
            key: verification[key] for key in ("filename", "byte_length", "sha256")
        }:
            _fail("CC002_MANIFEST", "verification byte identity mismatch")
        internal, _internal_source = _load_json_file(
            path / "verification.json", "internal offline verification"
        )
        _validate_internal_verification(internal, manifest, rebuilt_records)
        if internal["acquisition_manifest_sha256"] != _digest(
            _pending_manifest_source(manifest)
        ):
            _fail(
                "CC002_VERIFY",
                "completed verification lineage does not bind the pending manifest",
            )
    _require_exact_bundle_members(
        path, has_verification=(path / "verification.json").exists()
    )
    smoke = _artifact_record(SMOKE_INPUT)
    smoke["filename"] = "ontology/malleus.yaml"
    if manifest["smoke_input"] != smoke:
        _fail("CC002_MANIFEST", "generic smoke input changed")
    return manifest, source


def _materialize_embedded_roots(roots: Path, wheelhouse: Path) -> None:
    if EMBEDDED_ROOT_ARTIFACTS != {
        CFGRAPH_WHEEL_FILENAME: CFGRAPH_WHEEL_BYTES
    }:
        _fail("CC002_CFGRAPH_EMBED", "embedded root inventory changed")
    root = safe_target(roots, CFGRAPH_WHEEL_FILENAME)
    _write_atomic(root, CFGRAPH_WHEEL_BYTES)
    record = validate_embedded_cfgraph_wheel(root)
    runtime = safe_target(wheelhouse, CFGRAPH_WHEEL_FILENAME)
    _write_atomic(runtime, root.read_bytes())
    if (
        _artifact_record(runtime) != _content_record(record)
        or runtime.read_bytes() != root.read_bytes()
    ):
        _fail(
            "CC002_CFGRAPH_COPY",
            "embedded CFGraph root and runtime wheel bytes differ",
        )


def _copy_selected_wheels(roots: Path, wheelhouse: Path) -> None:
    if wheelhouse.is_symlink() or not wheelhouse.is_dir():
        _fail("CC002_WHEELHOUSE", "runtime wheelhouse is missing or unsafe")
    for filename in (*ROOT_WHEEL_FILENAMES, PIP_WHEEL_FILENAME):
        source = safe_target(roots, filename)
        target = safe_target(wheelhouse, filename)
        shutil.copyfile(source, target, follow_symlinks=False)


def acquire_environment() -> dict[str, Any]:
    """Materialize the fixed compiler environment, or attest an identical rerun."""
    require_repository_cwd()
    _require_safe_ancestors(DESTINATION, OUTPUT_TRUSTED_ROOT)
    if DESTINATION.is_symlink():
        _fail("CC002_SYMLINK", f"environment destination is a symlink: {DESTINATION}")
    if DESTINATION.exists():
        manifest, _source = _validated_environment()
        return acquire_result(
            artifact_count=(
                len(manifest["roots"]["artifacts"])
                + len(manifest["build_inputs"]["artifacts"])
                + len(manifest["derivative_inputs"]["artifacts"])
            ),
            built_artifact_count=len(manifest["built"]["artifacts"]),
            source_build_record_sha256=manifest["build_record"]["sha256"],
            derivation_record_sha256=manifest["derivation_record"]["sha256"],
            lock_sha256=manifest["lock"]["sha256"],
            wheel_count=len(manifest["wheelhouse"]["artifacts"]),
            wheelhouse_sha256=manifest["wheelhouse"]["sha256"],
        )
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".cc002-environment-", dir=DESTINATION.parent
    ) as temporary_name:
        staging = Path(temporary_name)
        roots = staging / "roots"
        roots.mkdir()
        wheelhouse = staging / "wheelhouse"
        wheelhouse.mkdir()
        _materialize_embedded_roots(roots, wheelhouse)
        build_inputs = staging / "build-inputs"
        build_inputs.mkdir()
        derivative_inputs = staging / "derivative-inputs"
        derivative_inputs.mkdir()
        opener = _default_opener()
        for artifact in SELECTED_ARTIFACTS:
            download_artifact(artifact, safe_target(roots, artifact.filename), opener)
        for artifact in BUILD_ARTIFACTS:
            download_artifact(
                artifact, safe_target(build_inputs, artifact.filename), opener
            )
        for artifact in DERIVATIVE_INPUTS:
            download_artifact(
                artifact,
                safe_target(derivative_inputs, artifact.filename),
                opener,
            )
        sdist_facts = validate_antlr_sdist(build_inputs / ANTLR_SDIST_FILENAME)
        validate_setuptools_wheel(build_inputs / SETUPTOOLS_WHEEL_FILENAME)
        upstream_path = derivative_inputs / PREFIXCOMMONS_INPUT_FILENAME
        upstream_record = validate_prefixcommons_input(upstream_path)
        docker_executable = _resolved_docker()
        docker_version = _docker_version(
            _run_checked(
                docker_version_command(),
                "Docker version",
                staging,
                docker_executable=docker_executable,
            )
        )
        raw_index = _fetch_selected_oci_index(opener)
        parse_oci_index(raw_index)
        _run_checked(
            image_pull_command(),
            "OCI child pull",
            staging,
            docker_executable=docker_executable,
        )
        _verify_local_image(
            _run_checked(
                image_inspect_command(),
                "local image inspection",
                staging,
                docker_executable=docker_executable,
            )
        )
        ownership = host_ownership()
        build_outputs = []
        for ordinal in (1, 2):
            output = staging / f".build-{ordinal}"
            output.mkdir()
            _run_checked(
                build_command(build_inputs, roots, output, host_user=ownership),
                f"network-denied ANTLR source build {ordinal}",
                staging,
                docker_executable=docker_executable,
            )
            build_outputs.append(output)
        built_wheel_record = validate_build_outputs(*build_outputs)
        child_facts = [
            retained_build_run(_load_json_file(output / ".cc002-build-facts.json", "source build child facts")[0])
            for output in build_outputs
        ]
        built = staging / "built"
        built.mkdir()
        built_path = built / built_wheel_record["filename"]
        shutil.copyfile(build_outputs[0] / built_wheel_record["filename"], built_path, follow_symlinks=False)
        if validate_built_antlr_wheel(built_path) != built_wheel_record:
            _fail(
                "CC002_BUILD_TOCTOU", "retained built wheel changed during publication"
            )
        derivation_outputs = []
        for ordinal in (1, 2):
            output = staging / f".derive-{ordinal}"
            output.mkdir()
            _run_checked(
                derivation_command(
                    derivative_inputs,
                    output,
                    host_user=ownership,
                ),
                f"network-denied prefixcommons derivation {ordinal}",
                staging,
                docker_executable=docker_executable,
            )
            derivation_outputs.append(output)
        derived_wheel_record = validate_derivation_outputs(*derivation_outputs)
        derived_content = _content_record(derived_wheel_record)
        derived_path = built / PREFIXCOMMONS_DERIVED_FILENAME
        shutil.copyfile(
            derivation_outputs[0] / PREFIXCOMMONS_DERIVED_FILENAME,
            derived_path,
            follow_symlinks=False,
        )
        if (
            _validate_prefixcommons_derivation(upstream_path, derived_path)
            != derived_wheel_record
        ):
            _fail(
                "CC002_DERIVATION_TOCTOU",
                "retained derived wheel changed during publication",
            )
        for output in build_outputs:
            shutil.rmtree(output)
        for output in derivation_outputs:
            shutil.rmtree(output)
        build_input_records = [
            _artifact_record(build_inputs / item.filename) for item in BUILD_ARTIFACTS
        ]
        output_content = _content_record(built_wheel_record)
        build_record = {
            "schema": "malleus.cc002.source-build/v1",
            "source_date_epoch": int(SOURCE_DATE_EPOCH),
            "python": PYTHON_TUPLE,
            "image": {"platform": OCI_PLATFORM, "child_digest": OCI_CHILD_DIGEST},
            "frontend": {"distribution": "pip", "version": "25.0.1", "origin": PIP_WHEEL_FILENAME},
            "backend": {"distribution": "setuptools", "version": "83.0.0", "origin": SETUPTOOLS_WHEEL_FILENAME},
            "backend_interface": "setuptools.build_meta:__legacy__",
            "post_build": {"wheel_generator": "setuptools (83.0.0)"},
            "isolation": {"build_count": 2, "network": "NONE", "read_only_root": True, "nonroot": True},
            "environment": {"source_date_epoch": 315532800, "tz": "UTC", "python_hash_seed": "0", "umask": "022", "no_build_isolation": True},
            "inputs": build_input_records,
            "sdist": sdist_facts,
            "runs": child_facts,
            "builds": [output_content, output_content],
            "byte_equal": True,
            "retained_output": output_content,
        }
        _write_atomic(
            staging / "build-record.json",
            (canonical_json(build_record) + "\n").encode("utf-8"),
        )
        derivation_record = {
            "schema": "malleus.cc002.wheel-derivation/v1",
            "input": upstream_record,
            "runs": [
                {**RETAINED_DERIVATION_RUN, "output": derived_content},
                {**RETAINED_DERIVATION_RUN, "output": derived_content},
            ],
            "outputs": [derived_content, derived_content],
            "byte_equal": True,
            "retained_output": derived_content,
            "license": {
                "upstream_member": "prefixcommons-0.1.12.dist-info/LICENSE",
                "derived_member": "prefixcommons-0.1.12+malleus.1.dist-info/LICENSE",
                "byte_length": PREFIXCOMMONS_LICENSE_BYTE_LENGTH,
                "sha256": "sha256:" + PREFIXCOMMONS_LICENSE_SHA256,
            },
            "tool": EXPECTED_DERIVATION_CHILD_FACTS["tool"],
        }
        _write_atomic(
            staging / "derivation-record.json",
            (canonical_json(derivation_record) + "\n").encode("utf-8"),
        )
        _copy_selected_wheels(roots, wheelhouse)
        shutil.copyfile(built_path, wheelhouse / built_path.name, follow_symlinks=False)
        shutil.copyfile(
            derived_path,
            wheelhouse / derived_path.name,
            follow_symlinks=False,
        )
        _run_checked(
            resolve_command(roots, wheelhouse, built=built, host_user=ownership),
            "transitive wheel resolution",
            staging,
            docker_executable=docker_executable,
        )
        lock_text, wheel_records = build_lock(wheelhouse)
        lock = lock_text.encode("utf-8")
        _write_atomic(staging / "requirements.lock", lock)
        with tempfile.TemporaryDirectory(
            prefix=".cc002-resolution-", dir=DESTINATION.parent
        ) as report_name:
            report_work = Path(report_name)
            _run_checked(
                lock_report_command(staging, report_work, host_user=ownership),
                "offline root resolution report",
                report_work,
                docker_executable=docker_executable,
            )
            report, _report_source = _load_json_file(
                report_work / "pip-report.json", "pip resolution report"
            )
            validate_resolution_report(report, wheel_records)
            _write_atomic(
                staging / "resolution-report.json",
                (canonical_json(report) + "\n").encode("utf-8"),
            )
        manifest = _manifest_from_staging(
            staging,
            lock,
            wheel_records,
            docker_client_version=docker_version,
        )
        _write_atomic(
            staging / "manifest.json",
            (canonical_json(manifest) + "\n").encode("utf-8"),
        )
        manifest, _source = _validated_environment(staging)
        publish_directory(staging, DESTINATION, OUTPUT_TRUSTED_ROOT)
    manifest, _source = _validated_environment()
    return acquire_result(
        artifact_count=(
            len(manifest["roots"]["artifacts"])
            + len(manifest["build_inputs"]["artifacts"])
            + len(manifest["derivative_inputs"]["artifacts"])
        ),
        built_artifact_count=len(manifest["built"]["artifacts"]),
        source_build_record_sha256=manifest["build_record"]["sha256"],
        derivation_record_sha256=manifest["derivation_record"]["sha256"],
        lock_sha256=manifest["lock"]["sha256"],
        wheel_count=len(manifest["wheelhouse"]["artifacts"]),
        wheelhouse_sha256=manifest["wheelhouse"]["sha256"],
    )


def _validate_container_result(
    work: Path, wheel_records: Sequence[Mapping[str, Any]]
) -> tuple[list[dict[str, str]], str]:
    result, _source = _load_json_file(work / "result.json", "container verification result")
    _exact_keys(
        result,
        {"schema", "installed_distributions", "generator_output", "python"},
        "container verification result",
    )
    if result["schema"] != "malleus.cc002.container-verification/v1":
        _fail("CC002_VERIFY", "unknown container verification schema")
    if result["generator_output"] != "/work/malleus.schema.json":
        _fail("CC002_VERIFY", "unexpected generator output path")
    if result["python"] != PYTHON_TUPLE:
        _fail("CC002_PYTHON_TUPLE", "offline verifier Python tuple mismatch")
    distributions = _validate_installed_closure(
        result["installed_distributions"], wheel_records
    )
    generator_source = (work / "malleus.schema.json").read_bytes()
    generated = strict_json(generator_source, "generated JSON Schema")
    if not isinstance(generated, dict) or not isinstance(generated.get("$defs"), dict):
        _fail("CC002_VERIFY", "generated JSON Schema lacks $defs")
    return distributions, _digest(generator_source)


def _completed_verification_result(
    manifest: Mapping[str, Any],
    manifest_source: bytes,
    internal: Mapping[str, Any],
    internal_source: bytes,
) -> dict[str, Any]:
    return verify_result(
        environment_manifest_sha256=_digest(manifest_source),
        verification_sha256=_digest(internal_source),
        generator_output_sha256=internal["generator_output_sha256"],
        installed_distribution_count=len(internal["installed_distributions"]),
        lock_sha256=manifest["lock"]["sha256"],
        wheelhouse_sha256=manifest["wheelhouse"]["sha256"],
        source_build_record_sha256=manifest["build_record"]["sha256"],
        derivation_record_sha256=manifest["derivation_record"]["sha256"],
    )


def verify_environment() -> dict[str, Any]:
    """Prove the retained environment installs and generates with network denied."""
    require_repository_cwd()
    _require_safe_ancestors(DESTINATION, OUTPUT_TRUSTED_ROOT)
    manifest, manifest_source = _validated_environment()
    verification_path = DESTINATION / "verification.json"
    if INTERNAL_VERIFICATION != verification_path:
        _fail("CC002_PATH", "internal verification path is not the fixed destination")
    if manifest["verification"].get("state") == "COMPLETE":
        internal, internal_source = _load_json_file(
            verification_path, "internal offline verification"
        )
        return _completed_verification_result(
            manifest, manifest_source, internal, internal_source
        )
    if verification_path.exists():
        internal, internal_source = _load_json_file(
            verification_path, "recoverable internal offline verification"
        )
    else:
        ownership = host_ownership()
        with tempfile.TemporaryDirectory(
            prefix=".cc002-verification-", dir=DESTINATION.parent
        ) as temporary_name:
            work = Path(temporary_name)
            docker_executable = _resolved_docker()
            docker_version = _docker_version(
                _run_checked(
                    docker_version_command(),
                    "Docker version",
                    work,
                    docker_executable=docker_executable,
                )
            )
            if docker_version != manifest["docker"]["client_version"]:
                _fail(
                    "CC002_DOCKER_VERSION",
                    "Docker client version changed after acquisition",
                )
            _verify_local_image(
                _run_checked(
                    image_inspect_command(),
                    "local image inspection",
                    work,
                    docker_executable=docker_executable,
                )
            )
            _run_checked(
                verify_command(DESTINATION, work, host_user=ownership),
                "offline container verification",
                work,
                docker_executable=docker_executable,
            )
            distributions, generator_digest = _validate_container_result(
                work, manifest["wheelhouse"]["artifacts"]
            )
        internal = {
            "schema": "malleus.cc002.internal-verification/v4",
            "workstream_id": "CC-002",
            "acquisition_manifest_sha256": _digest(manifest_source),
            "lock_sha256": manifest["lock"]["sha256"],
            "wheelhouse_sha256": manifest["wheelhouse"]["sha256"],
            "resolution_report_sha256": manifest["resolution_report"]["sha256"],
            "source_build_record_sha256": manifest["build_record"]["sha256"],
            "derivation_record_sha256": manifest["derivation_record"]["sha256"],
            "docker": manifest["docker"],
            "oci_index_digest": OCI_INDEX_DIGEST,
            "oci_child_digest": OCI_CHILD_DIGEST,
            "platform": OCI_PLATFORM,
            "network": "DENIED",
            "wheelhouse_mount": "READ_ONLY",
            "python": PYTHON_TUPLE,
            "smoke_input": manifest["smoke_input"],
            "generator_output_sha256": generator_digest,
            "installed_distributions": distributions,
        }
        _validate_internal_verification(
            internal, manifest, manifest["wheelhouse"]["artifacts"]
        )
        internal_source = (canonical_json(internal) + "\n").encode("utf-8")
        _write_atomic(verification_path, internal_source)
    completed = dict(manifest)
    record = _artifact_record(verification_path)
    completed["verification"] = {"state": "COMPLETE", **record}
    completed_source = (canonical_json(completed) + "\n").encode("utf-8")
    _replace_atomic(
        DESTINATION / "manifest.json",
        manifest_source,
        completed_source,
        OUTPUT_TRUSTED_ROOT,
    )
    completed, completed_source = _validated_environment()
    internal, internal_source = _load_json_file(
        verification_path, "internal offline verification"
    )
    return _completed_verification_result(
        completed, completed_source, internal, internal_source
    )


def main(arguments: Sequence[str] | None = None) -> int:
    arguments = sys.argv[1:] if arguments is None else list(arguments)
    if arguments != ["serve"]:
        sys.stderr.write("usage: contract_compiler_environment.py serve\n")
        return 2
    try:
        require_repository_cwd()
        serve()
    except CC002Error as error:
        sys.stderr.write(str(error) + "\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
