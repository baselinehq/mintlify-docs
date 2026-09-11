#!/usr/bin/env python3
"""Lint .mdx pages against the house style (CLAUDE.md, "Style guide").

Usage: scripts/style-lint.py [FILE ...]
With no files, lints the .mdx files changed relative to origin/main.
Errors fail the run; warnings are printed but do not.
"""
import re
import subprocess
import sys

MAX_WORDS = 26
NOTICE_TAGS = ("Note", "Warning", "Tip", "Info", "Check")

ERROR_PATTERNS = [
    (r"—", "em dash; rewrite with a comma, colon, or full stop"),
    (r"(?<=\S) - (?=\S)", "spaced hyphen used as a dash; rewrite the sentence"),
    (r"(?<![`>])->(?![`<])", "ascii arrow; write menu paths as **Menu > Item**"),
    (r"\bshould\b", "'should'; use 'must' for a requirement or 'we recommend' for advice"),
    (r"\bsimply\b", "'simply'; delete it"),
    (r"\bplease\b", "'please'; delete it"),
    (r"\be\.g\.", "'e.g.'; use 'for example' or 'such as'"),
    (r"\bi\.e\.", "'i.e.'; use 'that is'"),
    (r"\bin order to\b", "'in order to'; use 'to'"),
    (r"\bclick on\b", "'click on'; use 'click'"),
    (r"\bnote that\b", "'note that'; state the point directly"),
    (r"\butili[sz]e", "'utilize'; use 'use'"),
    (r"\bleverage\b", "'leverage'; use 'use'"),
    (r"\bdesired\b", "'desired'; use 'want' or 'need'"),
]

WARN_PATTERNS = [
    (r"\bjust\b", "'just' is usually filler"),
    (r"\bwill\b", "future tense; prefer present unless the action happens later"),
    (r"\b(above|below)\b", "directional language; use 'preceding', 'following', 'earlier', or 'later'"),
    (r"\bonce\b", "'once' meaning 'after'? use 'after'"),
    (r"\b(easy|easily|best|simplest|fastest|always|never|guarantee[sd]?|ensures?)\b", "excessive claim or absolute; state the behavior"),
    (r"\bvia\b", "'via'; prefer 'through' or 'by using'"),
]


def changed_files():
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AM", "origin/main...HEAD", "--", "*.mdx"],
        capture_output=True, text=True, check=False,
    ).stdout.split()
    return [f for f in out if f.endswith(".mdx")]


def blank(m):
    return "\n" * m.group(0).count("\n")


def strip_noise(body):
    body = re.sub(r"```.*?```", blank, body, flags=re.S)
    body = re.sub(r"`[^`\n]*`", "``", body)
    body = re.sub(r"^[ \t]*\|.*\|[ \t]*$", "", body, flags=re.M)
    body = re.sub(r"\]\([^)]*\)", "]()", body)
    body = re.sub(r"<[^>\n]+>", "", body)
    return body


def lint(path):
    errors, warns = [], []
    text = open(path, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        errors.append((1, "missing frontmatter"))
        body = text
    else:
        if "description:" not in fm.group(1):
            errors.append((1, "frontmatter has no description"))
        body = text[fm.end():]
    offset = text[: len(text) - len(body)].count("\n")

    for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", body, re.M):
        line = offset + body[: m.start()].count("\n") + 1
        words = m.group(2).split()
        if words and re.match(r"^[A-Z][a-z]+ing$", words[0]) and words[0] not in ("Billing", "Pricing"):
            warns.append((line, f"heading starts with -ing: {m.group(2)!r}; prefer a bare verb or noun phrase"))
        if re.search(r"[.:?!]$", m.group(2)):
            errors.append((line, f"heading ends with punctuation: {m.group(2)!r}"))

    notices = [(offset + body[: m.start()].count("\n") + 1, m.group(1))
               for m in re.finditer(r"^\s*<(%s)\b" % "|".join(NOTICE_TAGS), body, re.M)]
    if len(notices) > 2:
        warns.append((notices[2][0], f"{len(notices)} notices on one page; move core behavior into body text"))
    closes = [offset + body[: m.start()].count("\n") + 1
              for m in re.finditer(r"^\s*</(%s)>" % "|".join(NOTICE_TAGS), body, re.M)]
    for c in closes:
        nxt = [n for n in notices if n[0] > c]
        if nxt:
            between = body.split("\n")[c - offset: nxt[0][0] - offset - 1]
            if not any(l.strip() for l in between):
                errors.append((nxt[0][0], "two notices back to back; merge them or move one into body text"))

    prose = strip_noise(body)
    for pat, msg in ERROR_PATTERNS:
        for m in re.finditer(pat, prose, re.I):
            errors.append((offset + prose[: m.start()].count("\n") + 1, msg))
    for pat, msg in WARN_PATTERNS:
        for m in re.finditer(pat, prose, re.I):
            warns.append((offset + prose[: m.start()].count("\n") + 1, msg))

    paras = re.split(r"\n\s*\n", prose)
    pos = 0
    for para in paras:
        start = prose.find(para, pos)
        pos = start + len(para)
        if para.lstrip().startswith(("#", "-", "*", "1", "|", "import")):
            continue
        flat = re.sub(r"\s+", " ", para).strip()
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", flat):
            n = len(s.split())
            if n > MAX_WORDS:
                line = offset + prose[:start].count("\n") + 1
                warns.append((line, f"{n}-word sentence; aim for under {MAX_WORDS}: {s[:60]!r}"))
    return sorted(set(errors)), sorted(set(warns))


def main(argv):
    files = argv or changed_files()
    total_errors = 0
    for path in files:
        errors, warns = lint(path)
        total_errors += len(errors)
        for line, msg in errors:
            print(f"{path}:{line}: error: {msg}")
        for line, msg in warns:
            print(f"{path}:{line}: warning: {msg}")
    if not files:
        print("no .mdx files to lint")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
