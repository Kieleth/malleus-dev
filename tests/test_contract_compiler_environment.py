"""CC-002 compiler-environment MCP and offline materialization gates."""

from __future__ import annotations

import ast
import base64
import builtins
import csv
import hashlib
import io
import json
import os
import pathlib
import platform
import shutil
import stat
import struct
import subprocess
import sys
import sysconfig
import tarfile
import tomllib
import types
import venv
import warnings
import zipfile
import zlib
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import scripts.contract_compiler_environment as environment  # noqa: E402


CONFIG = ROOT / ".codex" / "config.toml"
MACHINE_CONFIG_EXAMPLE = ROOT / ".codex" / "cc002.user.example.toml"
MCP_SETUP = ROOT / ".codex" / "README.md"
MAINTAINER_SKILL = ROOT / ".claude" / "skills" / "malleus-dev" / "SKILL.md"


class FakeServices:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def acquire(self) -> dict[str, Any]:
        self.calls.append("acquire")
        return environment.acquire_result(
            artifact_count=9,
            built_artifact_count=2,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "7" * 64,
            lock_sha256="sha256:" + "1" * 64,
            wheel_count=23,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )

    def verify(self) -> dict[str, Any]:
        self.calls.append("verify")
        return environment.verify_result(
            environment_manifest_sha256="sha256:" + "3" * 64,
            verification_sha256="sha256:" + "4" * 64,
            generator_output_sha256="sha256:" + "5" * 64,
            installed_distribution_count=23,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "7" * 64,
        )


def _request(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    request_id: int | str = 1,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }
    if params is not None:
        value["params"] = params
    return value


def _initialize(version: str = "2025-06-18") -> dict[str, Any]:
    return _request(
        "initialize",
        {
            "protocolVersion": version,
            "capabilities": {},
            "clientInfo": {"name": "cc002-test", "version": "1"},
        },
    )


def _call(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    return _request(
        "tools/call",
        {"name": name, "arguments": {} if arguments is None else arguments},
    )


def _error_code(response: dict[str, Any]) -> int:
    return response["error"]["code"]


def _wheel(
    path: Path,
    name: str,
    version: str,
    requires: tuple[str, ...] = (),
    *,
    extra_names: tuple[str, ...] = (),
    metadata_extra: tuple[str, ...] = (),
) -> None:
    metadata = [
        "Metadata-Version: 2.4",
        f"Name: {name}",
        f"Version: {version}",
        *(f"Requires-Dist: {requirement}" for requirement in requires),
        *metadata_extra,
        "",
        "",
    ]
    dist = name.replace("-", "_")
    dist_info = f"{dist}-{version}.dist-info"
    sources = {
        f"{dist_info}/METADATA": "\n".join(metadata).encode(),
        f"{dist_info}/WHEEL": b"Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n\n",
    }
    sources.update({filename: b"fixture" for filename in extra_names})
    import base64
    rows = []
    for filename, source in sources.items():
        digest = base64.urlsafe_b64encode(hashlib.sha256(source).digest()).rstrip(b"=").decode()
        rows.append(f"{filename},sha256={digest},{len(source)}")
    record_name = f"{dist_info}/RECORD"
    rows.append(f"{record_name},,")
    sources[record_name] = ("\n".join(rows) + "\n").encode()
    with zipfile.ZipFile(path, "w") as archive:
        for filename, source in sources.items():
            archive.writestr(filename, source)


def _antlr_sdist(
    path: Path,
    *,
    unsafe: tarfile.TarInfo | None = None,
    pkg_info_extra: bytes = b"",
    setup_directory: bool = False,
) -> bytes:
    root = "antlr4-python3-runtime-4.9.3"
    with tarfile.open(path, "w:gz") as archive:
        for name, source in (
            (f"{root}/PKG-INFO", b"Metadata-Version: 2.1\nName: antlr4-python3-runtime\nVersion: 4.9.3\n" + pkg_info_extra + b"\n"),
            (f"{root}/setup.py", b"from setuptools import setup\nsetup()\n"),
        ):
            member = tarfile.TarInfo(name)
            if setup_directory and name.endswith("/setup.py"):
                member.name += "/"
                member.type = tarfile.DIRTYPE
                source = b""
            member.size = len(source)
            archive.addfile(member, io.BytesIO(source))
        if unsafe is not None:
            archive.addfile(unsafe, io.BytesIO(b"x") if unsafe.size else None)
    return path.read_bytes()


def _built_antlr_wheel(
    path: Path,
    *,
    generator: str = "setuptools (83.0.0)",
    timestamp=(1980, 1, 1, 0, 0, 0),
    extra_names: tuple[str, ...] = (),
    record_mutation: str | None = None,
) -> bytes:
    dist = "antlr4_python3_runtime-4.9.3.dist-info"
    sources = {
        "antlr4/__init__.py": b"",
        f"{dist}/METADATA": b"Metadata-Version: 2.4\nName: antlr4-python3-runtime\nVersion: 4.9.3\n\n",
        f"{dist}/WHEEL": f"Wheel-Version: 1.0\nGenerator: {generator}\nRoot-Is-Purelib: true\nTag: py3-none-any\n\n".encode(),
    }
    sources.update({name: b"fixture" for name in extra_names})
    record_name = f"{dist}/RECORD"
    rows = []
    import base64
    for name, source in sources.items():
        digest = base64.urlsafe_b64encode(hashlib.sha256(source).digest()).rstrip(b"=").decode()
        rows.append(f"{name},sha256={digest},{len(source)}")
    rows.append(f"{record_name},,")
    if record_mutation == "duplicate":
        rows.append(rows[0])
    elif record_mutation == "missing":
        rows.pop(0)
    elif record_mutation == "hash":
        parts = rows[0].split(",")
        parts[1] = "sha256=" + "A" * 43
        rows[0] = ",".join(parts)
    elif record_mutation == "size":
        parts = rows[0].split(",")
        parts[2] = str(int(parts[2]) + 1)
        rows[0] = ",".join(parts)
    sources[record_name] = ("\n".join(rows) + "\n").encode()
    with zipfile.ZipFile(path, "w") as archive:
        for name, source in sources.items():
            info = zipfile.ZipInfo(name, timestamp)
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, source)
    return path.read_bytes()


_PREFIXCOMMONS_METADATA = (
    b"Metadata-Version: 2.1\n"
    b"Name: prefixcommons\n"
    b"Version: 0.1.12\n"
    b"Requires-Dist: click\n"
    b"Requires-Dist: pytest-logging (>=2015.11.4,<2016.0.0)\n"
    b"Summary: Hermetic prefixcommons fixture\n"
)
_PREFIXCOMMONS_WHEEL = (
    b"Wheel-Version: 1.0\n"
    b"Generator: poetry 1.0.7\n"
    b"Root-Is-Purelib: true\n"
    b"Tag: py3-none-any\n"
)
_PREFIXCOMMONS_LICENSE = b"BSD 3-Clause License\nfixture notice\n"
_PREFIXCOMMONS_PAYLOADS = {
    "prefixcommons/__init__.py": b"from .curie_util import expand_uri, contract_uri\n",
    "prefixcommons/curie_transformer.py": b"class CurieTransformer: pass\n",
    "prefixcommons/curie_util.py": b"def expand_uri(value): return value\n",
    "prefixcommons/registry/go_context.jsonld": b"{}\n",
    "prefixcommons/registry/go_obo_context.jsonld": b"{}\n",
    "prefixcommons/registry/idot_context.jsonld": b"{}\n",
    "prefixcommons/registry/monarch_context.jsonld": b"{}\n",
    "prefixcommons/registry/obo_context.jsonld": b'{"GO":"http://purl.obolibrary.org/obo/GO_"}\n',
    "prefixcommons/registry/semweb_context.jsonld": b"{}\n",
    "prefixcommons/version.py": b'__version__ = "0.1.12"\n',
}


def _record_source(sources: dict[str, bytes], record_name: str) -> bytes:
    rows = []
    for name in sorted((*sources, record_name)):
        if name == record_name:
            rows.append((name, "", ""))
            continue
        digest = base64.urlsafe_b64encode(hashlib.sha256(sources[name]).digest())
        rows.append((name, "sha256=" + digest.rstrip(b"=").decode("ascii"), str(len(sources[name]))))
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


def _prefixcommons_upstream_wheel(
    path: Path,
    *,
    raw_name: str | None = None,
    member_mode: int = stat.S_IFREG | 0o644,
    duplicate_member: bool = False,
    record_mutation: str | None = None,
    metadata: bytes = _PREFIXCOMMONS_METADATA,
    wheel: bytes = _PREFIXCOMMONS_WHEEL,
    license_source: bytes | None = _PREFIXCOMMONS_LICENSE,
    compression: int = zipfile.ZIP_STORED,
) -> bytes:
    dist_info = "prefixcommons-0.1.12.dist-info"
    sources = {
        **_PREFIXCOMMONS_PAYLOADS,
        f"{dist_info}/METADATA": metadata,
        f"{dist_info}/WHEEL": wheel,
    }
    if license_source is not None:
        sources[f"{dist_info}/LICENSE"] = license_source
    if raw_name is not None:
        sources[raw_name] = sources.pop("prefixcommons/registry/go_context.jsonld")
    record_name = f"{dist_info}/RECORD"
    record = _record_source(sources, record_name)
    if record_mutation == "hash":
        digest_index = record.index(b"sha256=") + len(b"sha256=")
        changed = bytearray(record)
        changed[digest_index] = ord("A") if changed[digest_index] != ord("A") else ord("B")
        record = bytes(changed)
    elif record_mutation == "missing":
        record = record.partition(b"\n")[2]
    elif record_mutation == "duplicate":
        record = record.partition(b"\n")[0] + b"\n" + record
    sources[record_name] = record
    with zipfile.ZipFile(path, "w", compression=compression) as archive:
        for name, source in sources.items():
            info = zipfile.ZipInfo(name, (2020, 1, 2, 3, 4, 6))
            info.compress_type = compression
            info.create_system = 3
            info.external_attr = (
                0o644 if name.startswith(dist_info + "/") else member_mode
            ) << 16
            archive.writestr(info, source)
        if duplicate_member:
            name = "prefixcommons/__init__.py"
            info = zipfile.ZipInfo(name, (2020, 1, 2, 3, 4, 6))
            info.create_system = 3
            info.external_attr = member_mode << 16
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                archive.writestr(info, sources[name])
    return path.read_bytes()


def _corrupt_first_compressed_member(path: Path, compression: int) -> None:
    source = bytearray(path.read_bytes())
    with zipfile.ZipFile(path) as archive:
        member = archive.infolist()[0]
    assert member.compress_type == compression
    name_length, extra_length = struct.unpack_from(
        "<HH", source, member.header_offset + 26
    )
    data_offset = member.header_offset + 30 + name_length + extra_length
    if compression == zipfile.ZIP_DEFLATED:
        source[data_offset] = 0xFF
    else:
        assert compression == zipfile.ZIP_LZMA
        source[data_offset + 4] = 0xFF
    path.write_bytes(source)


def _select_prefixcommons_fixture(
    monkeypatch,
    path: Path,
    *,
    facts_path: Path | None = None,
) -> None:
    source = path.read_bytes()
    with zipfile.ZipFile(path if facts_path is None else facts_path) as archive:
        members = archive.infolist()
        expanded = sum(member.file_size for member in members)
        dist_info = "prefixcommons-0.1.12.dist-info"
        upstream_sources = {
            member.filename: archive.read(member) for member in members
        }
        metadata = archive.read(f"{dist_info}/METADATA")
        wheel = archive.read(f"{dist_info}/WHEEL")
        try:
            license_source = archive.read(f"{dist_info}/LICENSE")
        except KeyError:
            license_source = b""
    derived_dist = "prefixcommons-0.1.12+malleus.1.dist-info"
    derived_sources = {}
    for name, payload in upstream_sources.items():
        if name == f"{dist_info}/RECORD":
            continue
        target = (
            derived_dist + name[len(dist_info) :]
            if name.startswith(dist_info + "/")
            else name
        )
        if name == f"{dist_info}/METADATA":
            payload = payload.replace(
                b"Version: 0.1.12\n",
                b"Version: 0.1.12+malleus.1\n",
                1,
            ).replace(
                b"Requires-Dist: pytest-logging (>=2015.11.4,<2016.0.0)\n",
                b"",
                1,
            )
        elif name == f"{dist_info}/WHEEL":
            payload = payload.replace(
                b"Generator: poetry 1.0.7\n",
                b"Generator: malleus-cc002 (wheel-derivation-v1)\n",
                1,
            )
        derived_sources[target] = payload
    derived_record = f"{derived_dist}/RECORD"
    derived_sources[derived_record] = _record_source(
        derived_sources,
        derived_record,
    )
    selected = environment.SelectedArtifact(
        filename=path.name,
        kind="WHEEL",
        url="https://files.pythonhosted.org/fixture/" + path.name,
        byte_length=len(source),
        sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "DERIVATIVE_INPUTS", (selected,), raising=False)
    facts = {
        "PREFIXCOMMONS_MEMBER_COUNT": len(members),
        "PREFIXCOMMONS_UNCOMPRESSED_BYTE_LENGTH": expanded,
        "PREFIXCOMMONS_DERIVED_UNCOMPRESSED_BYTE_LENGTH": sum(
            len(payload) for payload in derived_sources.values()
        ),
        "PREFIXCOMMONS_PACKAGE_MEMBER_COUNT": len(_PREFIXCOMMONS_PAYLOADS),
        "PREFIXCOMMONS_METADATA_BYTE_LENGTH": len(metadata),
        "PREFIXCOMMONS_METADATA_SHA256": hashlib.sha256(metadata).hexdigest(),
        "PREFIXCOMMONS_WHEEL_BYTE_LENGTH": len(wheel),
        "PREFIXCOMMONS_WHEEL_SHA256": hashlib.sha256(wheel).hexdigest(),
        "PREFIXCOMMONS_LICENSE_BYTE_LENGTH": len(license_source),
        "PREFIXCOMMONS_LICENSE_SHA256": hashlib.sha256(license_source).hexdigest(),
    }
    for name, value in facts.items():
        monkeypatch.setattr(environment, name, value, raising=False)


def _selected_derivation_observation() -> dict[str, Any]:
    return {
        "python": environment.PYTHON_TUPLE,
        "implementation_name": "cpython",
        "soabi": "cpython-312-x86_64-linux-gnu",
        "effective_uid": 501,
        "environment": {
            "source_date_epoch": environment.SOURCE_DATE_EPOCH,
            "tz": "UTC",
            "python_hash_seed": "0",
        },
        "adapter_sha256": "sha256:"
        + hashlib.sha256(environment.ADAPTER_PATH.read_bytes()).hexdigest(),
    }


def _run_derivation_program(monkeypatch, derivative_inputs: Path, output: Path) -> None:
    calls = []
    actual_main = environment._derivation_main

    def observed_main():
        calls.append(True)
        return actual_main()

    with monkeypatch.context() as child:
        child.setattr(
            environment,
            "DERIVATION_INPUT_ROOT",
            derivative_inputs,
            raising=False,
        )
        child.setattr(
            environment,
            "DERIVATION_OUTPUT_ROOT",
            output,
            raising=False,
        )
        child.setattr(
            environment,
            "_observe_derivation_child",
            _selected_derivation_observation,
        )
        child.setattr(environment, "_derivation_main", observed_main)
        child.setitem(sys.modules, "contract_compiler_environment", environment)
        namespace = {"__name__": "__main__"}
        with pytest.raises(SystemExit) as caught:
            builtins.exec(
                compile(environment.DERIVATION_PROGRAM, "<cc002-derivation>", "exec"),
                namespace,
            )
    assert caught.value.code == 0
    assert calls == [True]


def _rewrite_derived_wheel(path: Path, mutation: str, monkeypatch) -> None:
    with zipfile.ZipFile(path) as archive:
        sources = {info.filename: archive.read(info) for info in archive.infolist()}
    record_name = "prefixcommons-0.1.12+malleus.1.dist-info/RECORD"
    if mutation in {"payload-byte", "inflated-payload"}:
        payload_name = "prefixcommons/curie_util.py"
        sources[payload_name] += (
            b"# coherent runtime-only divergence\n"
            if mutation == "payload-byte"
            else b"x" * (1024 * 1024)
        )
        without_record = {
            name: source for name, source in sources.items() if name != record_name
        }
        sources[record_name] = _record_source(without_record, record_name)
    rows = list(
        csv.reader(
            io.StringIO(sources[record_name].decode("utf-8"), newline=""),
            delimiter=",",
            quotechar='"',
            doublequote=True,
            escapechar=None,
            quoting=csv.QUOTE_MINIMAL,
            strict=True,
        )
    )
    payload_row = next(row for row in rows if row[0] != record_name)
    self_row = next(row for row in rows if row[0] == record_name)
    if mutation == "record-order":
        rows[0], rows[1] = rows[1], rows[0]
    elif mutation == "record-digest":
        payload_row[1] = "sha256=" + "A" * 43
    elif mutation == "record-size":
        payload_row[2] = str(int(payload_row[2]) + 1)
    elif mutation == "record-self-hash":
        self_row[1] = "sha256=" + "A" * 43
    elif mutation == "record-self-size":
        self_row[2] = "1"
    elif mutation == "record-fields":
        self_row.append("")
    if mutation.startswith("record-") and mutation not in {
        "record-bom",
        "record-crlf",
        "record-terminal",
    }:
        output = io.StringIO(newline="")
        csv.writer(
            output,
            delimiter=",",
            quotechar='"',
            doublequote=True,
            escapechar=None,
            lineterminator="\n",
            quoting=csv.QUOTE_MINIMAL,
        ).writerows(rows)
        sources[record_name] = output.getvalue().encode("utf-8")
    elif mutation == "record-bom":
        sources[record_name] = b"\xef\xbb\xbf" + sources[record_name]
    elif mutation == "record-crlf":
        sources[record_name] = sources[record_name].replace(b"\n", b"\r\n")
    elif mutation == "record-terminal":
        sources[record_name] = sources[record_name].removesuffix(b"\n")

    names = sorted(sources)
    if mutation == "member-order":
        names.reverse()
    rewritten = path.with_name("rewritten.whl")
    with monkeypatch.context() as zip_context:
        if mutation == "zip64-directory":
            zip_context.setattr(zipfile, "ZIP_FILECOUNT_LIMIT", 1)
        with zipfile.ZipFile(
            rewritten,
            "w",
            compression=zipfile.ZIP_STORED,
            allowZip64=True,
        ) as archive:
            for index, name in enumerate(names):
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
                if index == 0:
                    if mutation == "timestamp":
                        info.date_time = (1982, 1, 1, 0, 0, 0)
                    elif mutation == "compression":
                        info.compress_type = zipfile.ZIP_DEFLATED
                    elif mutation == "create-system":
                        info.create_system = 0
                    elif mutation == "create-version":
                        info.create_version = 21
                    elif mutation == "extract-version":
                        info.extract_version = 21
                    elif mutation == "reserved":
                        info.reserved = 1
                    elif mutation == "volume":
                        info.volume = 1
                    elif mutation == "internal-attr":
                        info.internal_attr = 1
                    elif mutation == "external-attr":
                        info.external_attr = 0o100600 << 16
                    elif mutation == "member-extra":
                        info.extra = b"\xfe\xca\x00\x00"
                    elif mutation == "member-comment":
                        info.comment = b"changed"
                if mutation == "zip64-header" and index == 0:
                    with archive.open(info, "w", force_zip64=True) as stream:
                        stream.write(sources[name])
                else:
                    archive.writestr(info, sources[name])
            archive.comment = b"changed" if mutation == "archive-comment" else b""
    if mutation in {"flag-bits", "unsupported-version-needed", "volume"}:
        source = bytearray(rewritten.read_bytes())
        central_header = source.index(b"PK\x01\x02")
        if mutation == "flag-bits":
            local = source.index(b"PK\x03\x04") + 6
            central = central_header + 8
            struct.pack_into(
                "<H", source, local, struct.unpack_from("<H", source, local)[0] | 0x20
            )
            struct.pack_into(
                "<H",
                source,
                central,
                struct.unpack_from("<H", source, central)[0] | 0x20,
            )
        elif mutation == "volume":
            struct.pack_into("<H", source, central_header + 34, 1)
        else:
            struct.pack_into("<H", source, central_header + 6, 255)
        rewritten.write_bytes(source)
    rewritten.replace(path)


def _execute_verifier_program(
    tmp_path: Path,
    monkeypatch,
    *,
    fault: str | None = None,
) -> tuple[dict[str, int], dict[str, Any]]:
    for name in ("malleus.schema.json", "result.json"):
        (tmp_path / name).unlink(missing_ok=True)
    calls = {
        "pip_install": 0,
        "pip_check": 0,
        "prefix_expand": 0,
        "prefix_contract": 0,
        "namespaces": 0,
        "cfgraph_list": 0,
        "generator": 0,
        "pip_list": 0,
    }
    expected_uri = "http://purl.obolibrary.org/obo/GO_0008150"

    prefixcommons = types.ModuleType("prefixcommons")

    def expand_uri(value, *, strict=False):
        calls["prefix_expand"] += 1
        assert value == "GO:0008150"
        assert strict is True
        if fault == "prefix-expand":
            return "https://example.invalid/wrong"
        return expected_uri

    def contract_uri(value, *, strict=False):
        calls["prefix_contract"] += 1
        assert value == expected_uri
        assert strict is True
        if fault == "prefix-contract":
            return ["WRONG:0008150"]
        return ["GO:0008150"]

    prefixcommons.expand_uri = expand_uri
    prefixcommons.contract_uri = contract_uri

    namespaces_module = types.ModuleType("linkml_runtime.utils.namespaces")

    class FakeNamespaces(dict):
        def curie_for(self, value):
            calls["namespaces"] += 1
            assert value == "https://example.org/item"
            assert self == {"ex": "https://example.org/"}
            if fault == "namespaces":
                return "wrong:item"
            return "ex:item"

    namespaces_module.Namespaces = FakeNamespaces
    runtime_module = types.ModuleType("linkml_runtime")
    runtime_module.__path__ = []
    utils_module = types.ModuleType("linkml_runtime.utils")
    utils_module.__path__ = []
    utils_module.namespaces = namespaces_module
    runtime_module.utils = utils_module
    linkml_module = types.ModuleType("linkml")
    linkml_module.__path__ = []
    antlr_module = types.ModuleType("antlr4")
    pyshex_module = types.ModuleType("pyshex")
    pyshex_module.__path__ = []

    class FakeURIRef(str):
        pass

    class FakeBNode:
        pass

    class FakeRDF:
        first = FakeURIRef("rdf:first")
        rest = FakeURIRef("rdf:rest")
        nil = FakeURIRef("rdf:nil")

    class FakeCFGraph:
        def __init__(self):
            self._links = []
            self._lists = {}

        def add(self, triple):
            self._links.append(triple)

        def objects(self, subject, predicate):
            calls["cfgraph_list"] += 1
            heads = [
                obj
                for current_subject, current_predicate, obj in self._links
                if current_subject == subject and current_predicate == predicate
            ]
            assert len(heads) == 1
            values = self._lists[heads[0]]
            return values[:1] if fault == "cfgraph-list" else values

    FakeCFGraph.__module__ = "CFGraph"
    FakeCFGraph.__name__ = "CFGraph"

    class FakeCollection:
        def __init__(self, graph, head, values):
            graph._lists[head] = list(values)

    shex_evaluator_module = types.ModuleType("pyshex.shex_evaluator")
    shex_evaluator_module.CFGraph = FakeCFGraph
    pyshex_module.shex_evaluator = shex_evaluator_module
    rdflib_module = types.ModuleType("rdflib")
    rdflib_module.__path__ = []
    rdflib_module.BNode = FakeBNode
    rdflib_module.RDF = FakeRDF
    rdflib_module.URIRef = FakeURIRef
    rdflib_collection_module = types.ModuleType("rdflib.collection")
    rdflib_collection_module.Collection = FakeCollection
    rdflib_module.collection = rdflib_collection_module

    class FakeEnvBuilder:
        def __init__(self, **options):
            assert options == {
                "with_pip": False,
                "clear": True,
                "symlinks": False,
            }

        def create(self, target):
            (Path(target) / "bin").mkdir(parents=True)

    def fake_run(arguments, **options):
        command = list(arguments)
        assert options["cwd"] == "/work"
        assert options["shell"] is False
        assert options["check"] is True
        if command[1:4] == ["-m", "pip", "install"]:
            calls["pip_install"] += 1
            return types.SimpleNamespace(returncode=0)
        if command[1:4] == ["-m", "pip", "check"]:
            calls["pip_check"] += 1
            if fault == "pip-check":
                raise subprocess.CalledProcessError(1, command)
            return types.SimpleNamespace(returncode=0)
        if command[1:4] == ["-m", "pip", "list"]:
            calls["pip_list"] += 1
            distributions = [
                {"name": "antlr4-python3-runtime", "version": "4.9.3"},
                {"name": "linkml", "version": "1.11.1"},
                {"name": "linkml-runtime", "version": "1.11.1"},
                {"name": "prefixcommons", "version": "0.1.12+malleus.1"},
            ]
            return types.SimpleNamespace(
                returncode=0,
                stdout=json.dumps(distributions),
            )
        if command[1:3] == ["-m", "linkml.generators.jsonschemagen"]:
            calls["generator"] += 1
            generated = {"wrong": {}} if fault == "generator" else {"$defs": {}}
            options["stdout"].write(json.dumps(generated).encode("utf-8"))
            return types.SimpleNamespace(returncode=0)
        if command[1] == "-c":
            builtins.exec(compile(command[2], "<cc002-verifier-smoke>", "exec"), {})
            return types.SimpleNamespace(returncode=0, stdout="")
        raise AssertionError(f"unexpected verifier subprocess: {command!r}")

    actual_path = pathlib.Path

    def mapped_path(value):
        return tmp_path if value == "/work" else actual_path(value)

    with monkeypatch.context() as verifier:
        verifier.setattr(pathlib, "Path", mapped_path)
        verifier.setattr(platform, "python_implementation", lambda: "CPython")
        verifier.setattr(platform, "python_version", lambda: "3.12.10")
        verifier.setattr(platform, "system", lambda: "Linux")
        verifier.setattr(platform, "machine", lambda: "x86_64")
        verifier.setattr(sys, "version_info", types.SimpleNamespace(major=3, minor=12))
        verifier.setattr(
            sysconfig,
            "get_config_var",
            lambda name: "cpython-312-x86_64-linux-gnu" if name == "SOABI" else None,
        )
        verifier.setattr(venv, "EnvBuilder", FakeEnvBuilder)
        verifier.setattr(subprocess, "run", fake_run)
        verifier.setitem(sys.modules, "antlr4", antlr_module)
        verifier.setitem(sys.modules, "linkml", linkml_module)
        verifier.setitem(sys.modules, "pyshex", pyshex_module)
        verifier.setitem(
            sys.modules,
            "pyshex.shex_evaluator",
            shex_evaluator_module,
        )
        verifier.setitem(sys.modules, "rdflib", rdflib_module)
        verifier.setitem(sys.modules, "rdflib.collection", rdflib_collection_module)
        verifier.setitem(sys.modules, "linkml_runtime", runtime_module)
        verifier.setitem(sys.modules, "linkml_runtime.utils", utils_module)
        verifier.setitem(
            sys.modules,
            "linkml_runtime.utils.namespaces",
            namespaces_module,
        )
        verifier.setitem(sys.modules, "prefixcommons", prefixcommons)
        builtins.exec(
            compile(environment.VERIFIER_PROGRAM, "<cc002-verifier>", "exec"),
            {"__name__": "__main__"},
        )
    result = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))
    return calls, result


def _build_facts() -> dict[str, Any]:
    return {
        "schema": "malleus.cc002.source-build-child/v1",
        "python": environment.PYTHON_TUPLE,
        "preflight_pip": {"version": "25.0.1", "origin": "/pip/pip-25.0.1-py3-none-any.whl/pip/__init__.py"},
        "preflight_backend_distributions": [{"name": "setuptools", "version": "83.0.0"}],
        "preflight_setuptools": {"version": "83.0.0", "origin_root": "/tmp/cc002-backend"},
        "source_date_epoch": 315532800,
        "configuration": {"backend_interface": "setuptools.build_meta:__legacy__", "no_build_isolation": True},
        "tz": "UTC",
        "python_hash_seed": "0",
        "umask": "022",
    }


def _write_build_facts(directory: Path) -> None:
    (directory / ".cc002-build-facts.json").write_text(
        json.dumps(_build_facts()), encoding="utf-8"
    )


def _manifest_for(directory: Path) -> dict[str, Any]:
    artifacts = []
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        source = path.read_bytes()
        artifacts.append(
            {
                "filename": path.name,
                "byte_length": len(source),
                "sha256": "sha256:" + hashlib.sha256(source).hexdigest(),
            }
        )
    return {"artifacts": artifacts}


def test_project_mcp_registration_contains_activation_and_policy_only():
    config = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    server = config["mcp_servers"]["cc002"]
    assert server == {
        "enabled": True,
        "required": True,
        "enabled_tools": ["cc002_acquire", "cc002_verify_offline"],
        "startup_timeout_sec": 10,
        "tool_timeout_sec": 3600,
        "tools": {"cc002_acquire": {"approval_mode": "prompt"}},
    }


def test_machine_registration_example_uses_absolute_disabled_transport():
    config = tomllib.loads(MACHINE_CONFIG_EXAMPLE.read_text(encoding="utf-8"))
    server = config["mcp_servers"]["cc002"]
    assert server["enabled"] is False
    assert Path(server["command"]).is_absolute()
    assert Path(server["args"][0]).is_absolute()
    assert server["args"][1:] == ["serve"]
    assert Path(server["cwd"]).is_absolute()
    assert Path(server["args"][0]).parent.parent == Path(server["cwd"])
    assert server["env"] == {
        "DOCKER_HOST": "unix:///absolute/path/to/.colima/default/docker.sock"
    }
    assert {
        "required",
        "enabled_tools",
        "startup_timeout_sec",
        "tool_timeout_sec",
        "tools",
    }.isdisjoint(server)


def test_project_registration_retains_no_machine_docker_transport():
    source = CONFIG.read_text(encoding="utf-8")
    server = tomllib.loads(source)["mcp_servers"]["cc002"]
    assert "env" not in server
    assert "DOCKER_HOST" not in source


def test_mcp_dependent_skill_has_fail_closed_resolvable_preflight():
    setup = MCP_SETUP.read_text(encoding="utf-8")
    skill = MAINTAINER_SKILL.read_text(encoding="utf-8")
    preflight = skill.split("## MCP preflight\n", 1)[1].split("\n## ", 1)[0]
    setup_link = "../../../.codex/README.md"
    assert "server `cc002`" in preflight
    for tool in ("cc002_acquire", "cc002_verify_offline"):
        assert tool in setup
        assert tool in preflight
    assert f"]({setup_link})" in preflight
    assert (MAINTAINER_SKILL.parent / setup_link).resolve() == MCP_SETUP.resolve()
    assert "If any are absent, stop" in preflight
    for forbidden_fallback in ("shell", "package-manager", "direct-network", "legacy"):
        assert forbidden_fallback in preflight
    assert "Any change that adds an MCP dependency" in preflight
    assert "regression test" in preflight
    assert "--strict-config" in setup
    assert "metadata-bearing `tools/list`" in setup
    assert "MCP request `_meta`" in setup


def test_absolute_desktop_launcher_completes_codex_discovery_from_root(monkeypatch):
    monkeypatch.chdir("/")
    initialized = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {},
    }
    listed = _request(
        "tools/list",
        {"_meta": {"progressToken": 0}},
        request_id=2,
    )
    completed = subprocess.run(
        [sys.executable, str(environment.ADAPTER_PATH), "serve"],
        cwd=ROOT,
        input="\n".join(map(json.dumps, (_initialize(), initialized, listed))) + "\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    assert completed.stderr == ""
    responses = [json.loads(line) for line in completed.stdout.splitlines()]
    assert responses[0]["result"]["serverInfo"]["name"] == "malleus-cc002"
    assert responses[0]["result"]["protocolVersion"] == "2025-06-18"
    assert [tool["name"] for tool in responses[1]["result"]["tools"]] == [
        "cc002_acquire",
        "cc002_verify_offline",
    ]


def test_server_entrypoint_refuses_arguments_and_wrong_repository_cwd(
    tmp_path, monkeypatch, capsys
):
    assert environment.main([]) == 2
    assert environment.main(["_cc002_resolve"]) == 2
    monkeypatch.chdir(tmp_path)
    assert environment.main(["serve"]) == 2
    assert "CC002_CWD" in capsys.readouterr().err


def test_server_entrypoint_accepts_only_serve_in_repository(monkeypatch):
    called = []
    monkeypatch.setattr(environment, "serve", lambda: called.append(True))
    monkeypatch.chdir(ROOT)
    assert environment.main(["serve"]) == 0
    assert called == [True]


def test_import_and_tool_discovery_do_not_touch_network_or_subprocess(monkeypatch):
    def denied(*_args, **_kwargs):
        raise AssertionError("external interaction outside tools/call")

    monkeypatch.setattr(environment.urllib.request, "build_opener", denied)
    monkeypatch.setattr(environment.subprocess, "run", denied)
    services = FakeServices()
    initialized = environment.handle_message(_initialize(), services)
    listed = environment.handle_message(_request("tools/list", {}), services)
    assert initialized["result"]["protocolVersion"] == "2025-06-18"
    assert [tool["name"] for tool in listed["result"]["tools"]] == [
        "cc002_acquire",
        "cc002_verify_offline",
    ]
    assert services.calls == []


@pytest.mark.parametrize("version", environment.SUPPORTED_PROTOCOL_VERSIONS)
def test_initialize_supports_only_declared_protocol_versions(version):
    response = environment.handle_message(_initialize(version), FakeServices())
    assert response == {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "malleus-cc002", "version": "2"},
        },
    }


def test_initialize_negotiates_latest_supported_version_for_unsupported_client():
    response = environment.handle_message(_initialize("2099-01-01"), FakeServices())
    assert response["result"]["protocolVersion"] == environment.SUPPORTED_PROTOCOL_VERSIONS[0]
    disconnect = io.StringIO(json.dumps(_initialize("2099-01-01")) + "\n")
    stdout = io.StringIO()
    environment.serve(disconnect, stdout, io.StringIO(), FakeServices())
    assert json.loads(stdout.getvalue())["result"]["protocolVersion"] == environment.SUPPORTED_PROTOCOL_VERSIONS[0]


def test_initialize_accepts_optional_client_title():
    request = _initialize()
    request["params"]["clientInfo"]["title"] = "Codex"
    response = environment.handle_message(request, FakeServices())
    assert response["result"]["protocolVersion"] == "2025-06-18"


def test_ping_and_initialized_notification_have_correct_shapes():
    assert environment.handle_message(_request("ping", {}), FakeServices()) == {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {},
    }
    notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {},
    }
    assert environment.handle_message(notification, FakeServices()) is None


def test_ping_accepts_mcp_metadata_extension():
    response = environment.handle_message(
        _request("ping", {"_meta": {"progressToken": "p1"}}), FakeServices()
    )
    assert response == {"jsonrpc": "2.0", "id": 1, "result": {}}


def test_tool_requests_accept_codex_progress_metadata():
    services = FakeServices()
    meta = {"_meta": {"progressToken": 0}}
    listed = environment.handle_message(_request("tools/list", meta), services)
    called = environment.handle_message(
        _request(
            "tools/call",
            {"name": "cc002_verify_offline", "arguments": {}, **meta},
        ),
        services,
    )
    assert len(listed["result"]["tools"]) == 2
    assert called["result"]["isError"] is False
    assert services.calls == ["verify"]


@pytest.mark.parametrize("method", ["ping", "tools/list", "tools/call"])
def test_tool_request_metadata_must_be_an_object(method):
    params = {"_meta": 0}
    if method == "tools/call":
        params.update(name="cc002_verify_offline", arguments={})
    response = environment.handle_message(_request(method, params), FakeServices())
    assert _error_code(response) == -32602
    assert "_meta must be an object" in response["error"]["message"]


@pytest.mark.parametrize("cursor", [None, "not-issued"])
def test_tools_list_refuses_unissued_cursor(cursor):
    response = environment.handle_message(
        _request("tools/list", {"cursor": cursor}), FakeServices()
    )
    assert _error_code(response) == -32602
    assert "CC002_CURSOR" in response["error"]["message"]


def test_tool_contracts_are_exact_zero_argument_closed_schemas():
    response = environment.handle_message(_request("tools/list", {}), FakeServices())
    tools = response["result"]["tools"]
    assert len(tools) == 2
    expected = {
        "cc002_acquire": {
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
        "cc002_verify_offline": {
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    }
    for tool in tools:
        assert tool["inputSchema"] == {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        }
        assert tool["annotations"] == expected[tool["name"]]
        assert "outputSchema" in tool
        assert "pattern" not in json.dumps(tool["outputSchema"])
        assert "confirm" not in json.dumps(tool)


def test_tool_output_schemas_are_exact_and_closed():
    tools = {tool["name"]: tool for tool in environment.TOOLS}
    acquire = tools["cc002_acquire"]["outputSchema"]
    verify = tools["cc002_verify_offline"]["outputSchema"]
    assert acquire["additionalProperties"] is False
    assert set(acquire["required"]) == set(acquire["properties"])
    assert acquire["properties"]["schema"] == {
        "const": "malleus.cc002.acquire-result/v4"
    }
    assert acquire["properties"]["state"] == {"const": "MATERIALIZED"}
    assert acquire["properties"]["artifact_count"] == {
        "type": "integer",
        "minimum": 9,
        "maximum": 9,
    }
    assert acquire["properties"]["built_artifact_count"] == {
        "type": "integer",
        "minimum": 2,
        "maximum": 2,
    }
    expected_digest_schema = {"type": "string", "minLength": 71, "maxLength": 71}
    assert acquire["properties"]["derivation_record_sha256"] == (
        expected_digest_schema
    )
    assert verify["additionalProperties"] is False
    assert set(verify["required"]) == set(verify["properties"])
    assert verify["properties"]["schema"] == {
        "const": "malleus.cc002.verify-result/v4"
    }
    assert verify["properties"]["state"] == {"const": "VERIFIED_OFFLINE"}
    assert verify["properties"]["derivation_record_sha256"] == (
        expected_digest_schema
    )
    for schema in (acquire, verify):
        for name, value in schema["properties"].items():
            if name.endswith("sha256") or name.endswith("digest"):
                assert value.get("pattern") is None


def test_result_constructors_refuse_bad_digests_counts_and_unknown_service_output():
    with pytest.raises(environment.CC002Error, match="lowercase hexadecimal"):
        environment.acquire_result(
            artifact_count=9,
            built_artifact_count=2,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "7" * 64,
            wheel_count=1,
            lock_sha256="sha256:" + "G" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )
    with pytest.raises(environment.CC002Error, match="artifact_count"):
        environment.acquire_result(
            artifact_count=True,
            built_artifact_count=2,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "7" * 64,
            wheel_count=1,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )
    with pytest.raises(environment.CC002Error, match="exactly nine"):
        environment.acquire_result(
            artifact_count=8,
            built_artifact_count=2,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "7" * 64,
            wheel_count=1,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )
    with pytest.raises(environment.CC002Error, match="exactly two"):
        environment.acquire_result(
            artifact_count=9,
            built_artifact_count=1,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "7" * 64,
            wheel_count=1,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )
    with pytest.raises(environment.CC002Error, match="derivation_record_sha256"):
        environment.acquire_result(
            artifact_count=9,
            built_artifact_count=2,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "G" * 64,
            wheel_count=1,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )
    with pytest.raises(environment.CC002Error, match="derivation_record_sha256"):
        environment.verify_result(
            environment_manifest_sha256="sha256:" + "3" * 64,
            verification_sha256="sha256:" + "4" * 64,
            generator_output_sha256="sha256:" + "5" * 64,
            installed_distribution_count=1,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
            source_build_record_sha256="sha256:" + "6" * 64,
            derivation_record_sha256="sha256:" + "G" * 64,
        )

    class InvalidServices(FakeServices):
        def acquire(self):
            return {"schema": "malleus.cc002.acquire-result/v1"}

    response = environment.handle_message(_call("cc002_acquire"), InvalidServices())
    assert response["result"]["isError"] is True
    assert "CC002_RESULT" in response["result"]["content"][0]["text"]


def test_public_result_contract_is_v4_only():
    assert environment.SERVER_VERSION == "2"
    acquire = environment.acquire_result(
        artifact_count=9,
        built_artifact_count=2,
        source_build_record_sha256="sha256:" + "6" * 64,
        derivation_record_sha256="sha256:" + "7" * 64,
        wheel_count=1,
        lock_sha256="sha256:" + "1" * 64,
        wheelhouse_sha256="sha256:" + "2" * 64,
    )
    assert acquire["schema"] == "malleus.cc002.acquire-result/v4"
    assert acquire["derivation_record_sha256"] == "sha256:" + "7" * 64
    assert environment._ACQUIRE_PROPERTIES["schema"] == {
        "const": "malleus.cc002.acquire-result/v4"
    }
    assert environment._VERIFY_PROPERTIES["schema"] == {
        "const": "malleus.cc002.verify-result/v4"
    }
    verify = FakeServices().verify()
    for legacy in ("v1", "v2", "v3"):
        with pytest.raises(environment.CC002Error, match="schema"):
            environment._validate_tool_output(
                "cc002_acquire",
                dict(acquire, schema=f"malleus.cc002.acquire-result/{legacy}"),
            )
        with pytest.raises(environment.CC002Error, match="schema"):
            environment._validate_tool_output(
                "cc002_verify_offline",
                dict(verify, schema=f"malleus.cc002.verify-result/{legacy}"),
            )


@pytest.mark.parametrize("legacy", ("v1", "v2", "v3"))
def test_environment_legacy_schemas_are_rejected(tmp_path, monkeypatch, legacy):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    manifest = json.loads((destination / "manifest.json").read_text())
    manifest["schema"] = f"malleus.cc002.compiler-environment/{legacy}"
    _write_bundle_manifest(destination, manifest)
    with pytest.raises(environment.CC002Error, match="schema"):
        environment._validated_environment(destination)


@pytest.mark.parametrize("legacy", ("v1", "v2", "v3"))
def test_internal_verification_legacy_schemas_are_rejected(
    tmp_path, monkeypatch, legacy
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    environment.verify_environment()
    internal_path = destination / "verification.json"
    internal = json.loads(internal_path.read_text())
    internal["schema"] = f"malleus.cc002.internal-verification/{legacy}"
    internal_path.write_text(environment.canonical_json(internal) + "\n", encoding="utf-8")
    completed = json.loads((destination / "manifest.json").read_text())
    completed["verification"] = {"state": "COMPLETE", **environment._artifact_record(internal_path)}
    _write_bundle_manifest(destination, completed)
    with pytest.raises(environment.CC002Error, match="internal verification schema"):
        environment._validated_environment(destination)


@pytest.mark.parametrize(
    ("name", "expected_call", "schema"),
    [
        ("cc002_acquire", "acquire", "malleus.cc002.acquire-result/v4"),
        (
            "cc002_verify_offline",
            "verify",
            "malleus.cc002.verify-result/v4",
        ),
    ],
)
def test_tools_call_only_fixed_services(name, expected_call, schema):
    services = FakeServices()
    response = environment.handle_message(_call(name), services)
    assert services.calls == [expected_call]
    assert response["result"]["isError"] is False
    assert response["result"]["structuredContent"]["schema"] == schema
    assert response["result"]["content"] == [
        {
            "type": "text",
            "text": environment.canonical_json(
                response["result"]["structuredContent"]
            ),
        }
    ]


def test_zero_argument_tool_call_accepts_omitted_arguments():
    services = FakeServices()
    response = environment.handle_message(
        _request("tools/call", {"name": "cc002_acquire"}), services
    )
    assert response["result"]["isError"] is False
    assert services.calls == ["acquire"]


@pytest.mark.parametrize(
    "arguments",
    [
        {"confirm": True},
        {"url": "https://example.invalid"},
        {"token": "caller-controlled"},
        {"host": "registry-1.docker.io"},
        {"digest": "sha256:" + "0" * 64},
        {"command": ["sh"]},
        {"path": "/tmp/output"},
    ],
)
def test_tool_arguments_refuse_old_unbounded_mechanisms(arguments):
    services = FakeServices()
    response = environment.handle_message(_call("cc002_acquire", arguments), services)
    assert _error_code(response) == -32602
    assert services.calls == []


@pytest.mark.parametrize(
    "message",
    [
        [],
        {"jsonrpc": "1.0", "id": 1, "method": "ping", "params": {}},
        {"jsonrpc": "2.0", "id": None, "method": "ping", "params": {}},
        {"jsonrpc": "2.0", "id": True, "method": "ping", "params": {}},
        {"jsonrpc": "2.0", "id": 1, "method": 4, "params": {}},
        {"jsonrpc": "2.0", "id": 1, "method": "ping", "extra": 1},
    ],
)
def test_malformed_jsonrpc_requests_fail_as_invalid_request(message):
    response = environment.handle_message(message, FakeServices())
    assert _error_code(response) == -32600


def test_unknown_method_and_tool_fail_with_standard_codes():
    unknown_method = environment.handle_message(_request("unknown", {}), FakeServices())
    unknown_tool = environment.handle_message(_call("unknown"), FakeServices())
    assert _error_code(unknown_method) == -32601
    assert _error_code(unknown_tool) == -32602


@pytest.mark.parametrize(
    "source",
    [
        "not-json",
        '{"jsonrpc":"2.0","id":1,"id":2,"method":"ping"}',
        '{"jsonrpc":"2.0","id":NaN,"method":"ping"}',
    ],
)
def test_strict_json_line_rejects_syntax_duplicates_and_nonfinite(source):
    response = environment.process_line(source, FakeServices())
    assert response["id"] is None
    assert _error_code(response) == -32700


def test_server_stdout_contains_protocol_lines_only_and_diagnostics_use_stderr():
    source = io.StringIO(
        json.dumps(_request("ping", {}))
        + "\nnot-json\n"
        + json.dumps(_call("unknown"))
        + "\n"
    )
    stdout = io.StringIO()
    stderr = io.StringIO()
    environment.serve(source, stdout, stderr, FakeServices())
    lines = stdout.getvalue().splitlines()
    assert len(lines) == 3
    assert all(json.loads(line)["jsonrpc"] == "2.0" for line in lines)
    assert "Traceback" not in stdout.getvalue()
    assert stderr.getvalue() == ""


def test_operational_tool_error_is_a_tool_result_not_protocol_corruption():
    class BrokenServices(FakeServices):
        def acquire(self):
            raise environment.CC002Error("[CC002_TEST] refused")

    response = environment.handle_message(_call("cc002_acquire"), BrokenServices())
    assert "error" not in response
    assert response["result"] == {
        "content": [{"type": "text", "text": "[CC002_TEST] refused"}],
        "isError": True,
    }


def test_unexpected_service_error_is_contained_and_server_continues():
    class BrokenServices(FakeServices):
        def acquire(self):
            raise RuntimeError("secret traceback detail")

    source = io.StringIO(
        json.dumps(_call("cc002_acquire"))
        + "\n"
        + json.dumps(_request("ping", {}, request_id=2))
        + "\n"
    )
    stdout = io.StringIO()
    environment.serve(source, stdout, io.StringIO(), BrokenServices())
    responses = [json.loads(line) for line in stdout.getvalue().splitlines()]
    assert responses[0]["result"]["isError"] is True
    assert responses[0]["result"]["content"] == [
        {"type": "text", "text": "[CC002_INTERNAL] tool execution failed"}
    ]
    assert responses[1] == {"jsonrpc": "2.0", "id": 2, "result": {}}
    assert "secret traceback detail" not in stdout.getvalue()


@pytest.mark.parametrize(
    "notification",
    [
        {"jsonrpc": "2.0", "method": "unknown", "params": {}},
        {"jsonrpc": "2.0", "method": "ping", "params": {"bad": True}},
        {"jsonrpc": "1.0", "method": "ping", "params": {}},
        {"jsonrpc": "2.0", "method": 4, "params": {}},
        {"jsonrpc": "2.0", "method": "ping", "extra": True},
    ],
)
def test_notifications_never_receive_responses(notification):
    assert environment.handle_message(notification, FakeServices()) is None


def test_selected_artifacts_bind_exact_urls_hashes_and_lengths():
    assert [artifact.as_dict() for artifact in environment.SELECTED_ARTIFACTS] == [
        {
            "filename": "linkml-1.11.1-py3-none-any.whl",
            "kind": "WHEEL",
            "url": "https://files.pythonhosted.org/packages/1f/fb/3068f649cc436be915f51b2f5ac0656c83dc9bcc6d4f8940633e295042c0/linkml-1.11.1-py3-none-any.whl",
            "byte_length": 483751,
            "sha256": "d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed",
        },
        {
            "filename": "linkml_runtime-1.11.1-py3-none-any.whl",
            "kind": "WHEEL",
            "url": "https://files.pythonhosted.org/packages/63/1d/600b0dd24aa61f03d35293a2e9a4695add1e94c03d8701436fb52d5daf4f/linkml_runtime-1.11.1-py3-none-any.whl",
            "byte_length": 654566,
            "sha256": "b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da",
        },
        {
            "filename": "linkml-1.11.1.tar.gz",
            "kind": "SDIST",
            "url": "https://files.pythonhosted.org/packages/b4/26/38e7340959cd4a87bfe5403cfcf5311d9fe2ff4382fa00e96008a1342760/linkml-1.11.1.tar.gz",
            "byte_length": 374853,
            "sha256": "2f6774e13628270cadaeecda3313db0437ecc15cd44ee35c6c2655dbe31c8524",
        },
        {
            "filename": "linkml_runtime-1.11.1.tar.gz",
            "kind": "SDIST",
            "url": "https://files.pythonhosted.org/packages/d0/7c/36332b49226f37d05d0dbfa4fb1c8017963d62ae722102c9c11c1f530696/linkml_runtime-1.11.1.tar.gz",
            "byte_length": 556549,
            "sha256": "e71300b596c4f35aeccd9dca096806678402213dbdb2c5e8e68f507e21320754",
        },
        {
            "filename": "pip-25.0.1-py3-none-any.whl",
            "kind": "WHEEL",
            "url": "https://files.pythonhosted.org/packages/c9/bc/b7db44f5f39f9d0494071bddae6880eb645970366d0a200022a1a93d57f5/pip-25.0.1-py3-none-any.whl",
            "byte_length": 1841526,
            "sha256": "c46efd13b6aa8279f33f2864459c8ce587ea6a1a59ee20de055868d8f7688f7f",
        },
    ]
    assert environment.ALLOWED_HTTPS_HOSTS == frozenset({"files.pythonhosted.org"})
    assert environment.OCI_INDEX_DIGEST == "sha256:" + "fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db"
    assert environment.OCI_CHILD_DIGEST == "sha256:" + "97983fa8cc88343512862c62307159a82261c3528dc025f79e5a3f7af43e50b4"
    assert environment.OCI_PLATFORM == "linux/amd64"
    assert environment.PYTHON_TUPLE == {
        "implementation": "CPython",
        "version": "3.12.10",
        "operating_system": "Linux",
        "architecture": "x86_64",
        "abi": "cp312",
    }


def test_provisional_cfgraph_root_is_exact_embedded_wheel_bytes():
    filename = "cfgraph-0.2.1-py3-none-any.whl"
    source = environment.CFGRAPH_WHEEL_BYTES

    assert environment.CFGRAPH_WHEEL_FILENAME == filename
    assert environment.EMBEDDED_ROOT_ARTIFACTS == {filename: source}
    assert isinstance(source, bytes)
    assert len(source) == 2256
    assert hashlib.sha256(source).hexdigest() == (
        "28a5bc1292af3c7de137c500da2f9607d66ed27fe787f15ce33e5698fa828f13"
    )
    adapter_source = environment.ADAPTER_PATH.read_text(encoding="utf-8")
    assert "CFGRAPH_WHEEL_BYTES = base64.b64decode(" in adapter_source

    dist_info = "cfgraph-0.2.1.dist-info"
    with zipfile.ZipFile(io.BytesIO(source)) as archive:
        assert archive.namelist() == [
            "CFGraph/__init__.py",
            f"{dist_info}/METADATA",
            f"{dist_info}/WHEEL",
            f"{dist_info}/top_level.txt",
            f"{dist_info}/RECORD",
        ]
        metadata = archive.read(f"{dist_info}/METADATA").decode("utf-8").splitlines()
        wheel = archive.read(f"{dist_info}/WHEEL").decode("utf-8").splitlines()

    assert [line for line in metadata if line.startswith("Name:")] == [
        "Name: CFGraph"
    ]
    assert [line for line in metadata if line.startswith("Version:")] == [
        "Version: 0.2.1"
    ]
    assert [line for line in metadata if line.startswith("Requires-Dist:")] == [
        "Requires-Dist: rdflib>=0.4.2"
    ]
    assert [line for line in wheel if line.startswith("Generator:")] == [
        "Generator: setuptools (83.0.0)"
    ]
    assert all(
        "cfgraph" not in artifact.filename.casefold() or artifact.kind != "SDIST"
        for artifacts in (
            environment.SELECTED_ARTIFACTS,
            environment.BUILD_ARTIFACTS,
            environment.DERIVATIVE_INPUTS,
        )
        for artifact in artifacts
    )


def test_governed_prefixcommons_derivative_input_coordinate_is_exact():
    assert environment.PREFIXCOMMONS_INPUT_FILENAME == (
        "prefixcommons-0.1.12-py3-none-any.whl"
    )
    assert environment.PREFIXCOMMONS_DERIVED_FILENAME == (
        "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    )
    assert [artifact.as_dict() for artifact in environment.DERIVATIVE_INPUTS] == [
        {
            "filename": "prefixcommons-0.1.12-py3-none-any.whl",
            "kind": "WHEEL",
            "url": "https://files.pythonhosted.org/packages/31/e8/715b09df3dab02b07809d812042dc47a46236b5603d9d3a2572dbd1d8a97/prefixcommons-0.1.12-py3-none-any.whl",
            "byte_length": 29482,
            "sha256": "16dbc0a1f775e003c724f19a694fcfa3174608f5c8b0e893d494cf8098ac7f8b",
        }
    ]
    assert {
        "member_count": environment.PREFIXCOMMONS_MEMBER_COUNT,
        "expanded_bytes": environment.PREFIXCOMMONS_UNCOMPRESSED_BYTE_LENGTH,
        "derived_expanded_bytes": environment.PREFIXCOMMONS_DERIVED_UNCOMPRESSED_BYTE_LENGTH,
        "package_members": environment.PREFIXCOMMONS_PACKAGE_MEMBER_COUNT,
        "metadata_bytes": environment.PREFIXCOMMONS_METADATA_BYTE_LENGTH,
        "metadata_sha256": environment.PREFIXCOMMONS_METADATA_SHA256,
        "wheel_bytes": environment.PREFIXCOMMONS_WHEEL_BYTE_LENGTH,
        "wheel_sha256": environment.PREFIXCOMMONS_WHEEL_SHA256,
        "license_bytes": environment.PREFIXCOMMONS_LICENSE_BYTE_LENGTH,
        "license_sha256": environment.PREFIXCOMMONS_LICENSE_SHA256,
    } == {
        "member_count": 14,
        "expanded_bytes": 109044,
        "derived_expanded_bytes": 109064,
        "package_members": 10,
        "metadata_bytes": 1960,
        "metadata_sha256": "4c6cf90de54fa4ce46d1235551f75c021bacab34b8c9894fd50a8096441a5303",
        "wheel_bytes": 83,
        "wheel_sha256": "cb778389a15548d4cf6e0cdf367d27627e6d127d5c5fa5ab75eb43950338c56c",
        "license_bytes": 1500,
        "license_sha256": "3a9b5b0d46996cdfd82b65429e189904e4ab1908014ce408cbecde9f591f37b4",
    }


class FakeResponse:
    def __init__(
        self,
        source: bytes,
        url: str,
        *,
        declared_length: int | None = None,
        status: int = 200,
        fail_after: int | None = None,
    ) -> None:
        self.source = source
        self.offset = 0
        self.url = url
        self.status = status
        self.headers = {
            "Content-Length": str(
                len(source) if declared_length is None else declared_length
            )
        }
        self.fail_after = fail_after

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def geturl(self) -> str:
        return self.url

    def read(self, size: int) -> bytes:
        if self.fail_after is not None and self.offset >= self.fail_after:
            raise OSError("interrupted")
        chunk = self.source[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk


class FakeOpener:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.requests = []

    def open(self, request, *, timeout):
        self.requests.append((request, timeout))
        return self.response


class SequenceOpener:
    def __init__(self, *responses: FakeResponse) -> None:
        self.responses = list(responses)
        self.requests = []

    def open(self, request, *, timeout):
        self.requests.append((request, timeout))
        return self.responses.pop(0)


class DuplicateHeaders:
    def __init__(self, name: str, *values: str) -> None:
        self.name = name
        self.values = list(values)

    def get_all(self, name: str):
        return self.values if name.lower() == self.name.lower() else None

    def get(self, name: str):
        values = self.get_all(name)
        return values[0] if values else None


def _synthetic_artifact(source: bytes, url: str = "https://files.pythonhosted.org/a.whl"):
    return environment.SelectedArtifact(
        filename="a.whl",
        kind="WHEEL",
        url=url,
        byte_length=len(source),
        sha256=hashlib.sha256(source).hexdigest(),
    )


def test_download_is_atomic_and_accepts_exact_bytes(tmp_path):
    source = b"exact artifact"
    artifact = _synthetic_artifact(source)
    opener = FakeOpener(FakeResponse(source, artifact.url))
    target = tmp_path / artifact.filename
    environment.download_artifact(artifact, target, opener)
    assert target.read_bytes() == source
    assert not list(tmp_path.glob("*.part"))
    request, timeout = opener.requests[0]
    assert request.full_url == artifact.url
    assert request.get_header("Accept-encoding") == "identity"
    assert timeout == environment.NETWORK_TIMEOUT_SECONDS


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("host", "host"),
        ("redirect", "redirect"),
        ("declared_length", "Content-Length"),
        ("actual_length", "byte length"),
        ("digest", "SHA-256"),
    ],
)
def test_download_refuses_host_redirect_length_and_digest(tmp_path, mutation, message):
    source = b"exact artifact"
    artifact = _synthetic_artifact(source)
    response_source = source
    response_url = artifact.url
    declared_length = None
    if mutation == "host":
        artifact = _synthetic_artifact(source, "https://example.invalid/a.whl")
    elif mutation == "redirect":
        response_url = "https://files.pythonhosted.org/other.whl"
    elif mutation == "declared_length":
        declared_length = len(source) + 1
    elif mutation == "actual_length":
        response_source += b"x"
        declared_length = artifact.byte_length
    elif mutation == "digest":
        artifact = environment.SelectedArtifact(
            filename=artifact.filename,
            kind=artifact.kind,
            url=artifact.url,
            byte_length=artifact.byte_length,
            sha256="0" * 64,
        )
    opener = FakeOpener(
        FakeResponse(
            response_source,
            response_url,
            declared_length=declared_length,
        )
    )
    with pytest.raises(environment.CC002Error, match=message):
        environment.download_artifact(artifact, tmp_path / artifact.filename, opener)
    assert not (tmp_path / artifact.filename).exists()


def test_download_interruption_leaves_no_partial_or_final_file(tmp_path):
    source = b"a" * (environment.DOWNLOAD_CHUNK_SIZE + 10)
    artifact = _synthetic_artifact(source)
    opener = FakeOpener(
        FakeResponse(
            source,
            artifact.url,
            fail_after=environment.DOWNLOAD_CHUNK_SIZE,
        )
    )
    with pytest.raises(environment.CC002Error, match="interrupted"):
        environment.download_artifact(artifact, tmp_path / artifact.filename, opener)
    assert list(tmp_path.iterdir()) == []


def test_default_opener_disables_proxies_and_redirects(monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", "https://hostile.invalid:444")
    captured = []
    monkeypatch.setattr(
        environment.urllib.request,
        "build_opener",
        lambda *handlers: captured.extend(handlers) or object(),
    )
    environment._default_opener()
    proxy = next(
        handler
        for handler in captured
        if isinstance(handler, environment.urllib.request.ProxyHandler)
    )
    assert proxy.proxies == {}
    redirect = next(handler for handler in captured if isinstance(handler, environment._NoRedirect))
    request = environment.urllib.request.Request(
        "https://files.pythonhosted.org/a.whl"
    )
    assert redirect.redirect_request(request, None, 302, "Found", {}, "https://files.pythonhosted.org/b.whl") is None


@pytest.mark.parametrize(
    ("header", "status", "message"),
    [(None, 200, "Content-Length is missing"), ("bad", 200, "invalid Content-Length"), ("1", 206, "HTTP status")],
)
def test_download_requires_200_and_numeric_content_length(tmp_path, header, status, message):
    source = b"x"
    artifact = _synthetic_artifact(source)
    response = FakeResponse(source, artifact.url, status=status)
    if header is None:
        response.headers = {}
    else:
        response.headers = {"Content-Length": header}
    with pytest.raises(environment.CC002Error, match=message):
        environment.download_artifact(
            artifact, tmp_path / artifact.filename, FakeOpener(response)
        )


def test_safe_target_refuses_symlink_and_path_escape(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(environment.CC002Error, match="relative filename"):
        environment.safe_target(root, "../escape")
    with pytest.raises(environment.CC002Error, match="symlink"):
        environment.safe_target(root, "link/file")


def test_download_refuses_target_and_partial_symlinks_without_touching_outside(tmp_path):
    source = b"exact"
    artifact = _synthetic_artifact(source)
    outside = tmp_path / "outside"
    outside.write_bytes(b"outside")
    target = tmp_path / artifact.filename
    target.symlink_to(outside)
    with pytest.raises(environment.CC002Error, match="conflicting existing artifact"):
        environment.download_artifact(
            artifact,
            target,
            FakeOpener(FakeResponse(source, artifact.url)),
        )
    assert outside.read_bytes() == b"outside"
    target.unlink()
    partial = tmp_path / (artifact.filename + ".part")
    partial.symlink_to(outside)
    with pytest.raises(environment.CC002Error, match="symlink|stale partial"):
        environment.download_artifact(
            artifact,
            target,
            FakeOpener(FakeResponse(source, artifact.url)),
        )
    assert outside.read_bytes() == b"outside"


def test_existing_identical_artifact_is_idempotent_and_conflict_fails(tmp_path):
    source = b"exact artifact"
    artifact = _synthetic_artifact(source)
    target = tmp_path / artifact.filename
    target.write_bytes(source)
    denied = FakeOpener(FakeResponse(b"not used", artifact.url))
    environment.download_artifact(artifact, target, denied)
    assert denied.requests == []
    target.write_bytes(b"conflict")
    with pytest.raises(environment.CC002Error, match="conflicting existing artifact"):
        environment.download_artifact(artifact, target, denied)


def test_oci_index_parser_binds_raw_digest_and_unique_linux_amd64_child():
    value = {
        "schemaVersion": 2,
        "manifests": [
            {
                "digest": environment.OCI_CHILD_DIGEST,
                "platform": {"architecture": "amd64", "os": "linux"},
            },
            {
                "digest": "sha256:" + "a" * 64,
                "platform": {"architecture": "arm64", "os": "linux"},
            },
        ],
    }
    raw = environment.canonical_json(value).encode()
    digest = "sha256:" + hashlib.sha256(raw).hexdigest()
    assert environment.parse_oci_index(raw, expected_index_digest=digest) == environment.OCI_CHILD_DIGEST


def test_oci_index_parser_refuses_digest_mismatch_duplicate_platform_and_wrong_child():
    base = {
        "schemaVersion": 2,
        "manifests": [
            {
                "digest": environment.OCI_CHILD_DIGEST,
                "platform": {"architecture": "amd64", "os": "linux"},
            }
        ],
    }
    raw = environment.canonical_json(base).encode()
    with pytest.raises(environment.CC002Error, match="index digest"):
        environment.parse_oci_index(raw, expected_index_digest="sha256:" + "0" * 64)
    duplicate = dict(base)
    duplicate["manifests"] = [*base["manifests"], *base["manifests"]]
    raw_duplicate = environment.canonical_json(duplicate).encode()
    with pytest.raises(environment.CC002Error, match="exactly one linux/amd64"):
        environment.parse_oci_index(
            raw_duplicate,
            expected_index_digest="sha256:" + hashlib.sha256(raw_duplicate).hexdigest(),
        )
    wrong = dict(base)
    wrong["manifests"] = [
        {
            "digest": "sha256:" + "a" * 64,
            "platform": {"architecture": "amd64", "os": "linux"},
        }
    ]
    raw_wrong = environment.canonical_json(wrong).encode()
    with pytest.raises(environment.CC002Error, match="child digest"):
        environment.parse_oci_index(
            raw_wrong,
            expected_index_digest="sha256:" + hashlib.sha256(raw_wrong).hexdigest(),
        )


def test_fixed_oci_requests_use_exact_separate_hosts_urls_headers_and_sequence():
    token = "fixture-bearer-token"
    raw_index = b"raw index"
    opener = SequenceOpener(
        FakeResponse(
            json.dumps({"token": token}).encode(), environment.OCI_AUTH_URL
        ),
        FakeResponse(raw_index, environment.OCI_INDEX_URL),
    )
    assert environment._fetch_selected_oci_index(opener) == raw_index
    assert environment.OCI_AUTH_HTTPS_HOSTS == frozenset({"auth.docker.io"})
    assert environment.OCI_REGISTRY_HTTPS_HOSTS == frozenset(
        {"registry-1.docker.io"}
    )
    assert [request.full_url for request, _timeout in opener.requests] == [
        "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/python:pull",
        "https://registry-1.docker.io/v2/library/python/manifests/sha256:fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db",
    ]
    assert all(
        request.get_method() == "GET"
        and timeout == environment.NETWORK_TIMEOUT_SECONDS
        for request, timeout in opener.requests
    )
    auth_headers = {
        name.lower(): value for name, value in opener.requests[0][0].header_items()
    }
    index_headers = {
        name.lower(): value for name, value in opener.requests[1][0].header_items()
    }
    assert auth_headers == {
        "accept": "application/json",
        "accept-encoding": "identity",
        "user-agent": "malleus-cc002/1",
    }
    assert index_headers == {
        "accept": (
            "application/vnd.oci.image.index.v1+json, "
            "application/vnd.docker.distribution.manifest.list.v2+json"
        ),
        "accept-encoding": "identity",
        "authorization": f"Bearer {token}",
        "user-agent": "malleus-cc002/1",
    }


@pytest.mark.parametrize(
    "url",
    [
        "http://auth.docker.io/token?service=registry.docker.io&scope=repository:library/python:pull",
        "https://auth.docker.io.invalid/token?service=registry.docker.io&scope=repository:library/python:pull",
        "https://user@auth.docker.io/token?service=registry.docker.io&scope=repository:library/python:pull",
        "https://auth.docker.io:443/token?service=registry.docker.io&scope=repository:library/python:pull",
        "https://auth.docker.io//token?service=registry.docker.io&scope=repository:library/python:pull",
        "https://auth.docker.io/%74oken?service=registry.docker.io&scope=repository:library/python:pull",
        "https://auth.docker.io/token?scope=repository:library/python:pull&service=registry.docker.io",
        "https://auth.docker.io/token?service=registry.docker.io&scope=repository%3Alibrary/python%3Apull",
        "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/python:pull&extra=1",
        "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/python:pull#fragment",
        "https://[auth.docker.io/token?service=registry.docker.io&scope=repository:library/python:pull",
    ],
)
def test_fixed_oci_auth_endpoint_refuses_canonicalization_drift(url):
    with pytest.raises(environment.CC002Error, match="OCI endpoint"):
        environment._validate_fixed_oci_endpoint(
            url,
            environment.OCI_AUTH_HTTPS_HOSTS,
            "/token",
            "service=registry.docker.io&scope=repository:library/python:pull",
        )


@pytest.mark.parametrize(
    "redirect",
    [
        "https://auth.docker.io/other",
        "https://registry-1.docker.io/token",
    ],
)
def test_fixed_oci_reader_refuses_same_host_and_cross_host_redirects(redirect):
    request = environment.urllib.request.Request(environment.OCI_AUTH_URL)
    opener = FakeOpener(FakeResponse(b"{}", redirect))
    with pytest.raises(environment.CC002Error, match="redirect"):
        environment._read_fixed_https(
            opener,
            request,
            environment.OCI_AUTH_URL,
            environment.OCI_AUTH_RESPONSE_LIMIT,
            "Docker Hub authentication",
        )


def test_fixed_oci_reader_accepts_missing_length_only_within_bound():
    response = FakeResponse(b"bounded", environment.OCI_AUTH_URL)
    response.headers = {}
    request = environment.urllib.request.Request(environment.OCI_AUTH_URL)
    assert environment._read_fixed_https(
        FakeOpener(response),
        request,
        environment.OCI_AUTH_URL,
        len(b"bounded"),
        "Docker Hub authentication",
    ) == b"bounded"


@pytest.mark.parametrize(
    ("headers", "source", "limit", "message"),
    [
        ({"Content-Length": "bad"}, b"x", 10, "Content-Length"),
        ({"Content-Length": "-1"}, b"x", 10, "Content-Length"),
        ({"Content-Length": "11"}, b"x", 10, "byte limit"),
        ({"Content-Length": "1" * 5000}, b"x", 10, "byte limit"),
        ({"Content-Length": "2"}, b"x", 10, "mismatch"),
        ({"Content-Encoding": "gzip", "Content-Length": "1"}, b"x", 10, "encoded"),
        ({}, b"x" * 11, 10, "byte limit"),
    ],
)
def test_fixed_oci_reader_refuses_invalid_encoding_or_length(
    headers, source, limit, message
):
    response = FakeResponse(source, environment.OCI_AUTH_URL)
    response.headers = headers
    request = environment.urllib.request.Request(environment.OCI_AUTH_URL)
    with pytest.raises(environment.CC002Error, match=message):
        environment._read_fixed_https(
            FakeOpener(response),
            request,
            environment.OCI_AUTH_URL,
            limit,
            "Docker Hub authentication",
        )


def test_fixed_oci_reader_refuses_duplicate_lengths_status_and_interruption():
    request = environment.urllib.request.Request(environment.OCI_AUTH_URL)
    duplicate = FakeResponse(b"x", environment.OCI_AUTH_URL)
    duplicate.headers = DuplicateHeaders("Content-Length", "1", "1")
    with pytest.raises(environment.CC002Error, match="Content-Length"):
        environment._read_fixed_https(
            FakeOpener(duplicate),
            request,
            environment.OCI_AUTH_URL,
            10,
            "Docker Hub authentication",
        )
    status = FakeResponse(b"x", environment.OCI_AUTH_URL, status=401)
    with pytest.raises(environment.CC002Error, match="HTTP status"):
        environment._read_fixed_https(
            FakeOpener(status),
            request,
            environment.OCI_AUTH_URL,
            10,
            "Docker Hub authentication",
        )
    interrupted = FakeResponse(b"xy", environment.OCI_AUTH_URL, fail_after=1)
    with pytest.raises(environment.CC002Error, match="fixed HTTPS request failed"):
        environment._read_fixed_https(
            FakeOpener(interrupted),
            request,
            environment.OCI_AUTH_URL,
            10,
            "Docker Hub authentication",
        )


def test_fixed_oci_reader_refuses_changed_request_without_opening_or_leaking_errors():
    class DeniedOpener:
        def open(self, *_args, **_kwargs):
            raise AssertionError("changed request reached network")

    changed = environment.urllib.request.Request(
        "https://auth.docker.io/other"
    )
    with pytest.raises(environment.CC002Error, match="request identity"):
        environment._read_fixed_https(
            DeniedOpener(),
            changed,
            environment.OCI_AUTH_URL,
            10,
            "Docker Hub authentication",
        )

    sentinel = "registry-secret-sentinel"

    class FailingOpener:
        def open(self, *_args, **_kwargs):
            raise environment.urllib.error.URLError(sentinel)

    fixed = environment.urllib.request.Request(environment.OCI_AUTH_URL)
    with pytest.raises(environment.CC002Error) as caught:
        environment._read_fixed_https(
            FailingOpener(),
            fixed,
            environment.OCI_AUTH_URL,
            10,
            "Docker Hub authentication",
        )
    assert sentinel not in str(caught.value)


@pytest.mark.parametrize(
    "source",
    [
        b"{",
        b'{"token":"one","token":"two"}',
        b"{}",
        b'{"token":"one","access_token":"two"}',
        b'{"token":""}',
        b'{"token":"contains space"}',
        b'{"token":"line\\nbreak"}',
        '{"token":"caf\u00e9"}'.encode(),
        b'{"token":"middle=padding"}',
        b'{"token":"colon:punctuation"}',
        b'{"token":"quote\\\"punctuation"}',
        b'{"token":"backslash\\\\punctuation"}',
        b'{"token":1}',
        b'{"token":"valid","unknown":"field"}',
        b'{"token":"valid","expires_in":true}',
        b'{"token":"valid","expires_in":0}',
        b'{"token":"valid","expires_in":"300"}',
        b'{"token":"valid","issued_at":""}',
        b'{"token":"valid","issued_at":1}',
        b'{"token":"valid","issued_at":"line\\nbreak"}',
        json.dumps(
            {"token": "valid", "issued_at": "x" * (environment.OCI_ISSUED_AT_LIMIT + 1)}
        ).encode(),
        json.dumps(
            {"token": "x" * (environment.OCI_AUTH_RESPONSE_LIMIT + 1)}
        ).encode(),
    ],
)
def test_docker_hub_token_parser_refuses_invalid_or_unbounded_values(source):
    with pytest.raises(environment.CC002Error, match="token response is invalid"):
        environment._parse_docker_hub_token(source)


def test_docker_hub_token_parser_accepts_equal_standard_token_fields():
    source = json.dumps(
        {
            "token": "Exact-._~+/09==",
            "access_token": "Exact-._~+/09==",
            "expires_in": 300,
            "issued_at": "2026-08-25T00:00:00Z",
        }
    ).encode()
    assert environment._parse_docker_hub_token(source) == "Exact-._~+/09=="


def test_registry_secret_never_appears_in_direct_or_mcp_errors():
    sentinel = "registry-secret-sentinel"
    source = json.dumps({"token": f"{sentinel} with-space"}).encode()
    with pytest.raises(environment.CC002Error) as caught:
        environment._parse_docker_hub_token(source)
    assert sentinel not in str(caught.value)

    class InvalidRegistryServices(FakeServices):
        def acquire(self):
            return environment._parse_docker_hub_token(source)

    response = environment.handle_message(
        _call("cc002_acquire"), InvalidRegistryServices()
    )
    assert sentinel not in environment.canonical_json(response)


def test_token_parser_sanitizes_unexpected_parser_errors(monkeypatch):
    sentinel = "registry-secret-sentinel"

    def fail(*_args, **_kwargs):
        raise RuntimeError(sentinel)

    monkeypatch.setattr(environment, "strict_json", fail)
    with pytest.raises(environment.CC002Error) as caught:
        environment._parse_docker_hub_token(b"bounded")
    assert sentinel not in str(caught.value)
    assert "token response is invalid" in str(caught.value)


def test_registry_index_opener_exception_cannot_echo_bearer_header():
    sentinel = "registry-secret-sentinel"

    class HeaderEchoOpener:
        def __init__(self):
            self.calls = 0

        def open(self, request, *, timeout):
            assert timeout == environment.NETWORK_TIMEOUT_SECONDS
            self.calls += 1
            if self.calls == 1:
                return FakeResponse(
                    json.dumps({"token": sentinel}).encode(),
                    environment.OCI_AUTH_URL,
                )
            raise RuntimeError(repr(request.header_items()))

    opener = HeaderEchoOpener()
    with pytest.raises(environment.CC002Error) as caught:
        environment._fetch_selected_oci_index(opener)
    assert opener.calls == 2
    assert sentinel not in str(caught.value)
    assert "fixed HTTPS request failed" in str(caught.value)


def test_acquisition_oci_index_cannot_depend_on_user_home_docker_plugins():
    forbidden = [
        "docker",
        "buildx",
        "imagetools",
        "inspect",
        f"docker.io/library/python@{environment.OCI_INDEX_DIGEST}",
        "--raw",
    ]
    assert not hasattr(environment, "oci_index_command"), (
        "OCI index acquisition still depends on Docker user-home plugin discovery: "
        f"{forbidden!r}"
    )
    source = (ROOT / "scripts" / "contract_compiler_environment.py").read_text(
        encoding="utf-8"
    )
    assert "buildx" not in source
    assert "imagetools" not in source


def test_docker_commands_pin_platform_digest_and_network_modes(tmp_path):
    roots = tmp_path / "roots"
    wheelhouse = tmp_path / "wheelhouse"
    roots.mkdir()
    wheelhouse.mkdir()
    (tmp_path / "derivative-inputs").mkdir()
    (tmp_path / "derive").mkdir()
    pull = environment.image_pull_command()
    resolve = environment.resolve_command(roots, wheelhouse, built=tmp_path / "built")
    derive = environment.derivation_command(
        tmp_path / "derivative-inputs", tmp_path / "derive"
    )
    verify = environment.verify_command(tmp_path / "bundle", tmp_path / "work")
    assert pull[-3:] == ["--platform", "linux/amd64", environment.OCI_CHILD_REFERENCE]
    assert "--platform" in resolve and "linux/amd64" in resolve
    assert "--network" in resolve and "bridge" in resolve
    assert "--pull=never" in resolve
    assert environment.OCI_CHILD_REFERENCE in resolve
    assert "--network" in derive and "none" in derive
    assert "--pull=never" in derive
    assert "--read-only" in derive
    assert environment.OCI_CHILD_REFERENCE in derive
    assert "--network" in verify and "none" in verify
    assert "--pull=never" in verify
    assert "--read-only" in verify
    assert f"{(tmp_path / 'bundle' / 'wheelhouse').resolve()}:/wheelhouse:ro" in verify
    assert f"{environment.SMOKE_INPUT.resolve()}:/input/malleus.yaml:ro" in verify
    assert all(":/repo" not in item for item in verify)
    assert environment.OCI_CHILD_REFERENCE in verify
    assert "linkml.generators.jsonschemagen" in environment.VERIFIER_PROGRAM
    assert "/input/malleus.yaml" in environment.VERIFIER_PROGRAM
    assert "cwd='/work'" in environment.VERIFIER_PROGRAM


def test_resolution_requires_distinct_explicit_built_and_wheelhouse_paths(tmp_path):
    roots = tmp_path / "roots"
    built = tmp_path / "built"
    wheelhouse = tmp_path / "wheelhouse"
    for directory in (roots, built, wheelhouse):
        directory.mkdir()
    with pytest.raises(TypeError):
        environment.resolve_command(roots, wheelhouse)
    with pytest.raises(environment.CC002Error, match="CC002_RESOLVER_MOUNTS"):
        environment.resolve_command(roots, wheelhouse, built=wheelhouse)
    for overlapping in (wheelhouse / "built", wheelhouse.parent):
        with pytest.raises(environment.CC002Error, match="CC002_RESOLVER_MOUNTS"):
            environment.resolve_command(roots, wheelhouse, built=overlapping)
    assert "/repo" not in environment.VERIFIER_PROGRAM
    assert "--no-index" in environment.VERIFIER_PROGRAM
    assert "--require-hashes" in environment.VERIFIER_PROGRAM


@pytest.mark.parametrize(
    "case",
    (
        "roots-equal-wheelhouse",
        "roots-under-wheelhouse",
        "wheelhouse-under-roots",
        "roots-equal-built",
        "roots-under-built",
        "built-under-roots",
    ),
)
def test_resolution_refuses_roots_overlap_with_other_mount_sources(tmp_path, case):
    roots = tmp_path / "roots"
    built = tmp_path / "built"
    wheelhouse = tmp_path / "wheelhouse"
    if case == "roots-equal-wheelhouse":
        roots = wheelhouse
    elif case == "roots-under-wheelhouse":
        roots = wheelhouse / "roots"
    elif case == "wheelhouse-under-roots":
        wheelhouse = roots / "wheelhouse"
    elif case == "roots-equal-built":
        roots = built
    elif case == "roots-under-built":
        roots = built / "roots"
    elif case == "built-under-roots":
        built = roots / "built"
    with pytest.raises(
        environment.CC002Error, match=r"\[CC002_RESOLVER_MOUNTS\]"
    ):
        environment.resolve_command(roots, wheelhouse, built=built)


@pytest.mark.parametrize(
    "wheelhouse",
    (
        environment.ADAPTER_PATH,
        environment.ADAPTER_PATH.parent,
        environment.ADAPTER_PATH.parent.parent,
    ),
)
def test_resolution_refuses_writable_wheelhouse_overlap_with_adapter(
    tmp_path, wheelhouse
):
    with pytest.raises(
        environment.CC002Error, match=r"\[CC002_RESOLVER_MOUNTS\]"
    ):
        environment.resolve_command(
            tmp_path / "roots", wheelhouse, built=tmp_path / "built"
        )


def test_every_container_run_uses_the_exact_nonroot_host_ownership_tuple(tmp_path):
    expected = f"{os.getuid()}:{os.getgid()}"
    (tmp_path / "derivative-inputs").mkdir()
    (tmp_path / "derive").mkdir()
    commands = (
        environment.resolve_command(tmp_path / "roots", tmp_path / "wheelhouse", built=tmp_path / "built"),
        environment.derivation_command(
            tmp_path / "derivative-inputs", tmp_path / "derive"
        ),
        environment.lock_report_command(tmp_path / "bundle", tmp_path / "report"),
        environment.verify_command(tmp_path / "bundle", tmp_path / "verify"),
    )
    for command in commands:
        assert command[:2] == ["docker", "run"]
        assert command.count("--user") == 1
        assert command[command.index("--user") + 1] == expected
        assert not expected.startswith("0:")


def test_host_ownership_tuple_refuses_root_execution(monkeypatch):
    monkeypatch.setattr(environment.os, "getuid", lambda: 0)
    monkeypatch.setattr(environment.os, "getgid", lambda: 0)
    with pytest.raises(environment.CC002Error, match="nonroot|UID"):
        environment.host_ownership()


def test_resolution_command_uses_selected_pip_fixed_index_and_no_proxy(tmp_path):
    roots = tmp_path / "roots"
    wheelhouse = tmp_path / "wheelhouse"
    roots.mkdir()
    wheelhouse.mkdir()
    command = environment.resolve_command(roots, wheelhouse, built=tmp_path / "built")
    assert command[:9] == [
        "docker",
        "run",
        "--rm",
        "--pull=never",
        "--platform",
        "linux/amd64",
        "--network",
        "bridge",
        "--read-only",
    ]
    assert command[-3:] == ["python", "-c", environment.RESOLVER_PROGRAM]
    assert f"{environment.ADAPTER_PATH.resolve()}:/adapter/contract_compiler_environment.py:ro" in command
    source = environment.RESOLVER_PIP_ARGUMENTS
    assert source[:7] == (
        "--isolated",
        "--proxy",
        "{proxy}",
        "download",
        "--no-cache-dir",
        "--index-url",
        "https://pypi.org/simple",
    )
    assert "https://pypi.org/simple" in source
    assert environment.ACQUISITION_HTTPS_HOSTS == frozenset(
        {"pypi.org", "files.pythonhosted.org"}
    )


def test_connect_proxy_accepts_only_exact_acquisition_hosts():
    for host in sorted(environment.ACQUISITION_HTTPS_HOSTS):
        request = (
            f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}:443\r\n\r\n"
        ).encode("ascii")
        assert environment.parse_connect_request(request) == (host, 443)


@pytest.mark.parametrize(
    "proxy_source",
    [
        b"GET https://pypi.org/simple HTTP/1.1\r\nHost: pypi.org\r\n\r\n",
        b"CONNECT example.invalid:443 HTTP/1.1\r\nHost: example.invalid:443\r\n\r\n",
        b"CONNECT pypi.org:80 HTTP/1.1\r\nHost: pypi.org:80\r\n\r\n",
        b"CONNECT user@pypi.org:443 HTTP/1.1\r\nHost: user@pypi.org:443\r\n\r\n",
        b"CONNECT https://pypi.org:443 HTTP/1.1\r\nHost: https://pypi.org:443\r\n\r\n",
        b"CONNECT pypi.org:443 HTTP/1.0\r\nHost: pypi.org:443\r\n\r\n",
        b"CONNECT pypi.org:443 HTTP/1.1\r\nHost: files.pythonhosted.org:443\r\n\r\n",
        b"CONNECT pypi.org:443 HTTP/1.1\r\nMalformed\r\n\r\n",
        b"CONNECT pypi.org:443 HTTP/1.1\r\nHost: pypi.org:443\r\n",
        b"\xff\r\n\r\n",
        b"A" * 8193,
    ],
)
def test_connect_proxy_refuses_unbounded_or_malformed_requests(proxy_source):
    with pytest.raises(environment.CC002Error):
        environment.parse_connect_request(proxy_source)


class FinderTripwire(RuntimeError):
    pass


def _fake_pip_runtime(monkeypatch, destination, dependency, version="25.0.1"):
    calls = {name: 0 for name in ("socket", "vcs", "unpack", "build", "finder")}

    class InstallationError(Exception):
        pass

    class Requirement:
        def __init__(self, source):
            self.source = source
            self.url = source.partition(" @ ")[2] or None

    class InstallRequirement:
        def __init__(self, req, comes_from, *args, **kwargs):
            del args, kwargs
            self.req = req
            self.comes_from = comes_from

    def install_req_from_line(source, comes_from=None, **_kwargs):
        return req_install.InstallRequirement(Requirement(source), comes_from)

    def install_req_from_req_string(source, comes_from=None, **_kwargs):
        return req_install.InstallRequirement(Requirement(source), comes_from)

    def tripwire(name):
        calls[name] += 1
        (destination / name).write_text("reached", encoding="utf-8")

    def fake_main(_arguments):
        parent = install_req_from_line(
            "/roots/linkml-1.11.1-py3-none-any.whl", comes_from=None
        )
        try:
            candidate = install_req_from_req_string(dependency, comes_from=parent)
        except InstallationError:
            return 23
        if candidate.req.url is None:
            calls["finder"] += 1
            raise FinderTripwire("ordinary dependency reached the finder")
        if candidate.req.url.startswith("https:"):
            tripwire("socket")
        elif candidate.req.url.startswith("git+"):
            tripwire("vcs")
        elif candidate.req.url.startswith("file:"):
            tripwire("unpack")
            tripwire("build")
        return 99

    pip = types.ModuleType("pip")
    pip.__version__ = version
    pip.__file__ = environment.PIP_IMPORT_ORIGIN
    internal = types.ModuleType("pip._internal")
    internal.__path__ = []
    exceptions = types.ModuleType("pip._internal.exceptions")
    exceptions.InstallationError = InstallationError
    req = types.ModuleType("pip._internal.req")
    req.__path__ = []
    req_install = types.ModuleType("pip._internal.req.req_install")
    req_install.InstallRequirement = InstallRequirement
    constructors = types.ModuleType("pip._internal.req.constructors")
    constructors.install_req_from_line = install_req_from_line
    constructors.install_req_from_req_string = install_req_from_req_string
    cli = types.ModuleType("pip._internal.cli")
    cli.__path__ = []
    cli_main = types.ModuleType("pip._internal.cli.main")
    cli_main.main = fake_main
    pip._internal = internal
    internal.exceptions = exceptions
    internal.req = req
    internal.cli = cli
    req.req_install = req_install
    req.constructors = constructors
    cli.main = cli_main
    modules = {
        "pip": pip,
        "pip._internal": internal,
        "pip._internal.exceptions": exceptions,
        "pip._internal.req": req,
        "pip._internal.req.req_install": req_install,
        "pip._internal.req.constructors": constructors,
        "pip._internal.cli": cli,
        "pip._internal.cli.main": cli_main,
    }
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)
    return pip, calls


@pytest.mark.parametrize(
    "dependency",
    [
        "Beta @ https://example.invalid/beta.whl",
        "Beta @ git+file:///definitely-missing@abc",
        "Beta @ file:///definitely-missing.tar.gz",
    ],
)
def test_pinned_pip_guard_refuses_direct_dependencies_before_any_preparation(
    tmp_path, monkeypatch, dependency
):
    destination = tmp_path / "wheelhouse"
    destination.mkdir()
    before = tuple(destination.iterdir())
    _pip, calls = _fake_pip_runtime(monkeypatch, destination, dependency)
    arguments = environment._resolver_pip_arguments("http://127.0.0.1:43123")
    assert environment._pinned_pip_main(arguments) == 23
    assert calls == {name: 0 for name in calls}
    assert tuple(destination.iterdir()) == before


def test_pinned_pip_guard_allows_ordinary_dependency_to_reach_finder(
    tmp_path, monkeypatch
):
    destination = tmp_path / "wheelhouse"
    destination.mkdir()
    _pip, calls = _fake_pip_runtime(monkeypatch, destination, "Beta>=3")
    arguments = environment._resolver_pip_arguments("http://127.0.0.1:43123")
    with pytest.raises(FinderTripwire, match="reached the finder"):
        environment._pinned_pip_main(arguments)
    assert calls["finder"] == 1
    assert all(calls[name] == 0 for name in ("socket", "vcs", "unpack", "build"))
    assert tuple(destination.iterdir()) == ()


def test_pinned_pip_wrapper_checks_exact_version_and_patches_before_cli(
    tmp_path, monkeypatch
):
    destination = tmp_path / "wheelhouse"
    destination.mkdir()
    _fake_pip_runtime(monkeypatch, destination, "Beta>=3", version="25.0.2")
    arguments = environment._resolver_pip_arguments("http://127.0.0.1:43123")
    with pytest.raises(environment.CC002Error, match="25.0.1"):
        environment._pinned_pip_main(arguments)
    source = (ROOT / "scripts/contract_compiler_environment.py").read_text(
        encoding="utf-8"
    )
    wrapper = source[source.index("def _pinned_pip_main") : source.index("def resolve_command")]
    assert wrapper.index("_install_direct_dependency_guard") < wrapper.index(
        "from pip._internal.cli.main import main"
    )


def test_pinned_pip_wrapper_refuses_same_version_from_ambient_origin(
    tmp_path, monkeypatch
):
    destination = tmp_path / "wheelhouse"
    destination.mkdir()
    pip, _calls = _fake_pip_runtime(monkeypatch, destination, "Beta>=3")
    pip.__file__ = "/ambient/site-packages/pip/__init__.py"
    arguments = environment._resolver_pip_arguments("http://127.0.0.1:43123")
    with pytest.raises(environment.CC002Error, match="origin|retained"):
        environment._pinned_pip_main(arguments)


def test_resolver_child_pythonpath_contains_only_the_selected_pip_root(tmp_path):
    child_environment = environment._resolver_child_environment(tmp_path)
    assert child_environment["PYTHONPATH"] == f"/roots/{environment.PIP_WHEEL_FILENAME}"
    assert "/adapter" not in child_environment["PYTHONPATH"]


def _synthetic_colima_socket(monkeypatch, endpoint, *, mutation=None):
    path = Path(endpoint.removeprefix("unix://"))
    current_uid = 501
    states = {}
    current = Path(path.anchor)
    states[current] = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_uid=0)
    for component in path.parts[1:-1]:
        current /= component
        states[current] = types.SimpleNamespace(
            st_mode=stat.S_IFDIR | 0o700,
            st_uid=current_uid,
        )
    states[path] = types.SimpleNamespace(
        st_mode=stat.S_IFSOCK | 0o600,
        st_uid=current_uid,
    )
    if mutation is not None:
        mutation(states, path, current_uid)
    observed = []

    def fake_lstat(candidate):
        candidate = Path(candidate)
        observed.append(candidate)
        return states[candidate]

    monkeypatch.setattr(environment.os, "getuid", lambda: current_uid)
    monkeypatch.setattr(environment.os, "lstat", fake_lstat)
    return path, observed


@pytest.mark.parametrize(
    "endpoint",
    [
        "docker.sock",
        "tcp://127.0.0.1:2375",
        "ssh://host/run/docker.sock",
        "unix://relative/docker.sock",
        "unix://authority/absolute/docker.sock",
        "unix:////absolute/docker.sock",
        "unix:///absolute//docker.sock",
        "unix:///absolute/./docker.sock",
        "unix:///absolute/../docker.sock",
        "unix:///absolute/docker.sock/",
        "unix:///absolute/%64ocker.sock",
        "unix:///absolute/docker.sock?query",
        "unix:///absolute/docker.sock#fragment",
        "unix:///absolute\\docker.sock",
        "unix:///absolute/\x00docker.sock",
    ],
)
def test_docker_host_refuses_noncanonical_or_nonlocal_endpoints(
    monkeypatch, endpoint
):
    if "\x00" in endpoint:
        monkeypatch.setattr(environment.os, "environ", {"DOCKER_HOST": endpoint})
    else:
        monkeypatch.setenv("DOCKER_HOST", endpoint)
    monkeypatch.setattr(
        environment.os,
        "lstat",
        lambda _path: pytest.fail("invalid URI reached the filesystem"),
    )
    with pytest.raises(environment.CC002Error, match="DOCKER_HOST|Unix|canonical"):
        environment.validated_docker_host()


@pytest.mark.parametrize("endpoint", [None, ""])
def test_docker_host_is_required_with_actionable_machine_setup(monkeypatch, endpoint):
    if endpoint is None:
        monkeypatch.delenv("DOCKER_HOST", raising=False)
    else:
        monkeypatch.setenv("DOCKER_HOST", endpoint)
    with pytest.raises(environment.CC002Error) as caught:
        environment.validated_docker_host()
    message = str(caught.value)
    for token in (
        "DOCKER_HOST",
        "[mcp_servers.cc002.env]",
        ".codex/README.md",
        "restart",
    ):
        assert token in message


@pytest.mark.parametrize(
    "endpoint",
    [
        "unix:///Users/alice/.colima/default/docker.sock",
        "unix:///opt/colima/docker.sock",
    ],
)
def test_docker_host_accepts_exact_safe_local_unix_socket(
    monkeypatch, endpoint
):
    path, observed = _synthetic_colima_socket(monkeypatch, endpoint)
    monkeypatch.setenv("DOCKER_HOST", endpoint)
    assert environment.validated_docker_host() == endpoint
    assert observed[0] == Path(path.anchor)
    assert observed[-1] == path
    assert observed == list(path.parents)[::-1] + [path]


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        (
            lambda states, path, _uid: setattr(
                states[path.parent], "st_mode", stat.S_IFLNK | 0o700
            ),
            "symlink",
        ),
        (
            lambda states, path, _uid: setattr(
                states[path.parent], "st_mode", stat.S_IFREG | 0o600
            ),
            "directory",
        ),
        (
            lambda states, path, _uid: setattr(states[path.parent], "st_uid", 777),
            "owner",
        ),
        (
            lambda states, path, _uid: setattr(
                states[path.parent], "st_mode", stat.S_IFDIR | 0o720
            ),
            "writable",
        ),
        (
            lambda states, path, _uid: setattr(
                states[path], "st_mode", stat.S_IFLNK | 0o600
            ),
            "symlink",
        ),
        (
            lambda states, path, _uid: setattr(
                states[path], "st_mode", stat.S_IFREG | 0o600
            ),
            "socket",
        ),
        (
            lambda states, path, _uid: setattr(states[path], "st_uid", 0),
            "owner",
        ),
        (
            lambda states, path, _uid: setattr(
                states[path], "st_mode", stat.S_IFSOCK | 0o660
            ),
            "0600",
        ),
    ],
)
def test_docker_host_refuses_unsafe_ancestor_or_socket(
    monkeypatch, mutation, reason
):
    endpoint = "unix:///Users/alice/.colima/default/docker.sock"
    _synthetic_colima_socket(monkeypatch, endpoint, mutation=mutation)
    monkeypatch.setenv("DOCKER_HOST", endpoint)
    with pytest.raises(environment.CC002Error, match=reason):
        environment.validated_docker_host()


def test_docker_host_refuses_missing_component_as_typed_error(monkeypatch):
    endpoint = "unix:///Users/alice/.colima/default/docker.sock"
    _path, _observed = _synthetic_colima_socket(monkeypatch, endpoint)
    original = environment.os.lstat

    def missing(candidate):
        if Path(candidate).name == ".colima":
            raise FileNotFoundError(candidate)
        return original(candidate)

    monkeypatch.setattr(environment.os, "lstat", missing)
    monkeypatch.setenv("DOCKER_HOST", endpoint)
    with pytest.raises(environment.CC002Error, match="DOCKER_HOST|missing"):
        environment.validated_docker_host()


def test_subprocess_runner_is_fixed_shell_false_cwd_and_sanitized_env(
    tmp_path, monkeypatch
):
    observed = {}

    def fake_run(argv, **kwargs):
        observed["argv"] = argv
        observed.update(kwargs)
        assert Path(kwargs["env"]["HOME"]).parent == tmp_path
        assert list(Path(kwargs["env"]["HOME"]).iterdir()) == []
        return subprocess.CompletedProcess(argv, 0, stdout=b"{}", stderr=b"")

    monkeypatch.setattr(environment.subprocess, "run", fake_run)
    monkeypatch.setattr(
        environment,
        "validated_docker_host",
        lambda: "unix:///validated/colima/docker.sock",
    )
    monkeypatch.setenv("HOME", "/hostile/home")
    monkeypatch.setenv("PATH", "/hostile/bin")
    for name in (
        "DOCKER_CONTEXT",
        "DOCKER_TLS_VERIFY",
        "DOCKER_CERT_PATH",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "SSH_AUTH_SOCK",
        "DOCKER_AUTH_CONFIG",
        "REGISTRY_AUTH_TOKEN",
    ):
        monkeypatch.setenv(name, "registry-secret-sentinel")
    environment.run_fixed([environment.DOCKER, "version"], tmp_path)
    assert observed["argv"] == ["docker", "version"]
    assert observed["cwd"] == environment.REPOSITORY
    assert observed["shell"] is False
    assert observed["check"] is False
    assert observed["capture_output"] is True
    assert observed["executable"] == str(
        Path(shutil.which("docker", path=environment.SANITIZED_PATH)).resolve()
    )
    assert observed["env"]["HOME"] != "/hostile/home"
    assert observed["env"]["PATH"] == environment.SANITIZED_PATH
    assert observed["env"]["DOCKER_HOST"] == "unix:///validated/colima/docker.sock"
    assert set(observed["env"]) == {
        "DOCKER_HOST",
        "HOME",
        "LANG",
        "LC_ALL",
        "PATH",
        "PYTHONIOENCODING",
    }
    assert "registry-secret-sentinel" not in observed["argv"]
    assert "registry-secret-sentinel" not in observed["env"].values()


def test_docker_transport_is_revalidated_and_executable_reresolved_before_each_run(
    tmp_path, monkeypatch
):
    checks = []
    runs = []

    def validate():
        checks.append("transport")
        return "unix:///validated/colima/docker.sock"

    monkeypatch.setattr(environment, "validated_docker_host", validate)
    monkeypatch.setattr(environment, "_resolved_docker", lambda: "/safe/bin/docker")
    monkeypatch.setattr(
        environment.subprocess,
        "run",
        lambda argv, **kwargs: runs.append((argv, kwargs))
        or subprocess.CompletedProcess(argv, 0, stdout=b"", stderr=b""),
    )
    for _ in range(2):
        environment.run_fixed(
            [environment.DOCKER, "version"],
            tmp_path,
            docker_executable="/safe/bin/docker",
        )
    assert checks == ["transport", "transport"]
    assert len(runs) == 2


def test_docker_subprocess_refuses_stale_resolved_executable(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        environment,
        "validated_docker_host",
        lambda: "unix:///validated/colima/docker.sock",
    )
    monkeypatch.setattr(environment, "_resolved_docker", lambda: "/new/bin/docker")
    monkeypatch.setattr(
        environment.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("stale executable was invoked"),
    )
    with pytest.raises(environment.CC002Error, match="changed|resolved"):
        environment.run_fixed(
            [environment.DOCKER, "version"],
            tmp_path,
            docker_executable="/old/bin/docker",
        )


def test_subprocess_failure_includes_stdout_only_reason(monkeypatch, tmp_path):
    result = subprocess.CompletedProcess(
        ["docker", "version"],
        1,
        stdout=b"ERROR: no matching distribution\n",
        stderr=b"",
    )
    monkeypatch.setattr(environment, "run_fixed", lambda *_args, **_kwargs: result)
    with pytest.raises(environment.CC002Error, match="no matching distribution"):
        environment._run_checked(
            ["docker", "version"],
            "transitive wheel resolution",
            tmp_path,
            docker_executable="/fixture/bin/docker",
        )


def test_subprocess_failure_diagnostic_is_bounded_and_safe(monkeypatch, tmp_path):
    result = subprocess.CompletedProcess(
        ["docker", "version"],
        9,
        stdout=b"\xff\x00" + b"A" * 20_000,
        stderr=b"Traceback (most recent call last):\nsecret\n",
    )
    monkeypatch.setattr(environment, "run_fixed", lambda *_args, **_kwargs: result)
    with pytest.raises(environment.CC002Error) as caught:
        environment._run_checked(
            ["docker", "version"],
            "bounded diagnostic",
            tmp_path,
            docker_executable="/fixture/bin/docker",
        )
    message = str(caught.value)
    assert "failed with 9" in message
    assert "[truncated]" in message
    assert "Traceback" not in message
    assert len(message) <= environment.SUBPROCESS_DIAGNOSTIC_LIMIT + 256


def test_subprocess_diagnostic_preserves_bounded_head_and_conflict_tail():
    conflict = (
        "ERROR: ResolutionImpossible: synthetic-root requires the unavailable "
        "synthetic-addon wheel"
    )
    stderr = b"Traceback (most recent call last):\nresolver-start\x00\n"
    stdout = b"resolution-start\n" + b"A" * 20_000 + b"\n" + conflict.encode()
    unbounded = (
        "stderr: [stack trace marker omitted]\n"
        "resolver-start\N{REPLACEMENT CHARACTER}\n"
        "stdout: resolution-start\n"
        + "A" * 20_000
        + "\n"
        + conflict
    )
    marker = "\n[truncated]\n"

    diagnostic = environment._subprocess_diagnostic(stderr, stdout)

    assert diagnostic == environment._subprocess_diagnostic(stderr, stdout)
    assert len(unbounded[:2042]) == 2042
    assert len(unbounded[-2041:]) == 2041
    assert diagnostic == unbounded[:2042] + marker + unbounded[-2041:]
    assert len(diagnostic) == environment.SUBPROCESS_DIAGNOSTIC_LIMIT
    assert "stdout: resolution-start" in diagnostic
    assert conflict in diagnostic
    assert diagnostic.count(marker) == 1
    assert "Traceback" not in diagnostic
    assert "\x00" not in diagnostic


def test_subprocess_diagnostic_exact_limit_and_limit_plus_one_boundaries():
    prefix = "stdout: "
    marker = "\n[truncated]\n"
    exact_payload = "A" * (environment.SUBPROCESS_DIAGNOSTIC_LIMIT - len(prefix))
    exact_unbounded = prefix + exact_payload

    exact = environment._subprocess_diagnostic(b"", exact_payload.encode())

    assert len(exact_unbounded) == environment.SUBPROCESS_DIAGNOSTIC_LIMIT
    assert exact == exact_unbounded
    assert marker not in exact

    overflow_unbounded = exact_unbounded + "Z"
    overflow = environment._subprocess_diagnostic(
        b"", (exact_payload + "Z").encode()
    )

    assert len(overflow_unbounded) == environment.SUBPROCESS_DIAGNOSTIC_LIMIT + 1
    assert overflow == overflow_unbounded[:2042] + marker + overflow_unbounded[-2041:]
    assert len(overflow) == environment.SUBPROCESS_DIAGNOSTIC_LIMIT
    assert overflow.count(marker) == 1


def test_lock_builder_is_complete_deterministic_and_hash_pinned(tmp_path):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    _wheel(wheelhouse / "alpha-1.0-py3-none-any.whl", "Alpha", "1.0", ("Beta>=2",))
    _wheel(wheelhouse / "beta-2.0-py3-none-any.whl", "Beta", "2.0")
    lock, records = environment.build_lock(wheelhouse)
    assert lock.splitlines() == sorted(lock.splitlines(), key=str.casefold)
    assert len(records) == 2
    assert all(" --hash=sha256:" in line for line in lock.splitlines())
    assert lock.endswith("\n")


def test_lock_builder_refuses_missing_dependency_duplicate_distribution_and_nonwheel(tmp_path):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    _wheel(wheelhouse / "alpha-1.0-py3-none-any.whl", "Alpha", "1.0")
    _wheel(wheelhouse / "alpha-1.0-1-py3-none-any.whl", "alpha", "1.0")
    with pytest.raises(environment.CC002Error, match="duplicate distribution"):
        environment.build_lock(wheelhouse)
    (wheelhouse / "alpha-1.0-1-py3-none-any.whl").unlink()
    (wheelhouse / "unexpected.txt").write_text("x", encoding="utf-8")
    with pytest.raises(environment.CC002Error, match="non-wheel"):
        environment.build_lock(wheelhouse)


def _pip_report(records, *, environment_values=None, installs=None):
    environment_values = environment_values or {
        "implementation_name": "cpython",
        "implementation_version": "3.12.10",
        "python_full_version": "3.12.10",
        "python_version": "3.12",
        "platform_machine": "x86_64",
        "platform_system": "Linux",
    }
    if installs is None:
        installs = [
            {
                "download_info": {
                    "url": f"file:///wheelhouse/{record['filename']}",
                    "archive_info": {
                        "hashes": {"sha256": record["sha256"].removeprefix("sha256:")}
                    },
                },
                "metadata": {
                    "name": record["distribution"],
                    "version": record["version"],
                },
            }
            for record in records
        ]
    return {
        "version": "1",
        "pip_version": "25.0.1",
        "install": installs,
        "environment": environment_values,
    }


def _fake_cc002_edges(tmp_path, monkeypatch, registry_failure_url=None, failure_context=None):
    source_dir = tmp_path / "published"
    source_dir.mkdir()
    artifacts = []
    definitions = [
        ("linkml-1.11.1-py3-none-any.whl", "WHEEL", "linkml", "1.11.1"),
        (
            "linkml_runtime-1.11.1-py3-none-any.whl",
            "WHEEL",
            "linkml-runtime",
            "1.11.1",
        ),
        ("linkml-1.11.1.tar.gz", "SDIST", None, None),
        ("linkml_runtime-1.11.1.tar.gz", "SDIST", None, None),
        ("pip-25.0.1-py3-none-any.whl", "WHEEL", "pip", "25.0.1"),
    ]
    sources = {}
    for filename, kind, distribution, version in definitions:
        path = source_dir / filename
        if kind == "WHEEL":
            _wheel(path, distribution, version)
        else:
            path.write_bytes((filename + "\n").encode())
        source = path.read_bytes()
        url = f"https://files.pythonhosted.org/fixture/{filename}"
        artifacts.append(
            environment.SelectedArtifact(
                filename=filename,
                kind=kind,
                url=url,
                byte_length=len(source),
                sha256=hashlib.sha256(source).hexdigest(),
            )
        )
        sources[url] = source
    build_artifacts = []
    antlr_path = source_dir / environment.ANTLR_SDIST_FILENAME
    _antlr_sdist(antlr_path)
    setuptools_path = source_dir / environment.SETUPTOOLS_WHEEL_FILENAME
    _wheel(setuptools_path, "setuptools", "83.0.0")
    for path, kind in ((antlr_path, "SDIST"), (setuptools_path, "WHEEL")):
        source = path.read_bytes()
        url = f"https://files.pythonhosted.org/fixture/{path.name}"
        build_artifacts.append(
            environment.SelectedArtifact(
                filename=path.name,
                kind=kind,
                url=url,
                byte_length=len(source),
                sha256=hashlib.sha256(source).hexdigest(),
            )
        )
        sources[url] = source
    prefixcommons_path = source_dir / "prefixcommons-0.1.12-py3-none-any.whl"
    _prefixcommons_upstream_wheel(prefixcommons_path)
    _select_prefixcommons_fixture(monkeypatch, prefixcommons_path)
    sources[environment.DERIVATIVE_INPUTS[0].url] = prefixcommons_path.read_bytes()

    class ExternalCalls(list):
        def __init__(self):
            super().__init__()
            self.docker_arguments = []
            self.network_requests = []

    calls = ExternalCalls()
    sources[environment.OCI_AUTH_URL] = json.dumps(
        {"token": "registry-secret-sentinel"}
    ).encode()
    sources[environment.OCI_INDEX_URL] = b"fixture-index"

    class RoutingOpener:
        def open(self, request, *, timeout):
            assert timeout == environment.NETWORK_TIMEOUT_SECONDS
            calls.network_requests.append(request)
            if request.full_url == registry_failure_url:
                raise RuntimeError(repr(request.header_items()))
            source = sources[request.full_url]
            return FakeResponse(source, request.full_url)

    destination = tmp_path / "compiler_environment"
    smoke = tmp_path / "malleus.yaml"
    smoke.write_text("name: malleus\nversion: 0.4.0\n", encoding="utf-8")

    def mount_path(arguments, suffix):
        value = next(item for item in arguments if item.endswith(suffix))
        return Path(value.removesuffix(suffix))

    def fake_run(arguments, context, operation_root, *, docker_executable=None):
        del operation_root
        assert docker_executable == "/fixture/bin/docker"
        calls.docker_arguments.append(list(arguments))
        if arguments[:2] == ["docker", "run"]:
            assert arguments.count("--user") == 1
            assert arguments[arguments.index("--user") + 1] == environment._docker_user_argument()
        calls.append(context)
        if context == failure_context:
            raise environment.CC002Error("[CC002_SUBPROCESS] injected fixture failure")
        if arguments == environment.docker_version_command():
            return b'"28.3.3"\n'
        if arguments == environment.image_pull_command():
            return b""
        if arguments == environment.image_inspect_command():
            return json.dumps(
                {
                    "Architecture": "amd64",
                    "Os": "linux",
                    "RepoDigests": [f"python@{environment.OCI_CHILD_DIGEST}"],
                }
            ).encode()
        if arguments[-1] == environment.LOCK_REPORT_PROGRAM:
            wheelhouse = mount_path(arguments, ":/wheelhouse:ro")
            work = mount_path(arguments, ":/work:rw")
            _lock, records = environment.build_lock(wheelhouse)
            report = _pip_report(
                [record for record in records if record["distribution"] != "pip"]
            )
            (work / "pip-report.json").write_text(json.dumps(report), encoding="utf-8")
            return b""
        if arguments[-1] == environment.VERIFIER_PROGRAM:
            work = mount_path(arguments, ":/work:rw")
            manifest = json.loads((destination / "manifest.json").read_text())
            distributions = [
                {"name": record["distribution"], "version": record["version"]}
                for record in manifest["wheelhouse"]["artifacts"]
            ]
            (work / "malleus.schema.json").write_text(
                json.dumps({"$defs": {"Malleus": {}}}), encoding="utf-8"
            )
            (work / "result.json").write_text(
                json.dumps(
                    {
                        "schema": "malleus.cc002.container-verification/v1",
                        "installed_distributions": distributions,
                        "generator_output": "/work/malleus.schema.json",
                        "python": environment.PYTHON_TUPLE,
                    }
                ),
                encoding="utf-8",
            )
            return b""
        if arguments[-1] == environment.BUILD_PROGRAM:
            output = mount_path(arguments, ":/output:rw")
            _built_antlr_wheel(output / "antlr4_python3_runtime-4.9.3-py3-none-any.whl")
            _write_build_facts(output)
            return b""
        if arguments[-1] == getattr(environment, "DERIVATION_PROGRAM", None):
            derivative_inputs = mount_path(arguments, ":/derivative-inputs:ro")
            output = mount_path(arguments, ":/output:rw")
            _run_derivation_program(monkeypatch, derivative_inputs, output)
            return b""
        if "transitive wheel resolution" == context:
            wheelhouse = mount_path(arguments, ":/wheelhouse:rw")
            cfgraph = wheelhouse / "cfgraph-0.2.1-py3-none-any.whl"
            if cfgraph.exists():
                _wheel(
                    wheelhouse / "rdflib-7.1.4-py3-none-any.whl",
                    "rdflib",
                    "7.1.4",
                )
            return b""
        raise AssertionError(f"unexpected external edge: {context}: {arguments}")

    monkeypatch.setattr(environment, "DESTINATION", destination)
    monkeypatch.setattr(environment, "OUTPUT_TRUSTED_ROOT", tmp_path)
    monkeypatch.setattr(environment, "INTERNAL_VERIFICATION", destination / "verification.json")
    monkeypatch.setattr(environment, "SMOKE_INPUT", smoke)
    monkeypatch.setattr(environment, "SELECTED_ARTIFACTS", tuple(artifacts))
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", tuple(build_artifacts))
    monkeypatch.setattr(environment, "ANTLR_SDIST_MEMBER_COUNT", 2)
    monkeypatch.setattr(
        environment,
        "ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH",
        sum(member.size for member in tarfile.open(antlr_path, "r:gz").getmembers()),
    )
    monkeypatch.setattr(environment, "_default_opener", lambda: RoutingOpener())
    monkeypatch.setattr(environment, "_resolved_docker", lambda: "/fixture/bin/docker")
    monkeypatch.setattr(environment, "parse_oci_index", lambda source: calls.append("parse OCI index") or environment.OCI_CHILD_DIGEST)
    monkeypatch.setattr(environment, "_run_checked", fake_run)
    return destination, calls


def test_embedded_cfgraph_is_root_and_wheelhouse_input_before_external_edge(
    tmp_path, monkeypatch
):
    _destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    opener_factory = environment._default_opener
    observations = []

    class CheckedOpener:
        def __init__(self, delegate):
            self.delegate = delegate

        def open(self, request, *, timeout):
            if not observations:
                staging = next(tmp_path.glob(".cc002-environment-*"))
                root = staging / "roots" / environment.CFGRAPH_WHEEL_FILENAME
                runtime = staging / "wheelhouse" / environment.CFGRAPH_WHEEL_FILENAME
                assert root.read_bytes() == environment.CFGRAPH_WHEEL_BYTES
                assert runtime.read_bytes() == environment.CFGRAPH_WHEEL_BYTES
                observations.append((root, runtime))
            return self.delegate.open(request, timeout=timeout)

    monkeypatch.setattr(
        environment,
        "_default_opener",
        lambda: CheckedOpener(opener_factory()),
    )
    environment.acquire_environment()
    assert len(observations) == 1


@pytest.mark.parametrize(
    "failure_url", [environment.OCI_AUTH_URL, environment.OCI_INDEX_URL]
)
def test_registry_failure_after_root_downloads_leaves_no_publication_or_staging(
    tmp_path, monkeypatch, failure_url
):
    destination, calls = _fake_cc002_edges(
        tmp_path, monkeypatch, registry_failure_url=failure_url
    )
    with pytest.raises(environment.CC002Error) as caught:
        environment.acquire_environment()
    assert "registry-secret-sentinel" not in str(caught.value)
    assert not destination.exists()
    assert list(tmp_path.glob(".cc002-environment-*")) == []
    assert [request.full_url for request in calls.network_requests[:5]] == [
        artifact.url for artifact in environment.SELECTED_ARTIFACTS
    ]
    assert calls.network_requests[-1].full_url == failure_url


@pytest.mark.parametrize(
    "context",
    [
        "network-denied ANTLR source build 1",
        "network-denied ANTLR source build 2",
        "network-denied prefixcommons derivation 1",
        "network-denied prefixcommons derivation 2",
        "transitive wheel resolution",
    ],
)
def test_source_build_failures_leave_no_publication_or_staging(tmp_path, monkeypatch, context):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch, failure_context=context)
    with pytest.raises(environment.CC002Error, match="injected fixture failure"):
        environment.acquire_environment()
    assert not destination.exists()
    assert list(tmp_path.glob(".cc002-*")) == []


def test_full_bundle_validation_failure_cannot_publish_invalid_destination(
    tmp_path, monkeypatch
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)

    def injected_failure(_path=None):
        raise environment.CC002Error("[CC002_INJECTED] full bundle validation failed")

    monkeypatch.setattr(environment, "_validated_environment", injected_failure)
    with pytest.raises(environment.CC002Error, match="full bundle validation failed"):
        environment.acquire_environment()
    assert not destination.exists()
    assert list(tmp_path.glob(".cc002-*")) == []


def test_acquire_revalidates_public_destination_after_atomic_publish(
    tmp_path, monkeypatch
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    original = environment._validated_environment
    validated_paths = []

    def observe(path=None):
        target = environment.DESTINATION if path is None else path
        validated_paths.append(target)
        if target == destination:
            raise environment.CC002Error("[CC002_INJECTED] public validation failed")
        return original(path)

    monkeypatch.setattr(environment, "_validated_environment", observe)
    with pytest.raises(environment.CC002Error, match="public validation failed"):
        environment.acquire_environment()
    assert validated_paths[0].name.startswith(".cc002-environment-")
    assert validated_paths[0] != destination
    assert validated_paths[1] == destination


def test_acquire_orchestrates_report_manifest_round_trip_and_idempotence(
    tmp_path, monkeypatch
):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    result = environment.acquire_environment()
    assert result["artifact_count"] == 9
    assert result["built_artifact_count"] == 2
    assert calls == [
        "Docker version",
        "parse OCI index",
        "OCI child pull",
        "local image inspection",
        "network-denied ANTLR source build 1",
        "network-denied ANTLR source build 2",
        "network-denied prefixcommons derivation 1",
        "network-denied prefixcommons derivation 2",
        "transitive wheel resolution",
        "offline root resolution report",
    ]
    manifest, _source = environment._validated_environment(destination)
    assert manifest["resolution_report"]["filename"] == "resolution-report.json"
    assert manifest["derivation_record"]["filename"] == "derivation-record.json"
    assert result["derivation_record_sha256"] == manifest["derivation_record"][
        "sha256"
    ]
    assert manifest["docker"] == {
        "command": "docker",
        "client_version": "28.3.3",
        "transport": "LOCAL_UNIX_SOCKET",
    }
    assert (destination / "resolution-report.json").is_file()
    assert all(
        "buildx" not in arguments and "imagetools" not in arguments
        for arguments in calls.docker_arguments
    )
    assert all(
        "registry-secret-sentinel" not in argument
        for arguments in calls.docker_arguments
        for argument in arguments
    )
    calls_before = list(calls)
    requests_before = list(calls.network_requests)
    assert environment.acquire_environment() == result
    assert calls == calls_before
    assert calls.network_requests == requests_before


def test_verify_writes_internal_bound_record_and_is_idempotent(tmp_path, monkeypatch):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    candidate_evidence = ROOT / "conformance/contract_compiler/v0/evidence/CC-002.json"
    evidence_before = (
        candidate_evidence.read_bytes() if candidate_evidence.exists() else None
    )
    environment.acquire_environment()
    requests_before = list(calls.network_requests)
    result = environment.verify_environment()
    assert result["state"] == "VERIFIED_OFFLINE"
    assert (destination / "verification.json").is_file()
    manifest, _source = environment._validated_environment(destination)
    assert manifest["verification"]["filename"] == "verification.json"
    internal = json.loads((destination / "verification.json").read_text())
    assert internal["schema"] == "malleus.cc002.internal-verification/v4"
    assert internal["source_build_record_sha256"] == manifest["build_record"]["sha256"]
    assert internal["derivation_record_sha256"] == manifest[
        "derivation_record"
    ]["sha256"]
    calls_before = list(calls)
    assert environment.verify_environment() == result
    assert calls == calls_before
    assert calls.network_requests == requests_before
    evidence_after = (
        candidate_evidence.read_bytes() if candidate_evidence.exists() else None
    )
    assert evidence_after == evidence_before


def test_runtime_ownership_can_change_without_changing_the_bundle_identity(
    tmp_path, monkeypatch
):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    ownership_a = {"uid": 501, "gid": 20}
    ownership_b = {"uid": 502, "gid": 21}
    monkeypatch.setattr(environment, "host_ownership", lambda: ownership_a)
    acquired = environment.acquire_environment()
    pending_source = (destination / "manifest.json").read_bytes()
    pending = json.loads(pending_source)
    monkeypatch.setattr(environment, "host_ownership", lambda: ownership_b)
    assert environment.acquire_environment() == acquired
    assert (destination / "manifest.json").read_bytes() == pending_source
    environment.verify_environment()
    completed = json.loads((destination / "manifest.json").read_text())
    assert {key: value for key, value in completed.items() if key != "verification"} == {
        key: value for key, value in pending.items() if key != "verification"
    }
    assert completed["docker"] == {
        "command": "docker",
        "client_version": "28.3.3",
        "transport": "LOCAL_UNIX_SOCKET",
    }
    assert "offline container verification" in calls


def test_machine_docker_endpoint_and_resolved_executable_are_not_retained(
    tmp_path, monkeypatch
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    endpoint_a = "unix:///Users/alice/.colima/default/docker.sock"
    endpoint_b = "unix:///opt/colima/docker.sock"
    monkeypatch.setenv("DOCKER_HOST", endpoint_a)
    acquired = environment.acquire_environment()
    pending_a = (destination / "manifest.json").read_bytes()
    manifest = json.loads(pending_a)
    assert manifest["docker"] == {
        "command": "docker",
        "client_version": "28.3.3",
        "transport": "LOCAL_UNIX_SOCKET",
    }
    monkeypatch.setenv("DOCKER_HOST", endpoint_b)
    assert environment.acquire_environment() == acquired
    assert (destination / "manifest.json").read_bytes() == pending_a
    verified = environment.verify_environment()
    retained_sources = [
        *(path.read_bytes() for path in destination.rglob("*.json")),
        environment.canonical_json(acquired).encode(),
        environment.canonical_json(verified).encode(),
    ]
    for source in retained_sources:
        for forbidden in (
            endpoint_a,
            endpoint_b,
            "/fixture/bin/docker",
            "resolved_executable",
            "registry-secret-sentinel",
            "Authorization",
            "Bearer ",
        ):
            assert forbidden.encode() not in source


def test_docker_version_command_measures_client_version_key():
    assert environment.docker_version_command() == [
        "docker",
        "version",
        "--format",
        "{{json .Client.Version}}",
    ]


def test_idempotent_acquire_and_complete_verify_do_not_consult_host_ownership(
    tmp_path, monkeypatch
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    acquired = environment.acquire_environment()
    verified = environment.verify_environment()
    manifest_before = (destination / "manifest.json").read_bytes()
    verification_before = (destination / "verification.json").read_bytes()

    def forbidden():
        raise AssertionError("no Docker run means no UID:GID lookup")

    monkeypatch.setattr(environment, "host_ownership", forbidden)
    assert environment.acquire_environment() == acquired
    assert environment.verify_environment() == verified
    assert (destination / "manifest.json").read_bytes() == manifest_before
    assert (destination / "verification.json").read_bytes() == verification_before


def _write_bundle_manifest(destination, manifest):
    (destination / "manifest.json").write_text(
        environment.canonical_json(manifest) + "\n", encoding="utf-8"
    )


def test_bundle_rejects_wheelhouse_pip_that_differs_from_selected_root(
    tmp_path, monkeypatch
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    pip = destination / "wheelhouse" / environment.PIP_WHEEL_FILENAME
    pip.write_bytes(pip.read_bytes() + b"tamper")
    lock, records = environment.build_lock(destination / "wheelhouse")
    (destination / "requirements.lock").write_text(lock, encoding="utf-8")
    manifest = json.loads((destination / "manifest.json").read_text())
    manifest["wheelhouse"] = {
        "artifacts": records,
        "sha256": environment._wheelhouse_identity(records),
    }
    manifest["lock"] = environment._artifact_record(destination / "requirements.lock")
    _write_bundle_manifest(destination, manifest)
    with pytest.raises(environment.CC002Error, match="selected pip|retained root"):
        environment._validated_environment(destination)


def test_bundle_binds_built_antlr_bytes_to_runtime_wheelhouse(tmp_path, monkeypatch):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    manifest = json.loads((destination / "manifest.json").read_text())
    built_record = manifest["built"]["artifacts"][0]
    wheelhouse_records = manifest["wheelhouse"]["artifacts"]
    environment._bind_built_wheel(destination, wheelhouse_records, built_record)
    runtime = destination / "wheelhouse" / built_record["filename"]
    runtime.write_bytes(runtime.read_bytes() + b"tampered")
    with pytest.raises(environment.CC002Error, match="BUILT_BINDING"):
        environment._bind_built_wheel(destination, wheelhouse_records, built_record)


def test_bundle_rejects_coherent_runtime_only_prefixcommons_divergence(
    tmp_path, monkeypatch
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    runtime = destination / "wheelhouse" / environment.PREFIXCOMMONS_DERIVED_FILENAME
    _rewrite_derived_wheel(runtime, "payload-byte", monkeypatch)
    lock, records = environment.build_lock(destination / "wheelhouse")
    (destination / "requirements.lock").write_text(lock, encoding="utf-8")
    report = _pip_report(
        [record for record in records if record["distribution"] != "pip"]
    )
    (destination / "resolution-report.json").write_text(
        environment.canonical_json(report) + "\n",
        encoding="utf-8",
    )
    manifest = json.loads((destination / "manifest.json").read_text())
    manifest["wheelhouse"] = {
        "artifacts": records,
        "sha256": environment._wheelhouse_identity(records),
    }
    manifest["lock"] = environment._artifact_record(destination / "requirements.lock")
    manifest["resolution_report"] = environment._artifact_record(
        destination / "resolution-report.json"
    )
    _write_bundle_manifest(destination, manifest)
    with pytest.raises(environment.CC002Error, match="DERIVATION"):
        environment._validated_environment(destination)


def test_v4_bundle_retains_provisional_root_and_closed_derivation_provenance(
    tmp_path, monkeypatch
):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    acquired = environment.acquire_environment()
    manifest, pending_source = environment._validated_environment(destination)
    upstream_name = "prefixcommons-0.1.12-py3-none-any.whl"
    derived_name = "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"

    assert manifest["schema"] == "malleus.cc002.compiler-environment/v4"
    assert acquired["artifact_count"] == 9
    assert acquired["built_artifact_count"] == 2
    assert len(manifest["roots"]["artifacts"]) == 6
    assert len(manifest["build_inputs"]["artifacts"]) == 2
    assert [record["filename"] for record in manifest["derivative_inputs"]["artifacts"]] == [
        upstream_name
    ]
    assert {record["filename"] for record in manifest["built"]["artifacts"]} == {
        "antlr4_python3_runtime-4.9.3-py3-none-any.whl",
        derived_name,
    }
    assert {path.name for path in destination.iterdir()} == {
        "build-inputs",
        "build-record.json",
        "built",
        "derivation-record.json",
        "derivative-inputs",
        "manifest.json",
        "requirements.lock",
        "resolution-report.json",
        "roots",
        "wheelhouse",
    }
    assert not (destination / upstream_name).exists()
    assert not (destination / "roots" / upstream_name).exists()
    assert not (destination / "built" / upstream_name).exists()
    assert not (destination / "wheelhouse" / upstream_name).exists()
    assert (destination / "derivative-inputs" / upstream_name).is_file()
    assert (destination / "built" / derived_name).read_bytes() == (
        destination / "wheelhouse" / derived_name
    ).read_bytes()
    cfgraph_root = destination / "roots" / environment.CFGRAPH_WHEEL_FILENAME
    cfgraph_runtime = destination / "wheelhouse" / environment.CFGRAPH_WHEEL_FILENAME
    assert cfgraph_root.read_bytes() == environment.CFGRAPH_WHEEL_BYTES
    assert cfgraph_runtime.read_bytes() == environment.CFGRAPH_WHEEL_BYTES
    assert not (destination / "cfgraph-build-record.json").exists()
    assert all(
        "cfgraph" not in record["filename"].casefold()
        for record in manifest["built"]["artifacts"]
    )

    build_record = json.loads((destination / "build-record.json").read_text())
    derivation = json.loads((destination / "derivation-record.json").read_text())
    assert build_record["schema"] == "malleus.cc002.source-build/v1"
    assert set(derivation) == {
        "schema",
        "input",
        "runs",
        "outputs",
        "byte_equal",
        "retained_output",
        "license",
        "tool",
    }
    assert derivation["schema"] == "malleus.cc002.wheel-derivation/v1"
    assert derivation["input"] == manifest["derivative_inputs"]["artifacts"][0]
    retained_output = next(
        record for record in manifest["built"]["artifacts"]
        if record["filename"] == derived_name
    )
    assert derivation["outputs"] == [retained_output, retained_output]
    assert derivation["retained_output"] == retained_output
    assert derivation["byte_equal"] is True
    assert derivation["runs"] == [
        {**environment.RETAINED_DERIVATION_RUN, "output": retained_output},
        {**environment.RETAINED_DERIVATION_RUN, "output": retained_output},
    ]
    assert derivation["license"] == {
        "upstream_member": "prefixcommons-0.1.12.dist-info/LICENSE",
        "derived_member": "prefixcommons-0.1.12+malleus.1.dist-info/LICENSE",
        "byte_length": environment.PREFIXCOMMONS_LICENSE_BYTE_LENGTH,
        "sha256": "sha256:" + environment.PREFIXCOMMONS_LICENSE_SHA256,
    }
    assert derivation["tool"] == {
        "implementation": "python-stdlib",
        "generator": "malleus-cc002 (wheel-derivation-v1)",
        "adapter_sha256": "sha256:"
        + hashlib.sha256(environment.ADAPTER_PATH.read_bytes()).hexdigest(),
    }
    assert manifest["derivation_record"] == environment._artifact_record(
        destination / "derivation-record.json"
    )
    assert acquired["derivation_record_sha256"] == manifest[
        "derivation_record"
    ]["sha256"]

    verified = environment.verify_environment()
    completed, _completed_source = environment._validated_environment(destination)
    internal = json.loads((destination / "verification.json").read_text())
    assert pending_source != (destination / "manifest.json").read_bytes()
    assert completed["verification"]["state"] == "COMPLETE"
    assert verified["derivation_record_sha256"] == manifest[
        "derivation_record"
    ]["sha256"]
    assert internal["derivation_record_sha256"] == manifest[
        "derivation_record"
    ]["sha256"]
    assert calls.network_requests[-1].full_url == environment.OCI_INDEX_URL


@pytest.mark.parametrize(
    "target",
    (
        "input",
        "output",
        "record-extra",
        "record-tool",
        "record-digest",
        "record-python",
        "record-image",
        "record-environment",
        "record-isolation",
        "record-output",
    ),
)
def test_v4_bundle_rejects_derivation_tamper_before_external_edges(
    tmp_path, monkeypatch, target
):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    calls_before = list(calls)
    requests_before = list(calls.network_requests)
    manifest = json.loads((destination / "manifest.json").read_text())
    assert manifest["schema"] == "malleus.cc002.compiler-environment/v4"
    assert "derivative_inputs" in manifest
    assert "derivation_record" in manifest
    if target == "input":
        path = destination / "derivative-inputs" / environment.PREFIXCOMMONS_INPUT_FILENAME
        path.write_bytes(path.read_bytes() + b"tamper")
        manifest["derivative_inputs"]["artifacts"][0] = environment._artifact_record(path)
    elif target == "output":
        path = destination / "built" / environment.PREFIXCOMMONS_DERIVED_FILENAME
        path.write_bytes(path.read_bytes() + b"tamper")
        record = environment._artifact_record(path)
        for index, current in enumerate(manifest["built"]["artifacts"]):
            if current["filename"] == path.name:
                manifest["built"]["artifacts"][index] = record
    else:
        path = destination / "derivation-record.json"
        record = json.loads(path.read_text())
        if target == "record-extra":
            record["unexpected"] = True
        elif target == "record-tool":
            record["tool"]["implementation"] = "third-party"
        elif target == "record-digest":
            record["tool"]["adapter_sha256"] = "sha256:" + "0" * 64
        elif target == "record-python":
            record["runs"][0]["python"]["version"] = "3.12.11"
        elif target == "record-image":
            record["runs"][0]["image"]["child_digest"] = "sha256:" + "0" * 64
        elif target == "record-environment":
            record["runs"][0]["environment"]["tz"] = "LOCAL"
        elif target == "record-isolation":
            record["runs"][0]["isolation"]["network"] = "BRIDGE"
        else:
            record["runs"][0]["output"]["sha256"] = "sha256:" + "0" * 64
        path.write_text(environment.canonical_json(record) + "\n", encoding="utf-8")
        manifest["derivation_record"] = environment._artifact_record(path)
    _write_bundle_manifest(destination, manifest)
    with pytest.raises(environment.CC002Error, match="DERIVATION|PREFIXCOMMONS"):
        environment._validated_environment(destination)
    assert calls == calls_before
    assert calls.network_requests == requests_before


def test_runtime_wheelhouse_excludes_source_and_backend_inputs(tmp_path, monkeypatch):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    names = {path.name for path in (destination / "wheelhouse").iterdir()}
    assert environment.ANTLR_SDIST_FILENAME not in names
    assert environment.SETUPTOOLS_WHEEL_FILENAME not in names
    assert "antlr4_python3_runtime-4.9.3-py3-none-any.whl" in names
    assert environment.PREFIXCOMMONS_INPUT_FILENAME not in names
    assert environment.PREFIXCOMMONS_DERIVED_FILENAME in names
    normalized = {name.split("-", 1)[0].replace("_", "-").casefold() for name in names}
    assert {"pytest", "pytest-logging", "py"}.isdisjoint(normalized)


def test_retained_build_record_contains_no_ephemeral_or_host_paths(tmp_path, monkeypatch):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    source = (destination / "build-record.json").read_text()
    for forbidden in ("/tmp", "/pip", str(ROOT), str(tmp_path), "docker.sock", "uid", "gid"):
        assert forbidden not in source
    record = json.loads(source)
    assert record["post_build"] == {"wheel_generator": "setuptools (83.0.0)"}
    assert set(record["runs"][0]) >= {
        "preflight_pip",
        "preflight_backend_distributions",
        "preflight_setuptools",
        "configuration",
    }
    assert {"pip", "setuptools", "backend_distributions"}.isdisjoint(record["runs"][0])


@pytest.mark.parametrize(
    "mutation",
    [
        "missing_filename",
        "missing_byte_length",
        "missing_sha256",
        "missing_distribution",
        "missing_version",
        "unknown",
        "non_object",
        "filename_type",
        "byte_length_type",
        "sha256_type",
        "distribution_type",
        "version_type",
    ],
)
def test_bundle_wheel_records_fail_actionably_before_any_external_edge(
    tmp_path, monkeypatch, mutation
):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    calls_before = list(calls)
    manifest = json.loads((destination / "manifest.json").read_text())
    record = manifest["wheelhouse"]["artifacts"][0]
    if mutation.startswith("missing_"):
        del record[mutation.removeprefix("missing_")]
    elif mutation == "unknown":
        record["surprise"] = True
    elif mutation == "non_object":
        manifest["wheelhouse"]["artifacts"][0] = None
    elif mutation == "filename_type":
        record["filename"] = 1
    elif mutation == "byte_length_type":
        record["byte_length"] = "1"
    elif mutation == "sha256_type":
        record["sha256"] = 1
    elif mutation == "distribution_type":
        record["distribution"] = None
    else:
        record["version"] = []
    _write_bundle_manifest(destination, manifest)
    with pytest.raises(environment.CC002Error, match="wheel.*record|object"):
        environment._validated_environment(destination)
    assert calls == calls_before


def test_nonobject_manifest_sections_fail_as_typed_cc002_errors(
    tmp_path, monkeypatch
):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    calls_before = list(calls)
    manifest = json.loads((destination / "manifest.json").read_text())
    manifest["roots"] = None
    _write_bundle_manifest(destination, manifest)
    with pytest.raises(environment.CC002Error, match="roots|artifact manifest.*object"):
        environment._validated_environment(destination)
    assert calls == calls_before


@pytest.mark.parametrize("state", ["PENDING", "COMPLETE"])
def test_internal_verification_binds_exact_pending_manifest_lineage(
    tmp_path, monkeypatch, state
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    environment.verify_environment()
    manifest = json.loads((destination / "manifest.json").read_text())
    internal_path = destination / "verification.json"
    internal = json.loads(internal_path.read_text())
    internal["acquisition_manifest_sha256"] = "sha256:" + "0" * 64
    internal_path.write_text(
        environment.canonical_json(internal) + "\n", encoding="utf-8"
    )
    if state == "PENDING":
        manifest["verification"] = {"state": "PENDING"}
    else:
        manifest["verification"] = {
            "state": "COMPLETE",
            **environment._artifact_record(internal_path),
        }
    _write_bundle_manifest(destination, manifest)
    with pytest.raises(environment.CC002Error, match="pending manifest|lineage"):
        environment._validated_environment(destination)


@pytest.mark.parametrize(
    "filename", ["unmanifested.bin", ".verification.json.crash", ".manifest.json.crash"]
)
def test_bundle_top_level_membership_is_exact_or_recovers_known_temp(
    tmp_path, monkeypatch, filename
):
    destination, _calls = _fake_cc002_edges(tmp_path, monkeypatch)
    environment.acquire_environment()
    residue = destination / filename
    residue.write_bytes(b"residue")
    if filename == "unmanifested.bin":
        with pytest.raises(environment.CC002Error, match="top-level"):
            environment._validated_environment(destination)
        assert residue.exists()
    else:
        environment._validated_environment(destination)
        assert not residue.exists()


def test_publish_refuses_symlink_in_lexical_ancestor(tmp_path):
    trusted = tmp_path / "trusted"
    outside = tmp_path / "outside"
    trusted.mkdir()
    outside.mkdir()
    (outside / "inner").mkdir()
    (trusted / "link").symlink_to(outside, target_is_directory=True)
    staging = tmp_path / "staging"
    staging.mkdir()
    (staging / "manifest.json").write_text("x", encoding="utf-8")
    destination = trusted / "link" / "inner" / "environment"
    with pytest.raises(environment.CC002Error, match="symlink|trusted root"):
        environment.publish_directory(staging, destination, trusted)
    assert not (outside / "inner" / "environment").exists()


def test_atomic_replace_accepts_identical_two_verifier_race(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_bytes(b"pending")
    environment._replace_atomic(path, b"pending", b"complete", tmp_path)
    environment._replace_atomic(path, b"pending", b"complete", tmp_path)
    assert path.read_bytes() == b"complete"
    path.write_bytes(b"third")
    with pytest.raises(environment.CC002Error, match="concurrent"):
        environment._replace_atomic(path, b"pending", b"complete", tmp_path)


def test_pip_report_proves_exact_selected_tuple_and_lock_closure(tmp_path):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    _wheel(wheelhouse / "alpha-1.0-py3-none-any.whl", "Alpha", "1.0")
    _lock, records = environment.build_lock(wheelhouse)
    report = _pip_report(records)
    assert environment.validate_resolution_report(report, records) == records


@pytest.mark.parametrize("mutation", ["missing", "version", "digest", "direct_url", "tuple"])
def test_pip_report_refuses_incomplete_incompatible_or_nonlocal_resolution(
    tmp_path, mutation
):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    _wheel(wheelhouse / "alpha-1.0-py3-none-any.whl", "Alpha", "1.0")
    _lock, records = environment.build_lock(wheelhouse)
    report = _pip_report(records)
    if mutation == "missing":
        report["install"] = []
    elif mutation == "version":
        report["install"][0]["metadata"]["version"] = "2.0"
    elif mutation == "digest":
        report["install"][0]["download_info"]["archive_info"]["hashes"]["sha256"] = "0" * 64
    elif mutation == "direct_url":
        report["install"][0]["download_info"]["url"] = "https://example.invalid/alpha.whl"
    else:
        report["environment"]["python_full_version"] = "3.12.9"
    with pytest.raises(environment.CC002Error):
        environment.validate_resolution_report(report, records)


def test_pip_report_does_not_let_an_extra_wheel_self_authorize(tmp_path):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    _wheel(wheelhouse / "alpha-1.0-py3-none-any.whl", "Alpha", "1.0")
    _lock, records = environment.build_lock(wheelhouse)
    report = _pip_report(records)
    _wheel(wheelhouse / "extra-1.0-py3-none-any.whl", "Extra", "1.0")
    _lock, records_with_extra = environment.build_lock(wheelhouse)
    with pytest.raises(environment.CC002Error, match="closure mismatch"):
        environment.validate_resolution_report(report, records_with_extra)


def test_container_result_binds_exact_python_and_installed_closure(tmp_path):
    records = [
        {
            "filename": "linkml-1.11.1-py3-none-any.whl",
            "byte_length": 1,
            "sha256": "sha256:" + "1" * 64,
            "distribution": "linkml",
            "version": "1.11.1",
        },
        {
            "filename": "linkml_runtime-1.11.1-py3-none-any.whl",
            "byte_length": 1,
            "sha256": "sha256:" + "2" * 64,
            "distribution": "linkml-runtime",
            "version": "1.11.1",
        },
        {
            "filename": "pip-25.0.1-py3-none-any.whl",
            "byte_length": 1,
            "sha256": "sha256:" + "3" * 64,
            "distribution": "pip",
            "version": "25.0.1",
        },
        {
            "filename": "prefixcommons-0.1.12+malleus.1-py3-none-any.whl",
            "byte_length": 1,
            "sha256": "sha256:" + "4" * 64,
            "distribution": "prefixcommons",
            "version": "0.1.12+malleus.1",
        },
    ]
    result = {
        "schema": "malleus.cc002.container-verification/v1",
        "installed_distributions": [
            {"name": record["distribution"], "version": record["version"]}
            for record in records
        ],
        "generator_output": "/work/malleus.schema.json",
        "python": environment.PYTHON_TUPLE,
    }
    (tmp_path / "result.json").write_text(json.dumps(result), encoding="utf-8")
    (tmp_path / "malleus.schema.json").write_text(
        json.dumps({"$defs": {"X": {}}}), encoding="utf-8"
    )
    distributions, _digest = environment._validate_container_result(tmp_path, records)
    assert len(distributions) == 4
    result["installed_distributions"].append({"name": "extra", "version": "1"})
    (tmp_path / "result.json").write_text(json.dumps(result), encoding="utf-8")
    with pytest.raises(environment.CC002Error, match="installed closure"):
        environment._validate_container_result(tmp_path, records)


def test_verifier_program_measures_exact_python_tuple_and_abi():
    program = environment.VERIFIER_PROGRAM
    assert "sys.implementation.name" in program
    assert "sys.version_info" in program
    assert "platform.system()" in program
    assert "platform.machine()" in program
    assert "SOABI" in program
    assert "3.12.10" in program
    assert "cp312" in program
    assert "import antlr4" in program
    assert "from pyshex.shex_evaluator import CFGraph" in program
    assert "from CFGraph import CFGraph" not in program
    assert "CFGraph.__module__" in program
    assert "CFGraph.__name__" in program
    assert "from rdflib.collection import Collection" in program
    list_behavior = program.index("Collection(")
    assert program.index("CFGraph()") < list_behavior
    assert program.index("CFGraph.__module__") < list_behavior
    assert program.index("CFGraph.__name__") < list_behavior


def test_lock_report_command_is_exact_selected_container_offline_proof(tmp_path):
    command = environment.lock_report_command(tmp_path / "bundle", tmp_path / "work")
    assert command[:9] == [
        "docker",
        "run",
        "--rm",
        "--pull=never",
        "--platform",
        "linux/amd64",
        "--network",
        "none",
        "--read-only",
    ]
    assert environment.OCI_CHILD_REFERENCE in command
    program = command[-1]
    assert "--dry-run" in program
    assert "--report" in program
    assert "--no-index" in program
    assert "--require-hashes" not in program
    assert "requirements.lock" not in program
    assert "/wheelhouse/linkml-1.11.1-py3-none-any.whl" in program
    assert "/wheelhouse/linkml_runtime-1.11.1-py3-none-any.whl" in program


def test_resolver_and_offline_report_use_each_exact_direct_root_once():
    derived = "/built/prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    cfgraph_root = "/roots/cfgraph-0.2.1-py3-none-any.whl"
    upstream = "prefixcommons-0.1.12-py3-none-any.whl"
    expected_roots = (
        "/roots/linkml-1.11.1-py3-none-any.whl",
        "/roots/linkml_runtime-1.11.1-py3-none-any.whl",
        derived,
        cfgraph_root,
    )
    fixed = tuple(environment.RESOLVER_PIP_ARGUMENTS)
    resolved = tuple(
        environment._resolver_pip_arguments("http://127.0.0.1:43123")
    )
    assert environment._validated_resolver_pip_arguments(resolved) == list(resolved)
    for arguments in (fixed, resolved):
        assert all(arguments.count(root) == 1 for root in expected_roots)
        assert all(upstream not in argument for argument in arguments)
    retained = derived.replace("/built/", "/wheelhouse/")
    assert environment.LOCK_REPORT_PROGRAM.count(retained) == 1
    assert environment.LOCK_REPORT_PROGRAM.count(
        "/wheelhouse/cfgraph-0.2.1-py3-none-any.whl"
    ) == 1
    assert upstream not in environment.LOCK_REPORT_PROGRAM


@pytest.mark.parametrize(
    ("version", "filename"),
    (
        ("0.2.0", "cfgraph-0.2.0-py3-none-any.whl"),
        ("0.2.2", "cfgraph-0.2.2-py3-none-any.whl"),
        ("0.2.1", "cfgraph-0.2.1-1-py3-none-any.whl"),
        ("0.2.1", "cfgraph-0.2.1-py3-none-any.whl"),
    ),
)
def test_runtime_policy_rejects_every_alternate_cfgraph(version, filename):
    record = {
        "filename": filename,
        "byte_length": len(environment.CFGRAPH_WHEEL_BYTES),
        "sha256": "sha256:" + "1" * 64,
        "distribution": "CFGraph",
        "version": version,
    }
    with pytest.raises(environment.CC002Error) as caught:
        environment._validate_runtime_distribution_policy([record])
    assert "CFGRAPH" in str(caught.value)


@pytest.mark.parametrize(
    ("distribution", "version", "filename"),
    (
        ("prefixcommons", "0.1.12", "prefixcommons-0.1.12-py3-none-any.whl"),
        ("prefixcommons", "0.1.11", "prefixcommons-0.1.11-py3-none-any.whl"),
        ("prefixcommons", "0.1.13", "prefixcommons-0.1.13-py3-none-any.whl"),
        (
            "prefixcommons",
            "0.1.12+malleus.2",
            "prefixcommons-0.1.12+malleus.2-py3-none-any.whl",
        ),
        (
            "prefixcommons",
            "0.1.12+other",
            "prefixcommons-0.1.12+other-py3-none-any.whl",
        ),
        ("pytest", "8.4.1", "pytest-8.4.1-py3-none-any.whl"),
        (
            "pytest-logging",
            "2015.11.4",
            "pytest_logging-2015.11.4-py3-none-any.whl",
        ),
        ("py", "1.11.0", "py-1.11.0-py2.py3-none-any.whl"),
    ),
)
def test_resolved_and_installed_closures_reject_upstream_and_test_packages(
    distribution, version, filename
):
    derived = {
        "filename": "prefixcommons-0.1.12+malleus.1-py3-none-any.whl",
        "byte_length": 1,
        "sha256": "sha256:" + "1" * 64,
        "distribution": "prefixcommons",
        "version": "0.1.12+malleus.1",
    }
    candidate = {
        "filename": filename,
        "byte_length": 1,
        "sha256": "sha256:" + "2" * 64,
        "distribution": distribution,
        "version": version,
    }
    records = [candidate] if distribution == "prefixcommons" else [derived, candidate]
    report = _pip_report(records)
    installed = [
        {"name": record["distribution"], "version": record["version"]}
        for record in records
    ]
    with pytest.raises(environment.CC002Error, match="PREFIXCOMMONS|FORBIDDEN|runtime"):
        environment.validate_resolution_report(report, records)
    with pytest.raises(environment.CC002Error, match="PREFIXCOMMONS|FORBIDDEN|runtime"):
        environment._validate_installed_closure(installed, records)


def test_offline_verifier_executes_every_governed_smoke_before_attesting(
    tmp_path, monkeypatch
):
    calls, result = _execute_verifier_program(tmp_path, monkeypatch)
    assert calls == {
        "pip_install": 1,
        "pip_check": 1,
        "prefix_expand": 1,
        "prefix_contract": 1,
        "namespaces": 1,
        "cfgraph_list": 1,
        "generator": 1,
        "pip_list": 1,
    }
    assert result["schema"] == "malleus.cc002.container-verification/v1"
    assert result["generator_output"] == "/work/malleus.schema.json"


@pytest.mark.parametrize(
    "fault",
    (
        "pip-check",
        "prefix-expand",
        "prefix-contract",
        "namespaces",
        "cfgraph-list",
        "generator",
    ),
)
def test_offline_verifier_refuses_any_failed_or_fabricated_smoke(
    tmp_path, monkeypatch, fault
):
    with pytest.raises(
        (AssertionError, RuntimeError, subprocess.CalledProcessError)
    ):
        _execute_verifier_program(tmp_path, monkeypatch, fault=fault)
    assert not (tmp_path / "result.json").exists()


def test_internal_verification_never_occupies_final_candidate_evidence_path():
    source = (
        ROOT / "scripts" / "contract_compiler_environment.py"
    ).read_text(encoding="utf-8")
    assert "CC-002.json" not in source
    assert environment.INTERNAL_VERIFICATION == environment.DESTINATION / "verification.json"


def test_lock_builder_refuses_tampered_wheel_metadata(tmp_path):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    path = wheelhouse / "alpha-1.0-py3-none-any.whl"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("alpha-1.0.dist-info/METADATA", "Name: Alpha\n")
    with pytest.raises(environment.CC002Error, match="Version"):
        environment.build_lock(wheelhouse)


@pytest.mark.parametrize(
    ("raw_name", "metadata_extra"),
    (
        ("alpha/./module.py", ()),
        ("alpha//module.py", ()),
        ("..\\escape.py", ()),
        ("alpha/evil\x1fname.py", ()),
        (None, ("Name: conflicting",)),
        (None, ("Version: 9.9.9",)),
    ),
)
def test_runtime_wheel_lock_refuses_noncanonical_members_and_duplicate_headers(
    tmp_path, raw_name, metadata_extra
):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    _wheel(
        wheelhouse / "alpha-1.0-py3-none-any.whl",
        "alpha",
        "1.0",
        extra_names=() if raw_name is None else (raw_name,),
        metadata_extra=metadata_extra,
    )
    with pytest.raises(environment.CC002Error, match="WHEEL"):
        environment.build_lock(wheelhouse)


def test_bundle_verifier_refuses_missing_tampered_extra_and_symlink_wheels(tmp_path):
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    wheel = wheelhouse / "alpha.whl"
    wheel.write_bytes(b"wheel")
    manifest = _manifest_for(wheelhouse)
    environment.verify_artifact_directory(wheelhouse, manifest)
    wheel.write_bytes(b"tampered")
    with pytest.raises(environment.CC002Error, match="byte length|SHA-256"):
        environment.verify_artifact_directory(wheelhouse, manifest)
    wheel.unlink()
    with pytest.raises(environment.CC002Error, match="missing"):
        environment.verify_artifact_directory(wheelhouse, manifest)
    wheel.write_bytes(b"wheel")
    (wheelhouse / "extra.whl").write_bytes(b"extra")
    with pytest.raises(environment.CC002Error, match="unexpected"):
        environment.verify_artifact_directory(wheelhouse, manifest)
    (wheelhouse / "extra.whl").unlink()
    wheel.unlink()
    outside = tmp_path / "outside.whl"
    outside.write_bytes(b"wheel")
    wheel.symlink_to(outside)
    with pytest.raises(environment.CC002Error, match="symlink"):
        environment.verify_artifact_directory(wheelhouse, manifest)


def test_atomic_directory_publish_accepts_identical_rerun_and_rejects_conflict(tmp_path):
    destination = tmp_path / "environment"
    first = tmp_path / "first"
    first.mkdir()
    (first / "manifest.json").write_text("same\n", encoding="utf-8")
    environment.publish_directory(first, destination, tmp_path)
    assert (destination / "manifest.json").read_text(encoding="utf-8") == "same\n"
    second = tmp_path / "second"
    second.mkdir()
    (second / "manifest.json").write_text("same\n", encoding="utf-8")
    assert environment.publish_directory(second, destination, tmp_path) is False
    conflict = tmp_path / "conflict"
    conflict.mkdir()
    (conflict / "manifest.json").write_text("different\n", encoding="utf-8")
    with pytest.raises(environment.CC002Error, match="conflicting existing environment"):
        environment.publish_directory(conflict, destination, tmp_path)
    shutil.rmtree(destination)
    destination.symlink_to(tmp_path / "outside", target_is_directory=True)
    symlink_staging = tmp_path / "symlink-staging"
    symlink_staging.mkdir()
    with pytest.raises(environment.CC002Error, match="conflicting existing environment"):
        environment.publish_directory(symlink_staging, destination, tmp_path)


def test_source_has_no_regex_or_unbounded_execution_mechanism():
    source = (ROOT / "scripts" / "contract_compiler_environment.py").read_text(
        encoding="utf-8"
    )
    assert "import re" not in source
    assert "from re " not in source
    assert "os.system" not in source
    assert "shell=True" not in source
    assert "Popen(" not in source
    tree = ast.parse(source)
    assert not any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "input"
        for node in ast.walk(tree)
    )
    assert "argparse" not in source
    assert "requests" not in source
    assert 'DOCKER = "/' not in source
    assert "Path.home()" not in source
    assert str(Path.home()) not in source


def _module_scope_import_nodes(tree: ast.Module) -> list[ast.Import | ast.ImportFrom]:
    imports = []
    pending = list(reversed(tree.body))
    pruned = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
    while pending:
        node = pending.pop()
        if isinstance(node, pruned):
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)
            continue
        pending.extend(reversed(list(ast.iter_child_nodes(node))))
    return imports


def test_module_scope_import_scan_reaches_control_flow_and_prunes_callables():
    fixture = ast.parse(
        "try:\n"
        "    import packaging\n"
        "except ImportError:\n"
        "    pass\n"
        "class ImportTimeBody:\n"
        "    import class_dependency\n"
        "    def method(self):\n"
        "        import method_dependency\n"
        "def function():\n"
        "    import function_dependency\n"
    )
    observed = {
        alias.name
        for node in _module_scope_import_nodes(fixture)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert observed == {"packaging", "class_dependency"}


def test_adapter_import_boundary_is_stdlib_only():
    tree = ast.parse(environment.ADAPTER_PATH.read_text(encoding="utf-8"))
    function_types = (ast.FunctionDef, ast.AsyncFunctionDef)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, function_types)
    }
    governed_roots = {
        "validate_prefixcommons_input",
        "derive_prefixcommons_wheel",
        "validate_derived_prefixcommons_wheel",
        "validate_derivation_outputs",
        "_derivation_main",
        "derivation_command",
    }
    missing = sorted(governed_roots - functions.keys())
    assert missing == []

    reachable = set()
    pending = list(governed_roots)
    while pending:
        name = pending.pop()
        if name in reachable:
            continue
        reachable.add(name)
        for node in ast.walk(functions[name]):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in functions
                and node.func.id not in reachable
            ):
                pending.append(node.func.id)

    imports = []
    inspected = _module_scope_import_nodes(tree)
    for name in sorted(reachable):
        inspected.extend(
            node
            for node in ast.walk(functions[name])
            if isinstance(node, (ast.Import, ast.ImportFrom))
        )
    for node in inspected:
        if isinstance(node, ast.Import):
            imports.extend(
                (alias.name.partition(".")[0], node.lineno)
                for alias in node.names
            )
            continue
        root = (
            node.module.partition(".")[0]
            if node.level == 0 and node.module is not None
            else ""
        )
        imports.append((root, node.lineno))
    allowed = {*sys.stdlib_module_names, "__future__"}
    disallowed = [
        {"root": root, "line": line}
        for root, line in imports
        if root not in allowed
    ]
    assert disallowed == []


def test_prefixcommons_derivation_changes_only_allowlisted_bytes_and_archive_fields(
    tmp_path, monkeypatch
):
    upstream = tmp_path / "prefixcommons-0.1.12-py3-none-any.whl"
    derived = tmp_path / "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    _prefixcommons_upstream_wheel(upstream)
    _select_prefixcommons_fixture(monkeypatch, upstream)

    environment.validate_prefixcommons_input(upstream)
    environment.derive_prefixcommons_wheel(upstream, derived)
    record = environment.validate_derived_prefixcommons_wheel(derived)
    assert record["distribution"] == "prefixcommons"
    assert record["version"] == "0.1.12+malleus.1"

    upstream_dist = "prefixcommons-0.1.12.dist-info"
    derived_dist = "prefixcommons-0.1.12+malleus.1.dist-info"
    with zipfile.ZipFile(upstream) as source_archive:
        upstream_infos = source_archive.infolist()
        upstream_sources = {
            info.filename: source_archive.read(info)
            for info in upstream_infos
        }
    assert all(
        info.external_attr >> 16 == 0o644
        for info in upstream_infos
        if ".dist-info/" in info.filename
    )
    with zipfile.ZipFile(derived) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        sources = {info.filename: archive.read(info) for info in infos}
        assert archive.comment == b""

    assert names == sorted(names)
    assert all(name.encode("ascii").decode("ascii") == name for name in names)
    assert len(names) == 14
    assert f"{upstream_dist}/METADATA" not in names
    assert f"{derived_dist}/METADATA" in names
    for name, payload in _PREFIXCOMMONS_PAYLOADS.items():
        assert sources[name] == payload == upstream_sources[name]
    assert sources[f"{derived_dist}/LICENSE"] == upstream_sources[
        f"{upstream_dist}/LICENSE"
    ]
    assert sources[f"{derived_dist}/LICENSE"].startswith(b"BSD 3-Clause License")
    assert sources[f"{derived_dist}/METADATA"] == _PREFIXCOMMONS_METADATA.replace(
        b"Version: 0.1.12\n", b"Version: 0.1.12+malleus.1\n", 1
    ).replace(
        b"Requires-Dist: pytest-logging (>=2015.11.4,<2016.0.0)\n",
        b"",
        1,
    )
    assert sources[f"{derived_dist}/WHEEL"] == _PREFIXCOMMONS_WHEEL.replace(
        b"Generator: poetry 1.0.7\n",
        b"Generator: malleus-cc002 (wheel-derivation-v1)\n",
        1,
    )

    record_name = f"{derived_dist}/RECORD"
    without_record = {name: source for name, source in sources.items() if name != record_name}
    record_source = sources[record_name]
    assert not record_source.startswith(b"\xef\xbb\xbf")
    assert record_source.endswith(b"\n")
    assert record_source == _record_source(without_record, record_name)
    rows = list(
        csv.reader(
            io.StringIO(record_source.decode("utf-8"), newline=""),
            delimiter=",",
            quotechar='"',
            doublequote=True,
            escapechar=None,
            quoting=csv.QUOTE_MINIMAL,
        )
    )
    assert [row[0] for row in rows] == names
    assert all(len(row) == 3 for row in rows)
    assert next(row for row in rows if row[0] == record_name) == [
        record_name,
        "",
        "",
    ]
    for name, digest, length in (row for row in rows if row[0] != record_name):
        expected = base64.urlsafe_b64encode(hashlib.sha256(sources[name]).digest())
        assert digest == "sha256=" + expected.rstrip(b"=").decode("ascii")
        assert "=" not in digest.removeprefix("sha256=")
        assert length == str(len(sources[name]))

    for info in infos:
        assert info.date_time == (1980, 1, 1, 0, 0, 0)
        assert info.compress_type == zipfile.ZIP_STORED
        assert info.create_system == 3
        assert info.create_version == 20
        assert info.extract_version == 20
        assert info.reserved == 0
        assert info.flag_bits == 0
        assert info.volume == 0
        assert info.internal_attr == 0
        assert info.external_attr == 0o100644 << 16
        assert info.extra == b""
        assert info.comment == b""
        assert info.compress_size == info.file_size == len(sources[info.filename])
        assert info.CRC == zlib.crc32(sources[info.filename])


@pytest.mark.parametrize(
    "mutation",
    (
        "whole-wheel",
        "duplicate-name",
        "unsafe-name",
        "nonregular-member",
        "record",
        "metadata-target",
        "wheel-target",
        "license",
        "zip64",
    ),
)
def test_prefixcommons_derivation_rejects_tamper_before_external_edges(
    tmp_path, monkeypatch, mutation
):
    upstream = tmp_path / "prefixcommons-0.1.12-py3-none-any.whl"
    expected = tmp_path / "expected-prefixcommons-0.1.12-py3-none-any.whl"
    _prefixcommons_upstream_wheel(expected)
    options: dict[str, Any] = {}
    if mutation == "duplicate-name":
        options["duplicate_member"] = True
    elif mutation == "unsafe-name":
        options["raw_name"] = "../prefixes.csv"
    elif mutation == "nonregular-member":
        options["member_mode"] = stat.S_IFLNK | 0o777
    elif mutation == "record":
        options["record_mutation"] = "hash"
    elif mutation == "metadata-target":
        options["metadata"] = _PREFIXCOMMONS_METADATA.replace(
            b"Version: 0.1.12\n", b"Version: 9.9.9\n"
        )
    elif mutation == "wheel-target":
        options["wheel"] = _PREFIXCOMMONS_WHEEL.replace(
            b"Generator: poetry 1.0.7\n", b"Generator: unknown\n"
        )
    elif mutation == "license":
        options["license_source"] = None
    _prefixcommons_upstream_wheel(upstream, **options)
    if mutation == "record":
        record_name = "prefixcommons-0.1.12.dist-info/RECORD"
        with zipfile.ZipFile(expected) as expected_archive:
            expected_record = expected_archive.read(record_name)
        with zipfile.ZipFile(upstream) as changed_archive:
            changed_record = changed_archive.read(record_name)
        assert changed_record != expected_record
        assert len(changed_record) == len(expected_record)
    _select_prefixcommons_fixture(monkeypatch, upstream, facts_path=expected)
    if mutation == "whole-wheel":
        upstream.write_bytes(upstream.read_bytes() + b"tamper")
    if mutation == "zip64":
        monkeypatch.setattr(environment.zipfile, "ZIP64_LIMIT", 1)

    external_edges = []

    def tripwire(*_args, **_kwargs):
        external_edges.append(True)
        raise AssertionError("external edge reached before local validation")

    monkeypatch.setattr(environment, "_run_checked", tripwire)
    monkeypatch.setattr(environment, "download_artifact", tripwire)
    target = tmp_path / "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    with pytest.raises(environment.CC002Error, match="PREFIXCOMMONS|DERIVATION"):
        environment.derive_prefixcommons_wheel(upstream, target)
    assert external_edges == []
    assert not target.exists()


@pytest.mark.parametrize(
    "mutation",
    (
        "member-order",
        "timestamp",
        "compression",
        "create-system",
        "create-version",
        "extract-version",
        "reserved",
        "flag-bits",
        "volume",
        "internal-attr",
        "external-attr",
        "member-extra",
        "member-comment",
        "archive-comment",
        "record-order",
        "record-bom",
        "record-crlf",
        "record-terminal",
        "record-digest",
        "record-size",
        "record-self-hash",
        "record-self-size",
        "record-fields",
        "unsupported-version-needed",
        "zip64-header",
        "zip64-directory",
    ),
)
def test_derived_prefixcommons_validator_rejects_every_archive_grammar_drift(
    tmp_path, monkeypatch, mutation
):
    upstream = tmp_path / "prefixcommons-0.1.12-py3-none-any.whl"
    derived = tmp_path / "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    _prefixcommons_upstream_wheel(upstream)
    _select_prefixcommons_fixture(monkeypatch, upstream)
    environment.derive_prefixcommons_wheel(upstream, derived)
    _rewrite_derived_wheel(derived, mutation, monkeypatch)
    expected_code = (
        r"^\[CC002_DERIVED_ARCHIVE\]"
        if mutation == "unsupported-version-needed"
        else "RECORD|ARCHIVE|DERIVED"
    )
    with pytest.raises(environment.CC002Error, match=expected_code):
        environment.validate_derived_prefixcommons_wheel(derived)


@pytest.mark.parametrize(
    "compression",
    (zipfile.ZIP_DEFLATED, zipfile.ZIP_LZMA),
    ids=("corrupt-deflate", "corrupt-lzma"),
)
def test_prefixcommons_decoder_errors_use_governed_archive_error(
    tmp_path, monkeypatch, compression
):
    facts = tmp_path / "valid-prefixcommons.whl"
    upstream = tmp_path / "prefixcommons-0.1.12-py3-none-any.whl"
    _prefixcommons_upstream_wheel(facts)
    _prefixcommons_upstream_wheel(upstream, compression=compression)
    _corrupt_first_compressed_member(upstream, compression)
    _select_prefixcommons_fixture(monkeypatch, upstream, facts_path=facts)

    with pytest.raises(
        environment.CC002Error,
        match=r"^\[CC002_PREFIXCOMMONS_ARCHIVE\]",
    ):
        environment.validate_prefixcommons_input(upstream)


def test_derived_prefixcommons_expansion_is_rejected_before_member_reads(
    tmp_path, monkeypatch
):
    upstream = tmp_path / "prefixcommons-0.1.12-py3-none-any.whl"
    derived = tmp_path / "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    _prefixcommons_upstream_wheel(upstream)
    _select_prefixcommons_fixture(monkeypatch, upstream)
    environment.derive_prefixcommons_wheel(upstream, derived)
    _rewrite_derived_wheel(derived, "inflated-payload", monkeypatch)
    reads = []

    def forbidden_read(*_args, **_kwargs):
        reads.append("member")
        raise AssertionError("member payload read before expansion validation")

    def forbidden_whole_file_read(*_args, **_kwargs):
        reads.append("archive")
        raise AssertionError("whole archive read before expansion validation")

    monkeypatch.setattr(zipfile.ZipFile, "read", forbidden_read)
    monkeypatch.setattr(Path, "read_bytes", forbidden_whole_file_read)
    with pytest.raises(environment.CC002Error, match="ARCHIVE|expansion"):
        environment.validate_derived_prefixcommons_wheel(derived)
    assert reads == []


def test_prefixcommons_derivation_is_zip_only_without_import_extract_or_execution(
    tmp_path, monkeypatch
):
    derivative_inputs = tmp_path / "derivative-inputs"
    derivative_inputs.mkdir()
    upstream = derivative_inputs / "prefixcommons-0.1.12-py3-none-any.whl"
    derived = tmp_path / "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    child_output = tmp_path / "child-output"
    child_output.mkdir()
    _prefixcommons_upstream_wheel(upstream)
    _select_prefixcommons_fixture(monkeypatch, upstream)
    forbidden_calls = []
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        root_name = name.partition(".")[0]
        if root_name not in sys.stdlib_module_names:
            forbidden_calls.append(("import", name))
            raise AssertionError(f"non-stdlib import reached: {name}")
        return original_import(name, *args, **kwargs)

    def tripwire(name):
        def fail(*_args, **_kwargs):
            forbidden_calls.append((name, None))
            raise AssertionError(f"forbidden derivation path reached: {name}")

        return fail

    prior_umask = os.umask(0o077)
    try:
        with monkeypatch.context() as guard:
            guard.setattr(builtins, "__import__", guarded_import)
            guard.setattr(builtins, "exec", tripwire("exec"))
            guard.setattr(builtins, "eval", tripwire("eval"))
            guard.setattr(zipfile.ZipFile, "extract", tripwire("extract"))
            guard.setattr(zipfile.ZipFile, "extractall", tripwire("extractall"))
            guard.setattr(environment.subprocess, "run", tripwire("subprocess.run"))
            guard.setattr(environment.subprocess, "Popen", tripwire("subprocess.Popen"))
            guard.setattr(environment.os, "system", tripwire("os.system"))
            guard.setattr(environment, "_run_checked", tripwire("_run_checked"))
            guard.setattr(environment, "run_fixed", tripwire("run_fixed"))
            guard.setattr(environment, "download_artifact", tripwire("download"))
            guard.setattr(
                environment,
                "DERIVATION_INPUT_ROOT",
                derivative_inputs,
                raising=False,
            )
            guard.setattr(
                environment,
                "DERIVATION_OUTPUT_ROOT",
                child_output,
                raising=False,
            )
            guard.setattr(
                environment,
                "_observe_derivation_child",
                _selected_derivation_observation,
            )
            environment.validate_prefixcommons_input(upstream)
            environment.derive_prefixcommons_wheel(upstream, derived)
            environment.validate_derived_prefixcommons_wheel(derived)
            assert environment._derivation_main() == 0
    finally:
        os.umask(prior_umask)
    assert forbidden_calls == []
    assert (child_output / environment.PREFIXCOMMONS_DERIVED_FILENAME).is_file()


def test_derivation_command_and_two_outputs_are_fresh_hardened_and_byte_equal(
    tmp_path, monkeypatch
):
    derivative_inputs = tmp_path / "derivative-inputs"
    derivative_inputs.mkdir()
    upstream = derivative_inputs / "prefixcommons-0.1.12-py3-none-any.whl"
    _prefixcommons_upstream_wheel(upstream)
    _select_prefixcommons_fixture(monkeypatch, upstream)
    outputs = [tmp_path / "derive-1", tmp_path / "derive-2"]
    for output in outputs:
        output.mkdir()

    commands = [
        environment.derivation_command(
            derivative_inputs,
            output,
            host_user={"uid": 501, "gid": 20},
        )
        for output in outputs
    ]
    for command, output in zip(commands, outputs, strict=True):
        assert command[:2] == ["docker", "run"]
        assert command[command.index("--network") + 1] == "none"
        assert command[command.index("--user") + 1] == "501:20"
        assert "--read-only" in command
        assert command[command.index("--cap-drop") + 1] == "ALL"
        assert command[command.index("--security-opt") + 1] == "no-new-privileges"
        assert f"SOURCE_DATE_EPOCH={environment.SOURCE_DATE_EPOCH}" in command
        assert "TZ=UTC" in command
        assert "PYTHONHASHSEED=0" in command
        assert f"{derivative_inputs.resolve()}:/derivative-inputs:ro" in command
        assert f"{output.resolve()}:/output:rw" in command
        assert environment.OCI_CHILD_REFERENCE in command
        assert command[-3:] == ["python", "-c", environment.DERIVATION_PROGRAM]
    assert commands[0] != commands[1]
    expected_facts = {
        "python": environment.PYTHON_TUPLE,
        "image": {
            "platform": environment.OCI_PLATFORM,
            "child_digest": environment.OCI_CHILD_DIGEST,
        },
        "tool": {
            "implementation": "python-stdlib",
            "generator": "malleus-cc002 (wheel-derivation-v1)",
            "adapter_sha256": "sha256:"
            + hashlib.sha256(environment.ADAPTER_PATH.read_bytes()).hexdigest(),
        },
        "environment": {
            "source_date_epoch": 315532800,
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
    assert environment.EXPECTED_DERIVATION_CHILD_FACTS == expected_facts
    assert environment.RETAINED_DERIVATION_RUN == expected_facts

    observed_umasks = []
    actual_umask = environment.os.umask

    def measured_umask(value):
        observed_umasks.append(value)
        return actual_umask(value)

    prior_umask = os.umask(0o077)
    try:
        monkeypatch.setattr(environment.os, "umask", measured_umask)
        for output in outputs:
            _run_derivation_program(monkeypatch, derivative_inputs, output)
    finally:
        actual_umask(prior_umask)
    assert observed_umasks.count(0o022) == 2
    for output in outputs:
        output_path = output / environment.PREFIXCOMMONS_DERIVED_FILENAME
        facts = json.loads((output / ".cc002-derivation-facts.json").read_text())
        assert facts == {
            **expected_facts,
            "output": environment._artifact_record(output_path),
        }
    retained = environment.validate_derivation_outputs(*outputs)
    assert retained["filename"] == (
        "prefixcommons-0.1.12+malleus.1-py3-none-any.whl"
    )
    assert retained["version"] == "0.1.12+malleus.1"
    second = outputs[1] / retained["filename"]
    second.write_bytes(second.read_bytes() + b"changed")
    with pytest.raises(environment.CC002Error, match="REPRODUCIBILITY|DERIVATION"):
        environment.validate_derivation_outputs(*outputs)


@pytest.mark.parametrize(
    "mutation",
    (
        "alias",
        "missing",
        "extra",
        "bytes",
        "facts-tool",
        "facts-digest",
        "facts-python",
        "facts-image",
        "facts-environment",
        "facts-isolation",
        "facts-output",
    ),
)
def test_derivation_outputs_reject_alias_content_and_measured_provenance_drift(
    tmp_path, monkeypatch, mutation
):
    derivative_inputs = tmp_path / "derivative-inputs"
    derivative_inputs.mkdir()
    upstream = derivative_inputs / "prefixcommons-0.1.12-py3-none-any.whl"
    _prefixcommons_upstream_wheel(upstream)
    _select_prefixcommons_fixture(monkeypatch, upstream)
    outputs = [tmp_path / "derive-1", tmp_path / "derive-2"]
    for output in outputs:
        output.mkdir()
        _run_derivation_program(monkeypatch, derivative_inputs, output)
    if mutation == "alias":
        alias = tmp_path / "derive-alias"
        alias.symlink_to(outputs[0], target_is_directory=True)
        outputs[1] = alias
        assert outputs[0] != outputs[1]
        assert outputs[0].resolve() == outputs[1].resolve()
    elif mutation == "missing":
        (outputs[1] / environment.PREFIXCOMMONS_DERIVED_FILENAME).unlink()
    elif mutation == "extra":
        (outputs[1] / "unexpected").write_bytes(b"unexpected")
    elif mutation == "bytes":
        path = outputs[1] / environment.PREFIXCOMMONS_DERIVED_FILENAME
        path.write_bytes(path.read_bytes() + b"changed")
    else:
        facts_path = outputs[1] / ".cc002-derivation-facts.json"
        facts = json.loads(facts_path.read_text())
        if mutation == "facts-tool":
            facts["tool"]["implementation"] = "third-party"
        elif mutation == "facts-digest":
            facts["tool"]["adapter_sha256"] = "sha256:" + "0" * 64
        elif mutation == "facts-python":
            facts["python"]["version"] = "3.12.11"
        elif mutation == "facts-image":
            facts["image"]["child_digest"] = "sha256:" + "0" * 64
        elif mutation == "facts-environment":
            facts["environment"]["tz"] = "LOCAL"
        elif mutation == "facts-isolation":
            facts["isolation"]["network"] = "BRIDGE"
        else:
            facts["output"]["sha256"] = "sha256:" + "0" * 64
        facts_path.write_text(
            environment.canonical_json(facts) + "\n", encoding="utf-8"
        )
    with pytest.raises(environment.CC002Error, match="DERIVATION|REPRODUCIBILITY"):
        environment.validate_derivation_outputs(*outputs)


@pytest.mark.parametrize(
    "relationship",
    ("same", "output-under-input", "input-under-output"),
)
def test_derivation_command_refuses_overlapping_mount_sources(
    tmp_path, relationship
):
    derivative_inputs = tmp_path / "derivative-inputs"
    output = tmp_path / "output"
    if relationship == "same":
        output = derivative_inputs
    elif relationship == "output-under-input":
        output = derivative_inputs / "output"
    else:
        derivative_inputs = output / "derivative-inputs"
    derivative_inputs.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    with pytest.raises(environment.CC002Error, match="MOUNTS|overlap|distinct"):
        environment.derivation_command(
            derivative_inputs,
            output,
            host_user={"uid": 501, "gid": 20},
        )


@pytest.mark.parametrize(
    "relationship", ("same", "output-contains", "adapter-contains")
)
def test_derivation_command_refuses_writable_output_overlap_with_adapter(
    tmp_path, monkeypatch, relationship
):
    derivative_inputs = tmp_path / "derivative-inputs"
    derivative_inputs.mkdir()
    adapter_root = tmp_path / "adapter"
    adapter_root.mkdir()
    adapter = adapter_root / "contract_compiler_environment.py"
    adapter.write_text("fixture\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()
    if relationship == "same":
        monkeypatch.setattr(environment, "ADAPTER_PATH", output)
    elif relationship == "output-contains":
        output = adapter_root
        monkeypatch.setattr(environment, "ADAPTER_PATH", adapter)
    else:
        nested_output = adapter_root / "output"
        nested_output.mkdir()
        output = nested_output
        monkeypatch.setattr(environment, "ADAPTER_PATH", adapter_root)
    with pytest.raises(environment.CC002Error, match="MOUNTS|overlap"):
        environment.derivation_command(
            derivative_inputs,
            output,
            host_user={"uid": 501, "gid": 20},
        )


def test_antlr_sdist_validation_refuses_unsafe_archive_member(tmp_path, monkeypatch):
    path = tmp_path / environment.ANTLR_SDIST_FILENAME
    unsafe = tarfile.TarInfo("../escape")
    unsafe.size = 1
    source = _antlr_sdist(path, unsafe=unsafe)
    selected = environment.SelectedArtifact(
        filename=path.name,
        kind="SDIST",
        url="https://files.pythonhosted.org/fixture/source.tar.gz",
        byte_length=len(source),
        sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (selected, environment.BUILD_ARTIFACTS[1]))
    monkeypatch.setattr(environment, "ANTLR_SDIST_MEMBER_COUNT", 2)
    monkeypatch.setattr(environment, "ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH", 107)
    with pytest.raises(environment.CC002Error, match="SDIST_SAFETY"):
        environment.validate_antlr_sdist(path)


@pytest.mark.parametrize("member_type", (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE))
def test_antlr_sdist_refuses_link_and_fifo_members(tmp_path, monkeypatch, member_type):
    path = tmp_path / environment.ANTLR_SDIST_FILENAME
    unsafe = tarfile.TarInfo("antlr4-python3-runtime-4.9.3/unsafe")
    unsafe.type = member_type
    unsafe.linkname = "target"
    source = _antlr_sdist(path, unsafe=unsafe)
    selected = environment.SelectedArtifact(
        filename=path.name, kind="SDIST", url="https://files.pythonhosted.org/fixture/source.tar.gz",
        byte_length=len(source), sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (selected, environment.BUILD_ARTIFACTS[1]))
    with pytest.raises(environment.CC002Error, match="SDIST_SAFETY"):
        environment.validate_antlr_sdist(path)


def test_antlr_sdist_validation_refuses_backslash_member(tmp_path, monkeypatch):
    path = tmp_path / environment.ANTLR_SDIST_FILENAME
    unsafe = tarfile.TarInfo("antlr4-python3-runtime-4.9.3/evil\\path")
    unsafe.size = 1
    source = _antlr_sdist(path, unsafe=unsafe)
    selected = environment.SelectedArtifact(
        filename=path.name, kind="SDIST", url="https://files.pythonhosted.org/fixture/source.tar.gz",
        byte_length=len(source), sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (selected, environment.BUILD_ARTIFACTS[1]))
    with pytest.raises(environment.CC002Error, match="SDIST_SAFETY"):
        environment.validate_antlr_sdist(path)


def test_setuptools_build_input_is_structurally_validated(tmp_path, monkeypatch):
    path = tmp_path / environment.SETUPTOOLS_WHEEL_FILENAME
    _wheel(path, "different-backend", "83.0.0")
    source = path.read_bytes()
    selected = environment.SelectedArtifact(
        filename=path.name, kind="WHEEL", url="https://files.pythonhosted.org/fixture/setuptools.whl",
        byte_length=len(source), sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (environment.BUILD_ARTIFACTS[0], selected))
    with pytest.raises(environment.CC002Error, match="BUILD_INPUT"):
        environment.validate_setuptools_wheel(path)


def test_governed_source_build_artifact_coordinates_are_exact():
    assert environment.SOURCE_DATE_EPOCH == "315532800"
    assert environment.ANTLR_SDIST_MEMBER_COUNT == 78
    assert environment.ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH == 477312
    assert [artifact.as_dict() for artifact in environment.BUILD_ARTIFACTS] == [
        {
            "filename": "antlr4-python3-runtime-4.9.3.tar.gz",
            "kind": "SDIST",
            "url": "https://files.pythonhosted.org/packages/3e/38/7859ff46355f76f8d19459005ca000b6e7012f2f1ca597746cbcd1fbfe5e/antlr4-python3-runtime-4.9.3.tar.gz",
            "byte_length": 117034,
            "sha256": "f224469b4168294902bb1efa80a8bf7855f24c99aef99cbefc1bcd3cce77881b",
        },
        {
            "filename": "setuptools-83.0.0-py3-none-any.whl",
            "kind": "WHEEL",
            "url": "https://files.pythonhosted.org/packages/5d/40/e1e72872c6354b306daef1703549e8e83b4d43cfea356311bf722a043752/setuptools-83.0.0-py3-none-any.whl",
            "byte_length": 1008090,
            "sha256": "29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3",
        },
    ]


def test_antlr_sdist_validation_binds_layout_metadata_and_measured_limits(tmp_path, monkeypatch):
    path = tmp_path / environment.ANTLR_SDIST_FILENAME
    source = _antlr_sdist(path)
    selected = environment.SelectedArtifact(
        filename=path.name,
        kind="SDIST",
        url="https://files.pythonhosted.org/fixture/source.tar.gz",
        byte_length=len(source),
        sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (selected, environment.BUILD_ARTIFACTS[1]))
    monkeypatch.setattr(environment, "ANTLR_SDIST_MEMBER_COUNT", 2)
    with tarfile.open(path, "r:gz") as archive:
        total = sum(member.size for member in archive.getmembers())
    monkeypatch.setattr(environment, "ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH", total)
    facts = environment.validate_antlr_sdist(path)
    assert facts["member_count"] == 2
    assert facts["uncompressed_byte_length"] > 0


@pytest.mark.parametrize("field", ("count", "expanded"))
def test_antlr_sdist_refuses_member_count_and_expansion_changes(tmp_path, monkeypatch, field):
    path = tmp_path / environment.ANTLR_SDIST_FILENAME
    source = _antlr_sdist(path)
    selected = environment.SelectedArtifact(
        filename=path.name, kind="SDIST", url="https://files.pythonhosted.org/fixture/source.tar.gz",
        byte_length=len(source), sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (selected, environment.BUILD_ARTIFACTS[1]))
    with tarfile.open(path, "r:gz") as archive:
        members = archive.getmembers()
    monkeypatch.setattr(environment, "ANTLR_SDIST_MEMBER_COUNT", len(members) + (field == "count"))
    monkeypatch.setattr(
        environment,
        "ANTLR_SDIST_UNCOMPRESSED_BYTE_LENGTH",
        sum(member.size for member in members) + (field == "expanded"),
    )
    with pytest.raises(environment.CC002Error, match="SDIST_LIMIT"):
        environment.validate_antlr_sdist(path)


@pytest.mark.parametrize(
    ("extra", "setup_directory"),
    ((b"Name: conflicting\n", False), (b"Version: 9.9.9\n", False), (b"", True)),
)
def test_antlr_sdist_rejects_duplicate_metadata_or_nonfile_setup(
    tmp_path, monkeypatch, extra, setup_directory
):
    path = tmp_path / environment.ANTLR_SDIST_FILENAME
    source = _antlr_sdist(path, pkg_info_extra=extra, setup_directory=setup_directory)
    selected = environment.SelectedArtifact(
        filename=path.name, kind="SDIST", url="https://files.pythonhosted.org/fixture/source.tar.gz",
        byte_length=len(source), sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (selected, environment.BUILD_ARTIFACTS[1]))
    with pytest.raises(environment.CC002Error, match="SDIST_METADATA|SDIST_LAYOUT"):
        environment.validate_antlr_sdist(path)


@pytest.mark.parametrize(
    ("generator", "error"),
    [
        ("setuptools (82.0.0)", "METADATA"),
    ],
)
def test_built_antlr_wheel_refuses_wrong_generator(tmp_path, generator, error):
    path = tmp_path / "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(path, generator=generator)
    with pytest.raises(environment.CC002Error, match=error):
        environment.validate_built_antlr_wheel(path)


@pytest.mark.parametrize(
    "raw_name",
    (
        "..\\escape.py",
        "antlr4/evil\x1fname.py",
        "antlr4/./fixture.py",
        "antlr4//fixture.py",
    ),
)
def test_built_wheel_refuses_noncanonical_raw_member_names(tmp_path, raw_name):
    path = tmp_path / "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(path, extra_names=(raw_name,))
    with pytest.raises(environment.CC002Error, match="BUILT_WHEEL_SAFETY"):
        environment.validate_built_antlr_wheel(path)


def test_built_wheel_keeps_distinct_linux_unicode_member_spellings(tmp_path):
    path = tmp_path / "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(path, extra_names=("antlr4/café.py", "antlr4/cafe\u0301.py"))
    assert environment.validate_built_antlr_wheel(path)["version"] == "4.9.3"


@pytest.mark.parametrize("mutation", ("duplicate", "missing", "hash", "size"))
def test_built_wheel_refuses_record_corruption(tmp_path, mutation):
    path = tmp_path / "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(path, record_mutation=mutation)
    with pytest.raises(environment.CC002Error, match="BUILT_WHEEL_RECORD"):
        environment.validate_built_antlr_wheel(path)


@pytest.mark.parametrize("kind", ("symlink", "special", "encrypted", "count", "expanded"))
def test_wheel_member_safety_refuses_types_flags_and_bounds(kind):
    count = 1001 if kind == "count" else 1
    members = []
    for index in range(count):
        info = zipfile.ZipInfo(f"member-{index}")
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        if kind == "symlink":
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
        elif kind == "special":
            info.external_attr = (stat.S_IFIFO | 0o644) << 16
        elif kind == "encrypted":
            info.flag_bits = 1
        elif kind == "expanded":
            info.file_size = 16 * 1024 * 1024 + 1
        members.append(info)

    class Archive:
        def infolist(self):
            return members

    with pytest.raises(environment.CC002Error, match="CC002_TEST_WHEEL"):
        environment._safe_wheel_members(
            Archive(), "CC002_TEST_WHEEL", enforce_build_limits=True
        )


def test_wheel_member_safety_accepts_directory_entry_and_rejects_file_trailing_slash():
    directory = zipfile.ZipInfo("package/")
    directory.external_attr = (stat.S_IFDIR | 0o755) << 16

    class DirectoryArchive:
        def infolist(self):
            return [directory]

    assert environment._safe_wheel_members(
        DirectoryArchive(), "CC002_TEST_WHEEL", enforce_build_limits=True
    ) == [directory]

    with pytest.raises(environment.CC002Error, match="CC002_TEST_WHEEL"):
        environment._validate_archive_member_name(
            "package/", {}, "CC002_TEST_WHEEL", is_directory=False
        )


@pytest.mark.parametrize(
    ("name", "mode"),
    (("package/", stat.S_IFREG | 0o644), ("package", stat.S_IFDIR | 0o755)),
)
def test_wheel_member_safety_rejects_name_mode_type_confusion(name, mode):
    member = zipfile.ZipInfo(name)
    member.external_attr = mode << 16

    class Archive:
        def infolist(self):
            return [member]

    with pytest.raises(environment.CC002Error, match="CC002_TEST_WHEEL"):
        environment._safe_wheel_members(
            Archive(), "CC002_TEST_WHEEL", enforce_build_limits=True
        )


@pytest.mark.parametrize("file_first", (False, True))
def test_archive_topology_refuses_file_ancestor_in_both_orders(file_first):
    entries = [("antlr4", False), ("antlr4/__init__.py", False)]
    if not file_first:
        entries.reverse()
    topology = {}
    environment._validate_archive_member_name(
        entries[0][0], topology, "CC002_TEST_WHEEL", is_directory=entries[0][1]
    )
    with pytest.raises(environment.CC002Error, match="CC002_TEST_WHEEL"):
        environment._validate_archive_member_name(
            entries[1][0], topology, "CC002_TEST_WHEEL", is_directory=entries[1][1]
        )


def test_archive_topology_allows_declared_directory_ancestor():
    topology = {}
    environment._validate_archive_member_name(
        "antlr4/", topology, "CC002_TEST_WHEEL", is_directory=True
    )
    environment._validate_archive_member_name(
        "antlr4/__init__.py", topology, "CC002_TEST_WHEEL", is_directory=False
    )


def test_generic_runtime_wheel_safety_does_not_invent_build_resource_caps():
    members = [zipfile.ZipInfo(f"member-{index}") for index in range(1001)]

    class Archive:
        def infolist(self):
            return members

    assert environment._safe_wheel_members(
        Archive(), "CC002_WHEEL", enforce_build_limits=False
    ) == members


def test_wheel_safety_preserves_caller_error_taxonomy():
    unsafe = zipfile.ZipInfo("..\\escape")

    class Archive:
        def infolist(self):
            return [unsafe]

    with pytest.raises(environment.CC002Error, match=r"\[CC002_BUILD_INPUT\]"):
        environment._safe_wheel_members(
            Archive(), "CC002_BUILD_INPUT", enforce_build_limits=True
        )


@pytest.mark.parametrize(
    "raw_name",
    ("..\\escape.py", "antlr4-python3-runtime-4.9.3/evil\x1fname.py", "antlr4-python3-runtime-4.9.3/./x", "antlr4-python3-runtime-4.9.3//x"),
)
def test_antlr_sdist_refuses_noncanonical_raw_member_names(tmp_path, monkeypatch, raw_name):
    path = tmp_path / environment.ANTLR_SDIST_FILENAME
    unsafe = tarfile.TarInfo(raw_name)
    unsafe.size = 1
    source = _antlr_sdist(path, unsafe=unsafe)
    selected = environment.SelectedArtifact(
        filename=path.name, kind="SDIST", url="https://files.pythonhosted.org/fixture/source.tar.gz",
        byte_length=len(source), sha256=hashlib.sha256(source).hexdigest(),
    )
    monkeypatch.setattr(environment, "BUILD_ARTIFACTS", (selected, environment.BUILD_ARTIFACTS[1]))
    with pytest.raises(environment.CC002Error, match="SDIST_SAFETY"):
        environment.validate_antlr_sdist(path)


def test_single_built_wheel_accepts_source_mtime_while_two_runs_require_equal_bytes(tmp_path):
    first = tmp_path / "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(first, timestamp=(2021, 1, 1, 0, 0, 0))
    assert environment.validate_built_antlr_wheel(first)["version"] == "4.9.3"


def test_two_builds_require_exactly_one_valid_byte_identical_wheel(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    name = "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(first / name)
    _built_antlr_wheel(second / name)
    _write_build_facts(first)
    _write_build_facts(second)
    record = environment.validate_build_outputs(first, second)
    assert record["distribution"] == "antlr4-python3-runtime"
    (second / name).write_bytes((second / name).read_bytes() + b"changed")
    with pytest.raises(environment.CC002Error, match="REPRODUCIBILITY|BUILT_WHEEL"):
        environment.validate_build_outputs(first, second)


@pytest.mark.parametrize("alias", (False, True))
def test_two_builds_require_distinct_resolved_output_directories(tmp_path, alias):
    output = tmp_path / "build"
    output.mkdir()
    name = "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(output / name)
    _write_build_facts(output)
    second = output / ".." / "build" if alias else output
    with pytest.raises(environment.CC002Error, match="distinct"):
        environment.validate_build_outputs(output, second)


def test_build_outputs_require_equal_observed_child_facts(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    name = "antlr4_python3_runtime-4.9.3-py3-none-any.whl"
    _built_antlr_wheel(first / name)
    _built_antlr_wheel(second / name)
    facts = _build_facts()
    for output in (first, second):
        (output / ".cc002-build-facts.json").write_text(json.dumps(facts), encoding="utf-8")
    record = environment.validate_build_outputs(first, second)
    assert record["distribution"] == "antlr4-python3-runtime"
    facts["python"] = {**environment.PYTHON_TUPLE, "version": "3.12.11"}
    (second / ".cc002-build-facts.json").write_text(json.dumps(facts), encoding="utf-8")
    with pytest.raises(environment.CC002Error, match="BUILD_FACTS"):
        environment.validate_build_outputs(first, second)


def test_source_build_command_is_two_run_network_none_hardened_and_fixed(tmp_path, monkeypatch):
    inputs = tmp_path / "inputs"
    roots = tmp_path / "roots"
    output = tmp_path / "output"
    for directory in (inputs, roots, output):
        directory.mkdir()
    (roots / environment.PIP_WHEEL_FILENAME).write_bytes(b"pip")
    command = environment.build_command(inputs, roots, output, host_user={"uid": 501, "gid": 20})
    assert command[:2] == ["docker", "run"]
    assert command[command.index("--network") + 1] == "none"
    assert command[command.index("--user") + 1] == "501:20"
    assert "--read-only" in command
    assert command[command.index("--cap-drop") + 1] == "ALL"
    assert command[command.index("--security-opt") + 1] == "no-new-privileges"
    assert f"SOURCE_DATE_EPOCH={environment.SOURCE_DATE_EPOCH}" in command
    assert "/tmp:rw,noexec,nosuid,nodev" in command
    assert "--no-build-isolation" in environment.BUILD_PROGRAM
    assert "--use-pep517" in environment.BUILD_PROGRAM
    assert "setuptools-83.0.0-py3-none-any.whl" in environment.BUILD_PROGRAM
    assert "venv" not in environment.BUILD_PROGRAM


@pytest.mark.parametrize(
    "case",
    ("output-equal-input", "output-under-input", "input-under-output", "input-under-roots", "roots-under-input"),
)
def test_source_build_command_refuses_overlapping_mount_sources(tmp_path, case):
    inputs = tmp_path / "inputs"
    roots = tmp_path / "roots"
    output = tmp_path / "output"
    if case == "output-equal-input":
        output = inputs
    elif case == "output-under-input":
        output = inputs / "output"
    elif case == "input-under-output":
        inputs = output / "inputs"
    elif case == "input-under-roots":
        inputs = roots / "inputs"
    elif case == "roots-under-input":
        roots = inputs / "roots"
    with pytest.raises(environment.CC002Error, match="overlap"):
        environment.build_command(
            inputs, roots, output, host_user={"uid": 501, "gid": 20}
        )


def test_source_build_program_proves_exact_frontend_and_backend_target():
    program = environment.BUILD_PROGRAM
    assert "pip.__version__" in program
    assert "pip.__file__" in program
    assert "/pip/pip-25.0.1-py3-none-any.whl/pip/__init__.py" in program
    assert "setuptools.__version__" in program
    assert "setuptools.__file__" in program
    assert "setuptools.build_meta" in program
    assert "__legacy__" in program
    assert "--target=/tmp/cc002-backend" in program
    assert "target.iterdir()" in program
    assert "is_symlink()" in program
    assert "distributions(path=[str(target)])" in program
    assert "[('setuptools', '83.0.0')]" in program
    assert "'/pip/pip-25.0.1-py3-none-any.whl:/tmp/cc002-backend'" in program
    assert "os.umask(0o022)" in program
    assert "'umask': '022'" in program
    assert "'backend_interface': 'setuptools.build_meta:__legacy__'" in program
    assert "'no_build_isolation': True" in program
    assert "'tz': 'UTC'" in program
    assert "'python_hash_seed': '0'" in program
    assert "'PYTHONNOUSERSITE': '1'" in program
    assert "home.mkdir(mode=0o700)" in program
    assert "'PYTHONSAFEPATH': '1'" in program
    assert "'python', '-P', '-S', '-m', 'pip', 'wheel'" in program
    assert "cwd='/tmp'" in program
    assert "cwd=str(project)" not in program
