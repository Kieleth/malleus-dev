"""Build an author-review TeX candidate from the unchanged working manuscript."""

import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CITATIONS = {
    "https://www.nature.com/articles/s41467-024-55792-9": "yu2025deep",
    "https://arxiv.org/abs/2304.02711": "caufield2024spires",
    "https://arxiv.org/abs/2510.01409": "cotti2026ontologx",
    "https://www.w3.org/TR/prov-o/": "lebo2013provo",
    "https://ottr.xyz/": "skjaeveland2024reasonable",
    "https://bluebrainnexus.io/products/nexus-delta/": "nexusdelta",
    "https://arxiv.org/abs/2602.23193": "santos2026esaa",
    "https://arxiv.org/abs/2005.11401": "lewis2020retrieval",
}


def escape(text):
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_\allowbreak{}",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def inline(text):
    text = " ".join(text.split())
    pattern = r"\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|\*([^*]+)\*|\b[0-9a-f]{64}\b"
    parts, end = [], 0
    for match in re.finditer(pattern, text):
        parts.append(escape(text[end : match.start()]))
        label, url, bold, italic = match.groups()
        if url:
            value = inline(label)
            if url in CITATIONS:
                value += r"~\cite{" + CITATIONS[url] + "}"
            elif url.startswith("https://"):
                value = r"\href{" + escape(url) + "}{" + value + "}"
            parts.append(value)
        elif bold:
            parts.append(r"\textbf{" + inline(bold) + "}")
        elif italic:
            parts.append(r"\emph{" + inline(italic) + "}")
        else:
            chunks = [match[0][i : i + 8] for i in range(0, 64, 8)]
            parts.append(r"{\small\ttfamily " + r"\allowbreak{}".join(chunks) + "}")
        end = match.end()
    return "".join(parts) + escape(text[end:])


def block_tex(block):
    if block.startswith("```"):
        match = re.fullmatch(r"```json\n(.*?)\n```", block, re.S)
        if not match:
            raise ValueError("Only complete JSON exhibits are supported")
        json.loads(match[1])
        return "\\begin{lstlisting}\n" + match[1] + "\n\\end{lstlisting}"
    if block.startswith("|"):
        rows = [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in block.splitlines()
        ]
        count = len(rows[0])
        if (
            count not in {4, 8}
            or len(rows) < 3
            or any(len(row) != count for row in rows)
            or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1])
        ):
            raise ValueError("Unsupported or malformed table")
        weights = (
            [0.30, 0.12, 0.12, 0.46]
            if count == 4
            else [0.14, 0.10, 0.08, 0.12, 0.14, 0.15, 0.14, 0.13]
        )
        columns = "".join(
            r">{\raggedright\arraybackslash}p{\dimexpr "
            + str(weight)
            + r"\linewidth-2\tabcolsep\relax}"
            for weight in weights
        )
        lines = [
            r"{\scriptsize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.3}",
            r"\begin{tabular}{" + columns + "}",
            r"\toprule",
            " & ".join(r"\textbf{" + inline(cell) + "}" for cell in rows[0]) + r" \\",
            r"\midrule",
        ]
        lines.extend(
            " & ".join(inline(cell) for cell in row) + r" \\" for row in rows[2:]
        )
        return "\n".join([*lines, r"\bottomrule", r"\end{tabular}}"])
    if block.startswith("#"):
        match = re.fullmatch(r"(#{2,3}) (.+)", block)
        if not match:
            raise ValueError("Unsupported heading")
        command = "section" if len(match[1]) == 2 else "subsection"
        prefix = r"\clearpage" + "\n" if match[2].startswith("Appendix ") else ""
        return prefix + "\\" + command + "*{" + inline(match[2]) + "}"
    if re.search(r"(?m)^(?:[-*] |\d+\. )", block):
        raise ValueError("Unsupported list, do not silently drop source content")
    return inline(block)


def convert(source):
    blocks = re.split(r"\n\s*\n", source.strip())
    if (
        not blocks[0].startswith("# ")
        or blocks[1] != "Luis Guzman Lorenzo. Author-review draft."
    ):
        raise ValueError("Unexpected title/author metadata")
    if blocks[2] != "## Abstract":
        raise ValueError("Missing abstract")
    main, appendix = [], []
    target = main
    main.extend(
        [r"\maketitle", r"\begin{abstract}", inline(blocks[3]), r"\end{abstract}"]
    )
    for index, block in enumerate(blocks[4:], 4):
        if block.startswith("## Appendix "):
            target = appendix
        value = block_tex(block)
        if block.startswith(("```", "|")):
            lead = (
                target.pop()
                if target and not blocks[index - 1].startswith(("#", "```", "|"))
                else ""
            )
            value = (
                "\\par\\medskip\n\\noindent\\begin{minipage}{\\linewidth}\n"
                + lead
                + "\n\n"
                + value
                + "\n\\end{minipage}\\par\\medskip"
            )
        target.append(value)
    template = (HERE / "template.tex").read_text()
    return {
        "main.tex": template.replace("TITLE_TEXT", inline(blocks[0][2:])),
        "body.tex": "\n\n".join(main) + "\n",
        "appendix.tex": "\n\n".join(appendix) + "\n",
    }


def archive_bytes(files):
    if set(files) != {
        "main.tex",
        "body.tex",
        "appendix.tex",
        "references.bib",
        "main.bbl",
    }:
        raise ValueError("Archive requires the exact five source files")
    result = io.BytesIO()
    with tarfile.open(fileobj=result, mode="w") as archive:
        for name, data in sorted(files.items()):
            item = tarfile.TarInfo(name)
            item.size, item.mode, item.mtime = len(data), 0o644, 0
            archive.addfile(item, io.BytesIO(data))
    return result.getvalue()


def build():
    config = json.loads((HERE / "build-config.json").read_text())
    source = (HERE.parent / "manuscript-v4-working.md").read_bytes()
    files = {name: value.encode() for name, value in convert(source.decode()).items()}
    files["references.bib"] = (HERE / "references.bib").read_bytes()
    executables = {}
    for name in config["executables"]:
        found = shutil.which(name) or next(
            (
                str(Path(directory) / name)
                for directory in config["tex_search_paths"]
                if (Path(directory) / name).is_file()
            ),
            None,
        )
        if found is None:
            raise RuntimeError(
                f"Missing {name}; use the declared TeX toolchain in build-config.json"
            )
        executables[name] = found
    scratch_root = ROOT / "tmp/pdfs"
    scratch_root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="submission-candidate-", dir=scratch_root))
    for name, value in files.items():
        (work / name).write_bytes(value)
    outputs = []
    for args in config["commands"]:
        result = subprocess.run(
            [executables[args[0]], *args[1:]], cwd=work, capture_output=True, text=True
        )
        outputs.append(result.stdout + result.stderr)
        if result.returncode:
            (work / "build-output.txt").write_text("\n".join(outputs))
            raise RuntimeError(
                f"TeX build refused; inspect {work / 'build-output.txt'}"
            )
    log = (work / "main.log").read_text()
    if re.search(
        r"undefined references|Citation .* undefined|Overfull \\[hv]box|Missing character:",
        log,
    ):
        raise RuntimeError(
            f"Unresolved reference or layout overflow; inspect {work / 'main.log'}"
        )
    files["main.bbl"] = (work / "main.bbl").read_bytes()
    archive = archive_bytes({name: files[name] for name in config["archive_files"]})
    output = ROOT / "output/pdf/malleus-paper-v4-submission-candidate.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes((work / "main.pdf").read_bytes())
    (HERE / "candidate-source.tar").write_bytes(archive)
    for name, value in files.items():
        (HERE / name).write_bytes(value)
    receipt = {
        "status": "BUILT_AWAITING_VISUAL_AND_AUTHOR_REVIEW",
        "manuscript_sha256": sha256(source).hexdigest(),
        "files": {name: sha256(value).hexdigest() for name, value in files.items()},
        "pdf_sha256": sha256(output.read_bytes()).hexdigest(),
        "archive_sha256": sha256(archive).hexdigest(),
        "archive_files": sorted(files),
        "build_directory": str(work),
        "tool_versions": {
            name: subprocess.run(
                [path, "--version"], capture_output=True, text=True, check=True
            ).stdout.splitlines()[0]
            for name, path in executables.items()
        },
        "arxiv_processing": "NOT_RUN",
        "human_ratification": "PENDING",
    }
    (HERE / "build-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(build(), indent=2))
