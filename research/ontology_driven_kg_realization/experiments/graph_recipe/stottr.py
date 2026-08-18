"""Strict stOTTR slice used by GE-010 and GE-020.

This is deliberately not a general OTTR implementation. It parses the pinned
syntax needed by the first conformance slice and rejects later profile
features with a typed diagnostic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

from malleus.ledger import canonical_json, content_digest
from malleus.source import source_bytes_digest

from research.ontology_driven_kg_realization.experiments.graph_recipe.model import (
    GraphRecipeDiagnostic,
    GraphRecipeFailure,
)


MGRP = "https://malleus.dev/graph-recipe/base/"
OTTR = "http://ns.ottr.xyz/0.4/"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
XSD = "http://www.w3.org/2001/XMLSchema#"
TOP = OTTR + "Top"

TERMINAL_FIELDS = {
    MGRP + "Record": ("member", "operation_kind", "record_type", "record_id"),
    MGRP + "Property": ("member", "property", "value"),
    MGRP + "RelationSource": ("member", "record_id"),
    MGRP + "RelationTarget": ("member", "record_id"),
    MGRP + "DependsOn": ("member", "prerequisite_member"),
}
TERMINAL_SIGNATURES = {
    MGRP + "Record": (
        (OTTR + "IRI", True),
        (OTTR + "IRI", True),
        (OTTR + "IRI", True),
        (XSD + "string", True),
    ),
    MGRP + "Property": (
        (OTTR + "IRI", True),
        (OTTR + "IRI", True),
        (TOP, False),
    ),
    MGRP + "RelationSource": ((OTTR + "IRI", True), (XSD + "string", True)),
    MGRP + "RelationTarget": ((OTTR + "IRI", True), (XSD + "string", True)),
    MGRP + "DependsOn": ((OTTR + "IRI", True), (OTTR + "IRI", True)),
}
FACT_ORDER = {
    "Record": 0,
    "Property": 1,
    "RelationSource": 2,
    "RelationTarget": 3,
    "DependsOn": 4,
}


def _failure(
    code: str,
    phase: str,
    subject: str,
    message: str,
    evidence: Mapping[str, Any],
) -> GraphRecipeFailure:
    return GraphRecipeFailure(
        GraphRecipeDiagnostic(
            code,
            phase,
            subject,
            {"message": message},
            evidence,
        )
    )


def _require_iri(value: str, subject: str) -> str:
    if not isinstance(value, str):
        raise _failure(
            "STOTTR_SYNTAX_ERROR",
            "recipe-parsing",
            subject,
            "An IRI must be a string.",
            {"actual_type": type(value).__name__},
        )
    parsed = urlsplit(value)
    if not parsed.scheme or any(character.isspace() for character in value):
        raise _failure(
            "STOTTR_SYNTAX_ERROR",
            "recipe-parsing",
            subject,
            f"'{value}' is not an absolute IRI.",
            {"value": value},
        )
    return value


@dataclass(frozen=True)
class Token:
    kind: str
    value: Any
    offset: int


def _tokens(source: str, source_id: str) -> tuple[Token, ...]:
    values: list[Token] = []
    index = 0
    length = len(source)
    punctuation = "[]{}(),!?=|"

    while index < length:
        character = source[index]
        if character.isspace():
            index += 1
            continue
        if source.startswith("/***", index):
            end = source.find("***/", index + 4)
            if end < 0:
                raise _failure(
                    "STOTTR_SYNTAX_ERROR",
                    "recipe-parsing",
                    source_id,
                    "Unterminated stOTTR block comment.",
                    {"offset": index},
                )
            index = end + 4
            continue
        if character == "#":
            end = source.find("\n", index + 1)
            index = length if end < 0 else end + 1
            continue
        if source.startswith("@prefix", index):
            end = index + len("@prefix")
            if end == length or source[end].isspace():
                values.append(Token("PREFIX", "@prefix", index))
                index = end
                continue
        if source.startswith("::", index):
            values.append(Token("DEFINE", "::", index))
            index += 2
            continue
        if source.startswith("^^", index):
            values.append(Token("DATATYPE", "^^", index))
            index += 2
            continue
        if character == "<":
            end = source.find(">", index + 1)
            if end < 0:
                raise _failure(
                    "STOTTR_SYNTAX_ERROR",
                    "recipe-parsing",
                    source_id,
                    "Unterminated IRI reference.",
                    {"offset": index},
                )
            value = source[index + 1 : end]
            values.append(Token("IRI", _require_iri(value, source_id), index))
            index = end + 1
            continue
        if character == '"':
            end = index + 1
            escaped = False
            while end < length:
                current = source[end]
                if current == '"' and not escaped:
                    break
                if current == "\\" and not escaped:
                    escaped = True
                else:
                    escaped = False
                end += 1
            if end >= length:
                raise _failure(
                    "STOTTR_SYNTAX_ERROR",
                    "recipe-parsing",
                    source_id,
                    "Unterminated string literal.",
                    {"offset": index},
                )
            raw = source[index : end + 1]
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as error:
                raise _failure(
                    "STOTTR_SYNTAX_ERROR",
                    "recipe-parsing",
                    source_id,
                    f"Invalid string literal: {error.msg}.",
                    {"offset": index},
                ) from error
            values.append(Token("STRING", value, index))
            index = end + 1
            continue
        if character == "?" and index + 1 < length and (
            source[index + 1].isalpha() or source[index + 1] == "_"
        ):
            end = index + 2
            while end < length and (source[end].isalnum() or source[end] in "_.-"):
                end += 1
            values.append(Token("VARIABLE", source[index + 1 : end], index))
            index = end
            continue
        if source.startswith("_:", index):
            end = index + 2
            while end < length and not source[end].isspace() and source[end] not in punctuation + ".":
                end += 1
            values.append(Token("BLANK", source[index:end], index))
            index = end
            continue
        if character == ".":
            values.append(Token("DOT", character, index))
            index += 1
            continue
        if character in punctuation:
            values.append(Token(character, character, index))
            index += 1
            continue
        if character.isdigit() or (
            character in "+-" and index + 1 < length and source[index + 1].isdigit()
        ):
            end = index + 1
            while end < length and source[end].isdigit():
                end += 1
            values.append(Token("INTEGER", int(source[index:end]), index))
            index = end
            continue

        end = index + 1
        stop = punctuation + '<>"#'
        while end < length and not source[end].isspace() and source[end] not in stop:
            end += 1
        raw = source[index:end]
        trailing_dot = raw.endswith(".")
        if trailing_dot:
            raw = raw[:-1]
        if not raw:
            raise _failure(
                "STOTTR_SYNTAX_ERROR",
                "recipe-parsing",
                source_id,
                f"Unexpected character '{character}'.",
                {"offset": index},
            )
        kind = "PNAME" if ":" in raw else "WORD"
        values.append(Token(kind, raw, index))
        if trailing_dot:
            values.append(Token("DOT", ".", end - 1))
        index = end

    values.append(Token("EOF", None, length))
    return tuple(values)


@dataclass(frozen=True)
class RecipeTerm:
    kind: str
    value: Any = None
    datatype: str | None = None

    @classmethod
    def iri(cls, value: str) -> "RecipeTerm":
        return cls("iri", _require_iri(value, "RDF term"))

    @classmethod
    def literal(cls, lexical_form: str, datatype: str = XSD + "string") -> "RecipeTerm":
        return cls("literal", lexical_form, _require_iri(datatype, "literal datatype"))

    @classmethod
    def integer(cls, value: int) -> "RecipeTerm":
        return cls("literal", str(value), XSD + "integer")

    @classmethod
    def from_artifact(cls, value: Mapping[str, Any], subject: str) -> "RecipeTerm":
        if not isinstance(value, Mapping):
            raise _failure(
                "RECIPE_ARGUMENT_TYPE_MISMATCH",
                "invocation-binding",
                subject,
                "Invocation term must be an object.",
                {"actual_type": type(value).__name__},
            )
        if "kind" not in value:
            raise _failure(
                "RECIPE_ARGUMENT_TYPE_MISMATCH",
                "invocation-binding",
                subject,
                "Invocation term requires kind.",
                {"actual_fields": sorted(value)},
            )
        kind = value["kind"]
        if kind == "iri" and set(value) == {"kind", "value"}:
            return cls.iri(value["value"])
        if kind == "literal" and set(value) == {"kind", "datatype", "lexical_form"}:
            return cls.literal(value["lexical_form"], value["datatype"])
        if kind == "none" and set(value) == {"kind"}:
            return cls("none")
        if kind == "blank_node" and set(value) == {"kind", "value"}:
            return cls("blank", value["value"])
        raise _failure(
            "RECIPE_ARGUMENT_TYPE_MISMATCH",
            "invocation-binding",
            subject,
            "Invocation term has an unsupported shape.",
            {"term": dict(value)},
        )

    def as_dict(self) -> dict[str, Any]:
        if self.kind == "iri":
            return {"kind": "iri", "value": self.value}
        if self.kind == "literal":
            return {
                "kind": "literal",
                "datatype": self.datatype,
                "lexical_form": self.value,
            }
        if self.kind == "none":
            return {"kind": "none"}
        if self.kind == "blank":
            return {"kind": "blank_node", "value": self.value}
        raise ValueError(f"Term kind '{self.kind}' is not serializable")

    def python_value(self) -> Any:
        if self.kind != "literal":
            return self.value
        if self.datatype == XSD + "integer":
            return int(self.value)
        return self.value


@dataclass(frozen=True)
class AstTerm:
    kind: str
    value: Any = None
    datatype: str | None = None

    def canonical(self, variables: Mapping[str, int]) -> dict[str, Any]:
        if self.kind == "variable":
            return {"kind": "variable", "position": variables[self.value]}
        return RecipeTerm(self.kind, self.value, self.datatype).as_dict()


@dataclass(frozen=True)
class RecipeParameter:
    name: str
    rdf_type: str
    mandatory: bool

    def canonical(self) -> dict[str, Any]:
        return {"rdf_type": self.rdf_type, "mandatory": self.mandatory}


@dataclass(frozen=True)
class RecipeCall:
    template_iri: str
    arguments: tuple[AstTerm, ...]
    source_pattern_index: int

    def canonical(self, variables: Mapping[str, int]) -> dict[str, Any]:
        return {
            "template": self.template_iri,
            "arguments": [argument.canonical(variables) for argument in self.arguments],
        }


@dataclass(frozen=True)
class RecipeTemplate:
    template_iri: str
    parameters: tuple[RecipeParameter, ...]
    patterns: tuple[RecipeCall, ...]
    base: bool

    def canonical(self) -> dict[str, Any]:
        variables = {parameter.name: index for index, parameter in enumerate(self.parameters)}
        patterns = [pattern.canonical(variables) for pattern in self.patterns]
        patterns.sort(key=canonical_json)
        return {
            "template": self.template_iri,
            "parameters": [parameter.canonical() for parameter in self.parameters],
            "base": self.base,
            "patterns": patterns,
        }


@dataclass(frozen=True)
class ParsedDocument:
    source_id: str
    source_digest: str
    templates: tuple[RecipeTemplate, ...]


class _Parser:
    def __init__(self, source: str, source_id: str):
        self.source_id = source_id
        self.tokens = _tokens(source, source_id)
        self.index = 0
        self.prefixes: dict[str, str] = {}

    @property
    def token(self) -> Token:
        return self.tokens[self.index]

    def take(self, kind: str) -> Token:
        if self.token.kind != kind:
            raise _failure(
                "STOTTR_SYNTAX_ERROR",
                "recipe-parsing",
                self.source_id,
                f"Expected {kind}, found {self.token.kind}.",
                {"offset": self.token.offset, "token": self.token.value},
            )
        token = self.token
        self.index += 1
        return token

    def accept(self, kind: str) -> Token | None:
        if self.token.kind != kind:
            return None
        return self.take(kind)

    def iri(self) -> str:
        if self.token.kind == "IRI":
            return self.take("IRI").value
        if self.token.kind != "PNAME":
            if self.token.kind == "BLANK":
                blank = self.take("BLANK").value
                raise _failure(
                    "FORBIDDEN_BLANK_NODE",
                    "profile-validation",
                    self.source_id,
                    f"Blank-node identity '{blank}' is forbidden in effective topology.",
                    {"value": blank},
                )
            return self.take("PNAME").value
        value = self.take("PNAME").value
        prefix, local = value.split(":", 1)
        if prefix not in self.prefixes:
            raise _failure(
                "STOTTR_SYNTAX_ERROR",
                "recipe-parsing",
                self.source_id,
                f"Prefix '{prefix}' is not declared.",
                {"prefix": prefix},
            )
        return _require_iri(self.prefixes[prefix] + local, self.source_id)

    def term(self) -> AstTerm:
        if self.token.kind == "VARIABLE":
            return AstTerm("variable", self.take("VARIABLE").value)
        if self.token.kind in {"IRI", "PNAME"}:
            return AstTerm("iri", self.iri())
        if self.token.kind == "BLANK" or self.token.kind == "[":
            if self.token.kind == "BLANK":
                value = self.take("BLANK").value
            else:
                self.take("[")
                self.take("]")
                value = "[]"
            return AstTerm("blank", value)
        if self.token.kind == "STRING":
            value = self.take("STRING").value
            datatype = XSD + "string"
            if self.accept("DATATYPE") is not None:
                datatype = self.iri()
            return AstTerm("literal", value, datatype)
        if self.token.kind == "INTEGER":
            return AstTerm("literal", str(self.take("INTEGER").value), XSD + "integer")
        if self.token.kind == "WORD" and self.token.value == "none":
            self.take("WORD")
            return AstTerm("none")
        if self.token.kind == "(":
            raise _failure(
                "UNIMPLEMENTED_PROFILE_FEATURE",
                "profile-validation",
                self.source_id,
                "List terms enter the profile at GE-040, not this slice.",
                {"feature": "list"},
            )
        raise _failure(
            "STOTTR_SYNTAX_ERROR",
            "recipe-parsing",
            self.source_id,
            f"Expected a term, found {self.token.kind}.",
            {"offset": self.token.offset, "token": self.token.value},
        )

    def parameter(self) -> RecipeParameter:
        mandatory = self.accept("!") is not None
        if self.accept("?") is not None:
            raise _failure(
                "UNIMPLEMENTED_PROFILE_FEATURE",
                "profile-validation",
                self.source_id,
                "Optional parameters enter the profile at GE-030, not this slice.",
                {"feature": "optional-parameter"},
            )
        rdf_type = TOP if self.token.kind == "VARIABLE" else self.iri()
        name = self.take("VARIABLE").value
        if self.accept("=") is not None:
            self.term()
            raise _failure(
                "UNIMPLEMENTED_PROFILE_FEATURE",
                "profile-validation",
                self.source_id,
                "Default parameters enter the profile after the first slice.",
                {"feature": "default-parameter", "parameter": name},
            )
        return RecipeParameter(name, rdf_type, mandatory)

    def template(self) -> RecipeTemplate:
        template_iri = self.iri()
        self.take("[")
        parameters: list[RecipeParameter] = []
        if self.token.kind != "]":
            while True:
                parameters.append(self.parameter())
                if self.accept(",") is None:
                    break
        self.take("]")
        self.take("DEFINE")
        if self.token.kind == "WORD" and self.token.value == "BASE":
            self.take("WORD")
            self.take("DOT")
            return RecipeTemplate(template_iri, tuple(parameters), (), True)
        self.take("{")
        patterns: list[RecipeCall] = []
        while self.token.kind != "}":
            if self.token.kind == "WORD" and self.token.value in {"cross", "zipMin", "zipMax"}:
                feature = self.take("WORD").value
                raise _failure(
                    "UNIMPLEMENTED_PROFILE_FEATURE",
                    "profile-validation",
                    self.source_id,
                    f"List expander '{feature}' is outside GE-000 through GE-020.",
                    {"feature": feature},
                )
            target = self.iri()
            self.take("(")
            arguments: list[AstTerm] = []
            if self.token.kind != ")":
                while True:
                    arguments.append(self.term())
                    if self.accept(",") is None:
                        break
            self.take(")")
            patterns.append(RecipeCall(target, tuple(arguments), len(patterns)))
            self.accept(",")
        self.take("}")
        self.take("DOT")
        return RecipeTemplate(template_iri, tuple(parameters), tuple(patterns), False)

    def document(self) -> tuple[RecipeTemplate, ...]:
        templates: list[RecipeTemplate] = []
        while self.token.kind != "EOF":
            if self.accept("PREFIX") is not None:
                prefix = self.take("PNAME").value
                if not prefix.endswith(":"):
                    raise _failure(
                        "STOTTR_SYNTAX_ERROR",
                        "recipe-parsing",
                        self.source_id,
                        "Prefix declaration requires a namespace name ending in ':'.",
                        {"prefix": prefix},
                    )
                namespace = self.take("IRI").value
                self.take("DOT")
                name = prefix[:-1]
                if name in self.prefixes:
                    raise _failure(
                        "STOTTR_SYNTAX_ERROR",
                        "recipe-parsing",
                        self.source_id,
                        f"Prefix '{name}' is declared more than once.",
                        {"prefix": name},
                    )
                self.prefixes[name] = namespace
                continue
            templates.append(self.template())
        return tuple(templates)


def parse_stottr(source_bytes: bytes, source_id: str) -> ParsedDocument:
    if not isinstance(source_bytes, bytes):
        raise TypeError("source_bytes must be bytes")
    try:
        source = source_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise _failure(
            "STOTTR_SYNTAX_ERROR",
            "recipe-parsing",
            source_id,
            "stOTTR source must be UTF-8.",
            {"start": error.start},
        ) from error
    templates = _Parser(source, source_id).document()
    return ParsedDocument(source_id, source_bytes_digest(source_bytes), templates)


@dataclass(frozen=True)
class CompiledGraphRecipe:
    root_template: str
    templates: tuple[RecipeTemplate, ...]
    source_digests: tuple[tuple[str, str], ...]
    effective_recipe_digest: str
    contract_digest: str
    profile_id: str
    expansion_profile_id: str

    def template(self, template_iri: str) -> RecipeTemplate:
        for template in self.templates:
            if template.template_iri == template_iri:
                return template
        raise _failure(
            "UNDECLARED_TEMPLATE",
            "recipe-compilation",
            template_iri,
            f"Template '{template_iri}' is not in the locked recipe closure.",
            {"template": template_iri},
        )


def compile_graph_recipe(
    documents: Sequence[ParsedDocument],
    *,
    root_template: str,
    contract_digest: str,
    profile_id: str,
    expansion_profile_id: str,
) -> CompiledGraphRecipe:
    if not documents:
        raise ValueError("documents cannot be empty")
    declarations: dict[str, RecipeTemplate] = {}
    sources: list[tuple[str, str]] = []
    for document in documents:
        sources.append((document.source_id, document.source_digest))
        for template in document.templates:
            if template.template_iri in declarations:
                raise _failure(
                    "DUPLICATE_TEMPLATE_DECLARATION",
                    "recipe-compilation",
                    template.template_iri,
                    f"Template '{template.template_iri}' is declared more than once.",
                    {"template": template.template_iri},
                )
            declarations[template.template_iri] = template

    expected_arity = {iri: len(fields) for iri, fields in TERMINAL_FIELDS.items()}
    for terminal, arity in expected_arity.items():
        declaration = declarations.get(terminal)
        actual_signature = (
            tuple((parameter.rdf_type, parameter.mandatory) for parameter in declaration.parameters)
            if declaration is not None
            else None
        )
        if (
            declaration is None
            or not declaration.base
            or len(declaration.parameters) != arity
            or actual_signature != TERMINAL_SIGNATURES[terminal]
        ):
            raise _failure(
                "TERMINAL_ABI_MISMATCH",
                "recipe-compilation",
                terminal,
                f"Terminal '{terminal}' does not match the frozen signature.",
                {
                    "terminal": terminal,
                    "expected_signature": [list(item) for item in TERMINAL_SIGNATURES[terminal]],
                    "actual_signature": (
                        [list(item) for item in actual_signature]
                        if actual_signature is not None
                        else None
                    ),
                },
            )

    root = declarations.get(root_template)
    if root is None or root.base:
        raise _failure(
            "UNDECLARED_TEMPLATE",
            "recipe-compilation",
            root_template,
            f"Root template '{root_template}' is not a concrete locked template.",
            {"root_template": root_template},
        )
    variables = {parameter.name for parameter in root.parameters}
    for call in root.patterns:
        if call.template_iri not in TERMINAL_FIELDS:
            raise _failure(
                "UNIMPLEMENTED_PROFILE_FEATURE",
                "profile-validation",
                call.template_iri,
                "Nested composite templates enter after the first implementation slice.",
                {"feature": "nested-template", "template": call.template_iri},
            )
        if len(call.arguments) != expected_arity[call.template_iri]:
            raise _failure(
                "TERMINAL_ABI_MISMATCH",
                "recipe-compilation",
                call.template_iri,
                "Terminal call arity does not match the frozen ABI.",
                {
                    "template": call.template_iri,
                    "expected_arity": expected_arity[call.template_iri],
                    "actual_arity": len(call.arguments),
                },
            )
        unsafe = sorted(
            argument.value
            for argument in call.arguments
            if argument.kind == "variable" and argument.value not in variables
        )
        if unsafe:
            raise _failure(
                "UNSAFE_RECIPE_VARIABLE",
                "recipe-compilation",
                root_template,
                "Recipe pattern references undeclared variables.",
                {"variables": unsafe},
            )
        blanks = [argument.value for argument in call.arguments if argument.kind == "blank"]
        if blanks:
            raise _failure(
                "FORBIDDEN_BLANK_NODE",
                "profile-validation",
                root_template,
                f"Blank-node identity '{blanks[0]}' is forbidden in effective topology.",
                {"value": blanks[0]},
            )

    canonical_templates = [template.canonical() for template in declarations.values()]
    canonical_templates.sort(key=lambda value: value["template"])
    effective_digest = content_digest(
        {
            "profile_id": profile_id,
            "root_template": root_template,
            "terminal_abi": {
                key: {
                    "fields": list(TERMINAL_FIELDS[key]),
                    "signature": [list(item) for item in TERMINAL_SIGNATURES[key]],
                }
                for key in sorted(TERMINAL_FIELDS)
            },
            "templates": canonical_templates,
        }
    )
    return CompiledGraphRecipe(
        root_template,
        tuple(sorted(declarations.values(), key=lambda item: item.template_iri)),
        tuple(sorted(sources)),
        effective_digest,
        contract_digest,
        profile_id,
        expansion_profile_id,
    )


def _actual_type(term: RecipeTerm) -> str:
    if term.kind == "iri":
        return OTTR + "IRI"
    if term.kind == "literal":
        return term.datatype or TOP
    return term.kind


def _validate_binding(
    parameter: RecipeParameter,
    term: RecipeTerm,
    invocation_id: str,
) -> None:
    if term.kind == "blank":
        raise _failure(
            "FORBIDDEN_BLANK_NODE",
            "profile-validation",
            invocation_id,
            f"Blank-node identity '{term.value}' is forbidden in effective topology.",
            {"invocation_id": invocation_id, "parameter": parameter.name, "value": term.value},
        )
    if term.kind == "none" and parameter.mandatory:
        raise _failure(
            "MANDATORY_RECIPE_VALUE_MISSING",
            "invocation-binding",
            invocation_id,
            f"Mandatory recipe parameter '{parameter.name}' cannot bind none.",
            {"invocation_id": invocation_id, "parameter": parameter.name},
        )
    if term.kind == "none":
        return
    accepted = (
        parameter.rdf_type == TOP
        or parameter.rdf_type in {OTTR + "IRI", RDFS + "Resource"} and term.kind == "iri"
        or parameter.rdf_type == XSD + "string"
        and term.kind == "literal"
        and term.datatype == XSD + "string"
        or parameter.rdf_type == XSD + "integer"
        and term.kind == "literal"
        and term.datatype == XSD + "integer"
    )
    if not accepted:
        raise _failure(
            "RECIPE_ARGUMENT_TYPE_MISMATCH",
            "invocation-binding",
            invocation_id,
            (
                f"Recipe parameter '{parameter.name}' requires '{parameter.rdf_type}', "
                f"received '{_actual_type(term)}'."
            ),
            {
                "invocation_id": invocation_id,
                "parameter": parameter.name,
                "expected_type": parameter.rdf_type,
                "actual_type": _actual_type(term),
            },
        )


def _evaluate(term: AstTerm, bindings: Mapping[str, RecipeTerm]) -> RecipeTerm:
    if term.kind == "variable":
        return bindings[term.value]
    return RecipeTerm(term.kind, term.value, term.datatype)


def _require_term_kind(
    term: RecipeTerm,
    kind: str,
    terminal: str,
    field: str,
) -> Any:
    if term.kind != kind:
        raise _failure(
            "TERMINAL_ABI_MISMATCH",
            "recipe-expansion",
            terminal,
            f"Terminal field '{field}' requires {kind}, received {term.kind}.",
            {"terminal": terminal, "field": field, "term": term.as_dict()},
        )
    return term.value


def _require_string_literal(
    term: RecipeTerm,
    terminal: str,
    field: str,
) -> str:
    value = _require_term_kind(term, "literal", terminal, field)
    if term.datatype != XSD + "string":
        raise _failure(
            "TERMINAL_ABI_MISMATCH",
            "recipe-expansion",
            terminal,
            f"Terminal field '{field}' requires xsd:string, received '{term.datatype}'.",
            {"terminal": terminal, "field": field, "term": term.as_dict()},
        )
    return value


def _fact(call: RecipeCall, arguments: tuple[RecipeTerm, ...]) -> dict[str, Any]:
    terminal = call.template_iri
    kind = terminal.removeprefix(MGRP)
    if kind == "Record":
        return {
            "kind": kind,
            "member": _require_term_kind(arguments[0], "iri", terminal, "member"),
            "operation_kind": _require_term_kind(arguments[1], "iri", terminal, "operation_kind"),
            "record_type": _require_term_kind(arguments[2], "iri", terminal, "record_type"),
            "record_id": _require_string_literal(arguments[3], terminal, "record_id"),
        }
    if kind == "Property":
        if arguments[2].kind in {"none", "blank", "variable"}:
            raise _failure(
                "TERMINAL_ABI_MISMATCH",
                "recipe-expansion",
                terminal,
                "Property value must be a concrete RDF term.",
                {"term": arguments[2].as_dict()},
            )
        return {
            "kind": kind,
            "member": _require_term_kind(arguments[0], "iri", terminal, "member"),
            "property": _require_term_kind(arguments[1], "iri", terminal, "property"),
            "value": arguments[2].as_dict(),
        }
    if kind in {"RelationSource", "RelationTarget"}:
        return {
            "kind": kind,
            "member": _require_term_kind(arguments[0], "iri", terminal, "member"),
            "record_id": _require_string_literal(arguments[1], terminal, "record_id"),
        }
    if kind == "DependsOn":
        return {
            "kind": kind,
            "member": _require_term_kind(arguments[0], "iri", terminal, "member"),
            "prerequisite_member": _require_term_kind(
                arguments[1], "iri", terminal, "prerequisite_member"
            ),
        }
    raise ValueError(f"Unknown terminal: {terminal}")


@dataclass(frozen=True)
class ExpansionResult:
    invocation_id: str
    invocation_digest: str
    emissions: tuple[dict[str, Any], ...]
    expansion_paths: tuple[dict[str, Any], ...]

    def terminal_artifact(self) -> dict[str, Any]:
        return {
            "schema_version": "1",
            "status": "complete",
            "invocation_digest": {
                "status": "complete",
                "algorithm": "canonical-json-sha256-v1",
                "value": self.invocation_digest,
            },
            "emissions": [dict(value) for value in self.emissions],
        }


def expand_invocation(
    compiled: CompiledGraphRecipe,
    *,
    invocation_id: str,
    arguments: Mapping[str, RecipeTerm],
) -> ExpansionResult:
    root = compiled.template(compiled.root_template)
    expected = [parameter.name for parameter in root.parameters]
    if list(arguments) != expected:
        raise _failure(
            "RECIPE_ARGUMENT_BINDING_MISMATCH",
            "invocation-binding",
            invocation_id,
            "Invocation arguments must match recipe parameters exactly and in order.",
            {"expected": expected, "actual": list(arguments)},
        )
    for parameter in root.parameters:
        _validate_binding(parameter, arguments[parameter.name], invocation_id)

    invocation_digest = content_digest(
        {
            "effective_recipe_digest": compiled.effective_recipe_digest,
            "contract_digest": compiled.contract_digest,
            "arguments": [arguments[name].as_dict() for name in expected],
            "expansion_profile_id": compiled.expansion_profile_id,
        }
    )
    expanded = []
    for call in root.patterns:
        terms = tuple(_evaluate(argument, arguments) for argument in call.arguments)
        fact = _fact(call, terms)
        expanded.append((fact, call))
    expanded.sort(
        key=lambda item: (
            item[0]["member"],
            FACT_ORDER[item[0]["kind"]],
            canonical_json(item[0]),
            canonical_json(item[1].canonical({p.name: i for i, p in enumerate(root.parameters)})),
        )
    )

    slug = invocation_id.rstrip("/").rsplit("/", 1)[-1]
    emissions = []
    paths = []
    for index, (fact, call) in enumerate(expanded):
        emission_id = f"{slug}:e{index:03d}"
        path_id = f"{slug}:p{index:03d}"
        emissions.append(
            {
                "emission_id": emission_id,
                "fact": fact,
                "expansion_path_id": path_id,
            }
        )
        paths.append(
            {
                "expansion_path_id": path_id,
                "invocation_id": invocation_id,
                "template_stack": [compiled.root_template, call.template_iri],
                "source_pattern_index": call.source_pattern_index,
                "emission_ids": [emission_id],
            }
        )
    return ExpansionResult(invocation_id, invocation_digest, tuple(emissions), tuple(paths))


def parse_file(path: str | Path, *, source_id: str | None = None) -> ParsedDocument:
    artifact = Path(path)
    return parse_stottr(
        artifact.read_bytes(),
        source_id if source_id is not None else artifact.as_posix(),
    )
