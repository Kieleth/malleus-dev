"""CC-002 compiler-environment MCP and offline materialization gates."""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tomllib
import types
import zipfile
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
            artifact_count=5,
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


def _wheel(path: Path, name: str, version: str, requires: tuple[str, ...] = ()) -> None:
    metadata = [
        "Metadata-Version: 2.4",
        f"Name: {name}",
        f"Version: {version}",
        *(f"Requires-Dist: {requirement}" for requirement in requires),
        "",
        "",
    ]
    dist = name.replace("-", "_")
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(f"{dist}-{version}.dist-info/METADATA", "\n".join(metadata))


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
            "serverInfo": {"name": "malleus-cc002", "version": "1"},
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
        "const": "malleus.cc002.acquire-result/v1"
    }
    assert acquire["properties"]["state"] == {"const": "MATERIALIZED"}
    assert verify["additionalProperties"] is False
    assert set(verify["required"]) == set(verify["properties"])
    assert verify["properties"]["schema"] == {
        "const": "malleus.cc002.verify-result/v1"
    }
    assert verify["properties"]["state"] == {"const": "VERIFIED_OFFLINE"}
    for schema in (acquire, verify):
        for name, value in schema["properties"].items():
            if name.endswith("sha256") or name.endswith("digest"):
                assert value.get("pattern") is None


def test_result_constructors_refuse_bad_digests_counts_and_unknown_service_output():
    with pytest.raises(environment.CC002Error, match="lowercase hexadecimal"):
        environment.acquire_result(
            artifact_count=5,
            wheel_count=1,
            lock_sha256="sha256:" + "G" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )
    with pytest.raises(environment.CC002Error, match="artifact_count"):
        environment.acquire_result(
            artifact_count=True,
            wheel_count=1,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )
    with pytest.raises(environment.CC002Error, match="exactly five"):
        environment.acquire_result(
            artifact_count=6,
            wheel_count=1,
            lock_sha256="sha256:" + "1" * 64,
            wheelhouse_sha256="sha256:" + "2" * 64,
        )

    class InvalidServices(FakeServices):
        def acquire(self):
            return {"schema": "malleus.cc002.acquire-result/v1"}

    response = environment.handle_message(_call("cc002_acquire"), InvalidServices())
    assert response["result"]["isError"] is True
    assert "CC002_RESULT" in response["result"]["content"][0]["text"]


@pytest.mark.parametrize(
    ("name", "expected_call", "schema"),
    [
        ("cc002_acquire", "acquire", "malleus.cc002.acquire-result/v1"),
        (
            "cc002_verify_offline",
            "verify",
            "malleus.cc002.verify-result/v1",
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
    pull = environment.image_pull_command()
    resolve = environment.resolve_command(roots, wheelhouse)
    verify = environment.verify_command(tmp_path / "bundle", tmp_path / "work")
    assert pull[-3:] == ["--platform", "linux/amd64", environment.OCI_CHILD_REFERENCE]
    assert "--platform" in resolve and "linux/amd64" in resolve
    assert "--network" in resolve and "bridge" in resolve
    assert "--pull=never" in resolve
    assert environment.OCI_CHILD_REFERENCE in resolve
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
    assert "/repo" not in environment.VERIFIER_PROGRAM
    assert "--no-index" in environment.VERIFIER_PROGRAM
    assert "--require-hashes" in environment.VERIFIER_PROGRAM


def test_every_container_run_uses_the_exact_nonroot_host_ownership_tuple(tmp_path):
    expected = f"{os.getuid()}:{os.getgid()}"
    commands = (
        environment.resolve_command(tmp_path / "roots", tmp_path / "wheelhouse"),
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
    command = environment.resolve_command(roots, wheelhouse)
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


def _fake_cc002_edges(tmp_path, monkeypatch, registry_failure_url=None):
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
        if "transitive wheel resolution" == context:
            return b""
        raise AssertionError(f"unexpected external edge: {context}: {arguments}")

    monkeypatch.setattr(environment, "DESTINATION", destination)
    monkeypatch.setattr(environment, "OUTPUT_TRUSTED_ROOT", tmp_path)
    monkeypatch.setattr(environment, "INTERNAL_VERIFICATION", destination / "verification.json")
    monkeypatch.setattr(environment, "SMOKE_INPUT", smoke)
    monkeypatch.setattr(environment, "SELECTED_ARTIFACTS", tuple(artifacts))
    monkeypatch.setattr(environment, "_default_opener", lambda: RoutingOpener())
    monkeypatch.setattr(environment, "_resolved_docker", lambda: "/fixture/bin/docker")
    monkeypatch.setattr(environment, "parse_oci_index", lambda source: calls.append("parse OCI index") or environment.OCI_CHILD_DIGEST)
    monkeypatch.setattr(environment, "_run_checked", fake_run)
    return destination, calls


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


def test_acquire_orchestrates_report_manifest_round_trip_and_idempotence(
    tmp_path, monkeypatch
):
    destination, calls = _fake_cc002_edges(tmp_path, monkeypatch)
    result = environment.acquire_environment()
    assert result["artifact_count"] == 5
    assert calls == [
        "Docker version",
        "parse OCI index",
        "OCI child pull",
        "local image inspection",
        "transitive wheel resolution",
        "offline root resolution report",
    ]
    manifest, _source = environment._validated_environment(destination)
    assert manifest["resolution_report"]["filename"] == "resolution-report.json"
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
    assert len(distributions) == 3
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
    assert "input(" not in source
    assert "argparse" not in source
    assert "requests" not in source
    assert 'DOCKER = "/' not in source
    assert "Path.home()" not in source
    assert str(Path.home()) not in source
    assert "import re" not in source
