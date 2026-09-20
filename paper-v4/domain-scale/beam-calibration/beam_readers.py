"""Paper-local question projection and citation checks, never answer scoring."""

from beam_prepare import canonical, decode, digest


def question_view(raw):
    try:
        questions = []
        for group in decode(raw).values():
            for item in group:
                text = item["question"]
                if not isinstance(text, str) or not text.strip():
                    raise ValueError("question text required")
                questions.append({"id": f"q{len(questions) + 1:02}", "question": text})
        if not questions:
            raise ValueError("questions required")
        return {"questions": questions}
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError(f"malformed question input: {error}") from error


def validate_answers(raw, questions_raw, evidence_raw, condition):
    """Check closure and exact excerpt location, not entailment or completeness."""
    try:
        answer, questions, evidence = map(decode, (raw, questions_raw, evidence_raw))
        if condition not in {"source", "graph"} or answer["condition"] != condition:
            raise ValueError("reader condition mismatch")
        if answer["questions_sha256"] != digest(questions_raw) or answer[
            "evidence_sha256"
        ] != digest(evidence_raw):
            raise ValueError("answer input identity mismatch")
        if condition == "source":
            records = [b for p in evidence["pages"] for b in p["blocks"]]
        else:
            records = [
                r
                for family in (
                    "entities",
                    "relations",
                    "events",
                    "signals",
                    "event_participations",
                )
                for r in evidence[family]
            ]
        index = {r["id"]: r for r in records}
        if len(index) != len(records):
            raise ValueError("duplicate evidence locator")
        wanted = [q["id"] for q in questions["questions"]]
        rows = answer["answers"]
        if [r["question_id"] for r in rows] != wanted or len(set(wanted)) != len(
            wanted
        ):
            raise ValueError("answer closure/order mismatch")
        count = 0
        for row in rows:
            if row["status"] not in {"ANSWERED", "PARTIAL", "UNDETERMINED"}:
                raise ValueError("unknown answer status")
            for field in ("answer", "limitations"):
                if not isinstance(row[field], str) or not row[field].strip():
                    raise ValueError(f"nonempty {field} required")
            if not isinstance(row["evidence"], list) or (
                row["status"] != "UNDETERMINED" and not row["evidence"]
            ):
                raise ValueError("positive answer needs evidence")
            for citation in row["evidence"]:
                value = index[citation["locator"]]
                path = citation["path"]
                if not isinstance(path, list) or not path:
                    raise ValueError("citation field path required")
                for part in path:
                    value = value[part]
                text = value if isinstance(value, str) else canonical(value).decode()
                excerpt = citation["excerpt"]
                if (
                    not isinstance(excerpt, str)
                    or not excerpt.strip()
                    or excerpt not in text
                ):
                    raise ValueError("citation excerpt not in declared field")
                if (
                    not isinstance(citation["supports"], str)
                    or not citation["supports"].strip()
                ):
                    raise ValueError("citation explanation required")
                count += 1
        return {
            "answers": len(rows),
            "citations": count,
            "semantic_support": "NOT_CHECKED",
        }
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError(f"malformed or unresolved answer: {error}") from error
