from __future__ import annotations

import builtins
import errno
from pathlib import Path
from typing import Any

import hbreader
import pytest
from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.loaders import YAMLLoader
from linkml_runtime.utils.schemaview import SchemaView


def _schema(name: str, imports: tuple[str, ...] = ()) -> SchemaDefinition:
    return SchemaDefinition(
        id=f"https://example.test/{name}",
        name=name,
        imports=list(imports),
    )


class _MemorySchemaView(SchemaView):
    def __init__(
        self,
        root: SchemaDefinition,
        imported: dict[str, SchemaDefinition],
    ) -> None:
        super().__init__(root)
        self._imported = imported

    def load_import(
        self,
        imp: str,
        from_schema: SchemaDefinition | None = None,
    ) -> SchemaDefinition:
        del from_schema
        return self._imported[imp]


def test_yaml_loader_loads_receives_the_exact_source_text() -> None:
    source_text = (
        "id: https://example.test/root\n"
        "name: root\n"
        "description: |\n"
        "  first line\n"
        "  second line  \n"
        "classes: {}\n"
    )
    observed: list[Any] = []

    class RecordingYAMLLoader(YAMLLoader):
        def _read_source(self, source: Any, **kwargs: Any) -> dict[str, Any] | str:
            observed.append(source)
            return super()._read_source(source, **kwargs)

    schema = RecordingYAMLLoader().loads(
        source_text,
        target_class=SchemaDefinition,
    )

    assert len(observed) == 1
    assert observed[0] is source_text
    assert observed[0] == source_text
    assert schema.name == "root"


def test_yaml_loader_duplicate_key_raw_outcome() -> None:
    source_text = (
        "id: https://example.test/root\n"
        "name: first\n"
        "name: second\n"
        "classes: {}\n"
    )

    with pytest.raises(ValueError) as caught:
        YAMLLoader().loads(source_text, target_class=SchemaDefinition)

    assert type(caught.value) is ValueError
    assert caught.value.args == ('Duplicate key: "name"',)
    assert str(caught.value) == 'Duplicate key: "name"'


def test_schema_view_imports_closure_reaches_local_file_io(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root_path = tmp_path / "root.yaml"
    child_path = tmp_path / "child.yaml"
    root_path.write_text(
        "id: https://example.test/root\n"
        "name: root\n"
        "imports: [child]\n"
        "classes: {}\n",
        encoding="utf-8",
    )
    child_path.write_text(
        "id: https://example.test/child\n"
        "name: child\n"
        "classes: {}\n",
        encoding="utf-8",
    )
    real_open = builtins.open
    opened: list[str] = []

    def recording_open(file: Any, *args: Any, **kwargs: Any) -> Any:
        opened.append(str(file))
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", recording_open)

    closure = SchemaView(str(root_path)).imports_closure(inject_metadata=False)

    assert closure == ["child", "root"]
    assert len(opened) == 2
    assert opened[0] == str(root_path)
    assert opened[1] != str(root_path)


def test_schema_view_load_import_reaches_url_io(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[str] = []

    def intercept_urlopen(request: Any, **_kwargs: Any) -> None:
        requests.append(request.full_url)
        raise RuntimeError("intercepted URL read")

    monkeypatch.setattr(hbreader, "urlopen", intercept_urlopen)
    view = SchemaView(_schema("root", ("https://network.invalid/child",)))

    with pytest.raises(RuntimeError) as caught:
        view.imports_closure(inject_metadata=False)

    assert type(caught.value) is RuntimeError
    assert caught.value.args == ("intercepted URL read",)
    assert len(requests) == 1


def test_schema_view_nested_diamond_raw_closure() -> None:
    common = _schema("common")
    left = _schema("left", ("common",))
    right = _schema("right", ("common",))
    root = _schema("root", ("left", "right"))
    view = _MemorySchemaView(
        root,
        {"common": common, "left": left, "right": right},
    )

    closure = view.imports_closure(inject_metadata=False)

    assert closure == ["common", "left", "right", "root"]


def test_schema_view_missing_import_raw_exception(tmp_path: Path) -> None:
    root = _schema("root", ("missing",))
    root.source_file = str(tmp_path / "root.yaml")

    with pytest.raises(FileNotFoundError) as caught:
        SchemaView(root).imports_closure(inject_metadata=False)

    assert type(caught.value) is FileNotFoundError
    assert caught.value.errno == errno.ENOENT
    assert caught.value.args[:2] == (errno.ENOENT, "No such file or directory")


def test_schema_view_two_module_cycle_raw_closure() -> None:
    first = _schema("first", ("second",))
    second = _schema("second", ("first",))
    view = _MemorySchemaView(first, {"first": first, "second": second})

    closure = view.imports_closure(inject_metadata=False)

    assert closure == ["first", "second"]


def test_future_boundary_seam_is_not_implemented() -> None:
    import boundary

    assert boundary is not None
