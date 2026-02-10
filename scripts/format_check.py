#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Any

EXT_DEFAULT = [".h", ".hpp", ".c", ".cc", ".cpp"]

OPERATOR_RE = re.compile(r"[^ \t](==|!=|<=|>=|\+|-|\*|/|%|=|<|>|\|\||&&)[^ \t]")

# Space AFTER keywords: `if (` not `if(`
KW_AFTER_RE = re.compile(r"\b(if|switch|for|while)\(")
ELSEIF_AFTER_RE = re.compile(r"\belse\s+if\(")

# Space BEFORE keywords: `} else`, `; if`, etc.
KW_BEFORE_RE = re.compile(r"([;}\)\]])(if|for|while|switch|return|break|continue|case|else)\b")

CLASS_RE = re.compile(r"\bclass\s+([a-z_][a-zA-Z0-9_]*)")
STRUCT_RE = re.compile(r"\bstruct\s+([a-z_][a-zA-Z0-9_]*)")
TYPEDEF_STRUCT_RE = re.compile(r"typedef\s+struct\s+([a-zA-Z0-9_]*)")

# Pointer/ref style: allowed `int *var`, `int &var`
BAD_PTR_REF_RE = re.compile(r"\b\w+[\*&]\s+\w+")      # int* var
NO_SPACE_PTR_REF_RE = re.compile(r"\b\w+[\*&]\w+\b")  # int*var
SPACE_BETWEEN_PTR_REF_RE = re.compile(r"\b\w+\s+[\*&]\s+\w+\b")  # int * var
GOOD_PTR_REF_RE = re.compile(r"\b\w+\s+[\*&]\w+\b")

# Heuristics for definitions
FUNC_LINE_HAS_PAREN = re.compile(r"\)\s*(const)?\s*(noexcept)?\s*$")
FUNC_LINE_HAS_OPEN_BRACE = re.compile(r"\)\s*(const)?\s*(noexcept)?\s*\{")
CLASS_STRUCT_LINE = re.compile(r"^\s*(class|struct)\b")

<<<<<<< HEAD
# Preprocessor directives should be treated as code (i.e. not ignored like comments).
COMMENT_OR_PREPROC = re.compile(r"^\s*(#)")

LICENSE = "GNU General Public License"
=======
COMMENT_OR_PREPROC = re.compile(r"^\s*(//|/\*|\*|\*/|#)")

LICENSE = """
/* 
 * -*- coding: utf-8 -*- 
 * Copyright 2026 physim devlopers
 *
 * This file is part of physim.
 *
 * physim is free software: you can redistribute it and/or modify
 * it under the term of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the license, or
 * (at your option) any later version.
 *
 * physim is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with physim. If not, see <https:://www.gnu.org/license/#GPL>
*/
"""
>>>>>>> tests

def load_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    rules: dict[str, Any] = {}
    cur_list: list[str] | None = None
    in_rules = False

    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue

        if raw.startswith("rules:"):
            in_rules = True
            cur_list = None
            continue

        if in_rules and raw and not raw.startswith(" "):
            in_rules = False

        target = rules if in_rules else data
        line = raw.strip()

        if line.endswith(":") and not line.startswith("-"):
            key = line[:-1].strip()
            target[key] = []
            cur_list = target[key]
            continue

        if line.startswith("-"):
            if cur_list is None:
                raise ValueError(f"YAML parse error near: {raw}")
            cur_list.append(line[1:].strip().strip('"').strip("'"))
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            cur_list = None
            if val.lower() in ("true", "false"):
                target[key] = (val.lower() == "true")
            else:
                try:
                    target[key] = int(val)
                except ValueError:
                    target[key] = val
            continue

        raise ValueError(f"YAML parse error near: {raw}")

    data["rules"] = rules
    return data

@dataclass(frozen=True)
class Rules:
    max_line_length: int = 88
    forbid_trailing_whitespace: bool = True
    require_newline_at_eof: bool = True

    indentation_tabs_only: bool = True
    tab_width: int = 2
    indent_multiple_of: int = 2

    require_space_after_keywords: bool = True
    require_space_before_keywords: bool = True
    require_space_around_operators: bool = True
    require_space_around_braces: bool = True

    require_blank_line_before_includes: bool = True
    require_blank_line_after_includes: bool = True

    require_blank_lines_around_definitions: bool = True  # NEW

    pointer_reference_style: str = "type_space_starvar"

    typedef_struct_suffix: str = "_t"
    class_name_capitalized: bool = True

    license_required_substring: str = LICENSE
<<<<<<< HEAD
    license_scan_lines: int = 20 
=======
    license_scan_lines: int = 19
>>>>>>> tests

def err(rel: Path, line: int, msg: str) -> str:
    return f"{rel}:{line}: {msg}"

<<<<<<< HEAD
def strip_comments(text: str) -> list[str]:
    """Return per-line *code-only* strings with comments removed.

    Important: comments are **skipped**, not replaced with whitespace.
    This avoids introducing artificial spaces that could trigger style checks.

    Handles:
    - // line comments
    - /* block comments */ (including multi-line)
    - ignores comment markers inside string/char literals
    """

    out_lines: list[list[str]] = [[]]
    in_block = False
    in_str = False
    in_char = False
    escape = False

    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""

        if ch == "\n":
            out_lines.append([])
            escape = False
            i += 1
            continue

        # If we're inside a /* ... */ block comment, only look for the end.
        if in_block:
            if ch == "*" and nxt == "/":
                in_block = False
                i += 2
                continue
            i += 1
            continue

        # Inside string/char: keep everything, but track escapes.
        if in_str or in_char:
            out_lines[-1].append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif in_str and ch == '"':
                in_str = False
            elif in_char and ch == "'":
                in_char = False
            i += 1
            continue

        # Not in comment or literal: detect comment starts.
        if ch == "/" and nxt == "/":
            # skip rest of line
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            continue

        if ch == "/" and nxt == "*":
            in_block = True
            i += 2
            continue

        if ch == '"':
            in_str = True
            out_lines[-1].append(ch)
            i += 1
            continue

        if ch == "'":
            in_char = True
            out_lines[-1].append(ch)
            i += 1
            continue

        out_lines[-1].append(ch)
        i += 1

    # Preserve the original number of lines (splitlines()) behavior.
    return ["".join(parts) for parts in out_lines]

=======
>>>>>>> tests
def indent_columns(prefix: str, tab_width: int) -> int:
    cols = 0
    for ch in prefix:
        cols += tab_width if ch == "\t" else 1
    return cols

def first_nonempty_index(lines: list[str], start: int) -> int | None:
    for i in range(start, len(lines)):
        if lines[i].strip() != "":
            return i
    return None

def check_license(rel: Path, lines: list[str], rules: Rules) -> list[str]:
    if not lines:
        return [err(rel, 1, "file is empty, missing license header")]
    if not lines[0].lstrip().startswith("/*"):
        return [err(rel, 1, "missing license block comment at file start (/* ... */)")]
    header = "\n".join(lines[: max(1, rules.license_scan_lines)])
    if rules.license_required_substring not in header:
        return [err(rel, 1, f"license header missing '{rules.license_required_substring}'")]
    return []

def is_probable_function_definition_start(lines: list[str], i: int) -> bool:
    """Detect function definition starting at line i (0-based)."""
    line = lines[i]
    s = line.strip()
    if not s or COMMENT_OR_PREPROC.match(s):
        return False
    # Must contain a ')' somewhere (function-ish)
    if ")" not in line:
        return False
    # Reject prototypes ending with ';'
    if s.endswith(";"):
        return False
    # Easy case: `{` on same line after ')'
    if FUNC_LINE_HAS_OPEN_BRACE.search(line):
        return True
    # Next non-empty line is '{'
    j = first_nonempty_index(lines, i + 1)
    if j is not None and lines[j].strip() == "{":
        # We require the current line to look like a signature end.
        if FUNC_LINE_HAS_PAREN.search(line):
            return True
    return False

def is_probable_class_struct_definition_start(lines: list[str], i: int) -> bool:
    line = lines[i]
    s = line.strip()
    if not s or COMMENT_OR_PREPROC.match(s):
        return False
    if not CLASS_STRUCT_LINE.match(line):
        return False
    # Forward declaration: `class X;`
    if s.endswith(";") and "{" not in s:
        return False
    if "{" in s:
        return True
    j = first_nonempty_index(lines, i + 1)
    if j is not None and lines[j].strip() == "{":
        return True
    return False

def find_matching_brace_end(lines: list[str], start_i: int) -> int | None:
    """
    Find end line index (0-based) of a brace-delimited definition starting at start_i.
    Very simple brace counter, ignores strings/comments (good enough for style checking).
    """
    depth = 0
    started = False
    for i in range(start_i, len(lines)):
        l = lines[i]
        # Count braces
        opens = l.count("{")
        closes = l.count("}")
        if opens > 0:
            depth += opens
            started = True
        if closes > 0:
            depth -= closes
        if started and depth <= 0:
            return i
    return None

<<<<<<< HEAD
def check_blank_lines_around_definitions(rel: Path, code_lines: list[str], raw_lines: list[str]) -> list[str]:
    """Require a blank line before/after brace-delimited definitions.

    This uses *code-only* lines for detecting where definitions start/end, but it
    checks blank lines using the raw file lines.
    """

    errors: list[str] = []
    i = 0
    while i < len(code_lines):
        if is_probable_class_struct_definition_start(code_lines, i) or is_probable_function_definition_start(code_lines, i):
            start = i
            end = find_matching_brace_end(code_lines, start)
=======
def check_blank_lines_around_definitions(rel: Path, lines: list[str]) -> list[str]:
    errors: list[str] = []

    # Find include block end to avoid forcing a blank line "before a definition"
    # if it immediately follows include+required blank line.
    include_idxs = [idx for idx, l in enumerate(lines) if l.startswith("#include")]
    include_block_end = include_idxs[-1] if include_idxs else None

    i = 0
    while i < len(lines):
        if is_probable_class_struct_definition_start(lines, i) or is_probable_function_definition_start(lines, i):
            start = i
            end = find_matching_brace_end(lines, start)
>>>>>>> tests
            if end is None:
                i += 1
                continue

<<<<<<< HEAD
            # blank line before
            if start > 0 and raw_lines[start - 1].strip() != "":
                errors.append(err(rel, start + 1, "missing blank line before definition"))

            # blank line after
            if end + 1 < len(raw_lines) and raw_lines[end + 1].strip() != "":
                errors.append(err(rel, end + 2, "missing blank line after definition"))
=======
            # ---- blank line before start ----
            # Don’t require if start is the first non-empty line after includes+blankline region.
            prev_nonempty = None
            for k in range(start - 1, -1, -1):
                if lines[k].strip() != "":
                    prev_nonempty = k
                    break
            # Require that the line directly above start is blank, unless we're at top-ish
            if start > 0:
                if lines[start - 1].strip() != "":
                    # Allow: directly after include block if there was already a blank line rule
                    # but the rule you want is: there *should* be empty lines before/after definitions,
                    # so we enforce strictly (this is what you asked).
                    errors.append(err(rel, start + 1, "missing blank line before definition"))

            # ---- blank line after end ----
            if end + 1 < len(lines):
                if lines[end + 1].strip() != "":
                    errors.append(err(rel, end + 1, "missing blank line after definition"))
>>>>>>> tests

            i = end + 1
            continue

        i += 1

    return errors

def check_file(repo_root: Path, file_path: Path, rules: Rules) -> list[str]:
    rel = file_path.relative_to(repo_root)
    errors: list[str] = []

    raw_bytes = file_path.read_bytes()

    # newline at EOF
    if rules.require_newline_at_eof and raw_bytes and not raw_bytes.endswith(b"\n"):
        errors.append(err(rel, 1, "missing newline at end of file"))

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return errors

<<<<<<< HEAD
    raw_lines = text.splitlines()
    code_lines = strip_comments(text)
    if len(code_lines) > len(raw_lines):
        code_lines = code_lines[: len(raw_lines)]

    # license (raw file)
    errors += check_license(rel, raw_lines, rules)

    include_idxs: list[int] = []

    def _check_brace_spacing_line(line: str) -> list[str]:
            """Return a list of human-readable brace spacing errors for one line.

            Rules requested:
            - Before '{' there should always be a space.
            - After '{' a space is required only if something follows it on the same line.
              (If the line ends with '{' (ignoring trailing whitespace), it's fine.)
            - Before '}' there should always be a space, except if '}' is the first
              non-whitespace character on the line.
            - After '}' there must be **no** space if the next token is one of: ';', ',', ')',
              or end-of-line. Otherwise, require a space after '}'.
            """
            out: list[str] = []

            # Work on the raw line; we're only enforcing whitespace immediately adjacent
            # to braces, so trailing whitespace is already handled elsewhere.
            s = line
            n = len(s)

            # Helper: is brace at start-of-line (ignoring indentation whitespace)?
            lstripped = s.lstrip(" \t")
            start_nonws_idx = n - len(lstripped)

            for idx, ch in enumerate(s):
                if ch == "{":
                    # Space before '{' always (unless it's truly at column 0).
                    if idx > 0 and s[idx - 1] not in (" ", "\t"):
                        out.append("missing space before '{'")

                    # Space after '{' only if something follows on the same line.
                    # (i.e. '{' is not the last non-whitespace char)
                    # Find if there is any non-whitespace after idx.
                    has_after = any(c not in (" ", "\t") for c in s[idx + 1 :])
                    if has_after:
                        if idx + 1 < n and s[idx + 1] not in (" ", "\t"):
                            out.append("missing space after '{'")

                elif ch == "}":
                    # Space before '}' unless '}' begins the line (ignoring indentation).
                    if idx != start_nonws_idx and idx > 0 and s[idx - 1] not in (" ", "\t"):
                        out.append("missing space before '}'")

                    # After '}' spacing rules.
                    if idx + 1 >= n:
                        continue  # end of line

                    nxt = s[idx + 1]

                    # If there is whitespace after '}', look ahead to the next non-ws.
                    if nxt in (" ", "\t"):
                        j = idx + 1
                        while j < n and s[j] in (" ", "\t"):
                            j += 1
                        if j >= n:
                            continue  # whitespace until EOL is fine
                        if s[j] in (";", ",", ")"):
                            out.append("unexpected space after '}' before ';', ',', or ')'")
                        # Otherwise ok: there is a space after '}' before a keyword/token.
                        continue

                    # No whitespace after '}'. If it immediately closes with these, it's fine.
                    if nxt in (";", ",", ")"):
                        continue

                    # Otherwise require a space after '}' (e.g. `} else`).
                    out.append("missing space after '}'")

            return out

    # Single-pass per-line checks (fast + consistent)
    for idx0, (raw, code) in enumerate(zip(raw_lines, code_lines), start=0):
        lineno = idx0 + 1

        raw_strip = raw.strip()
        raw_lstrip = raw.lstrip(" \t")
        is_commentish = raw_lstrip.startswith("//") or raw_lstrip.startswith("/*") or raw_lstrip.startswith("*") or raw_lstrip.startswith("*/")
        has_code = code.strip() != ""

        # include block detection uses the raw file
        if raw_lstrip.startswith("#include"):
            include_idxs.append(idx0)

        # --- file-level line style checks (raw file) ---
        if rules.forbid_trailing_whitespace and raw.rstrip(" \t") != raw:
            errors.append(err(rel, lineno, "trailing whitespace"))

        if rules.max_line_length > 0 and len(raw) > rules.max_line_length:
            errors.append(err(rel, lineno, f"line exceeds {rules.max_line_length} chars (got {len(raw)})"))

        # indentation: skip comment-only lines to avoid comment-filter artefacts
        if not is_commentish and raw_strip:
            leading_len = len(raw) - len(raw.lstrip(" \t"))
            if leading_len > 0:
                prefix = raw[:leading_len]
                if rules.indentation_tabs_only and " " in prefix:
                    errors.append(err(rel, lineno, "spaces used for indentation (tabs only)"))
                if rules.indent_multiple_of > 0:
                    cols = indent_columns(prefix, rules.tab_width)
                    if cols % rules.indent_multiple_of != 0:
                        errors.append(err(rel, lineno, f"indentation {cols} columns not multiple of {rules.indent_multiple_of}"))

        # From here on: skip lines with no code after comment stripping
        if not has_code:
            continue

        # --- operator spacing (code-only) ---
        if rules.require_space_around_operators and OPERATOR_RE.search(code):
            errors.append(err(rel, lineno, "missing spaces around operator"))

        # --- keyword spacing (code-only) ---
        if rules.require_space_after_keywords:
            if KW_AFTER_RE.search(code):
                errors.append(err(rel, lineno, "missing space after keyword (use 'if (' / 'for (' etc.)"))
            if ELSEIF_AFTER_RE.search(code):
                errors.append(err(rel, lineno, "missing space in 'else if ('"))

        if rules.require_space_before_keywords:
            m = KW_BEFORE_RE.search(code)
            if m:
                before = m.group(1)
                kw = m.group(2)
                errors.append(err(rel, lineno, f"missing space before keyword '{kw}' (after '{before}')"))

        # --- brace spacing (code-only) ---
        if rules.require_space_around_braces:
            for msg in _check_brace_spacing_line(code):
                errors.append(err(rel, lineno, msg))

        # --- pointer/reference style (code-only) ---
        if rules.pointer_reference_style == "type_space_starvar":
            if BAD_PTR_REF_RE.search(code) or NO_SPACE_PTR_REF_RE.search(code) or SPACE_BETWEEN_PTR_REF_RE.search(code):
                if not GOOD_PTR_REF_RE.search(code):
                    errors.append(err(rel, lineno, "pointer/reference style: use 'int *var' / 'int &var'"))

        # --- typedef struct suffix (code-only) ---
        m = TYPEDEF_STRUCT_RE.search(code)
        if m:
            name = m.group(1)
            if rules.typedef_struct_suffix and name and not name.endswith(rules.typedef_struct_suffix):
                errors.append(err(rel, lineno, f"typedef struct name must end with '{rules.typedef_struct_suffix}'"))

        # --- class naming (code-only) ---
        if rules.class_name_capitalized:
            m2 = CLASS_RE.search(code)
            if m2 and not m2.group(1)[0].isupper():
                errors.append(err(rel, lineno, "class name must start with capital letter"))

    # include blank line before/after include block
=======
    lines = text.splitlines()

    # license
    errors += check_license(rel, lines, rules)

    # trailing whitespace, max line length, indentation rules
    for i, l in enumerate(lines, 1):
        if rules.forbid_trailing_whitespace and l.rstrip(" \t") != l:
            errors.append(err(rel, i, "trailing whitespace"))

        if rules.max_line_length > 0 and len(l) > rules.max_line_length:
            errors.append(err(rel, i, f"line exceeds {rules.max_line_length} chars (got {len(l)})"))

        leading_len = len(l) - len(l.lstrip(" \t"))
        if leading_len > 0:
            prefix = l[:leading_len]
            if rules.indentation_tabs_only and " " in prefix:
                errors.append(err(rel, i, "spaces used for indentation (tabs only)"))
            if rules.indent_multiple_of > 0:
                cols = indent_columns(prefix, rules.tab_width)
                if cols % rules.indent_multiple_of != 0:
                    errors.append(err(rel, i, f"indentation {cols} columns not multiple of {rules.indent_multiple_of}"))

    # include blank line before/after include block
    include_idxs = [idx for idx, l in enumerate(lines) if l.startswith("#include")]
>>>>>>> tests
    if include_idxs:
        first = include_idxs[0]
        last = include_idxs[-1]
        if rules.require_blank_line_before_includes:
<<<<<<< HEAD
            if first == 0 or (raw_lines[first - 1].strip() != "" and not raw_lines[first - 1].lstrip().startswith("#include")):
                errors.append(err(rel, first + 1, "missing blank line before include block"))
        if rules.require_blank_line_after_includes:
            if last + 1 >= len(raw_lines) or (raw_lines[last + 1].strip() != "" and not raw_lines[last + 1].lstrip().startswith("#include")):
                errors.append(err(rel, last + 2, "missing blank line after include block"))

    # blank lines around *definitions* only (use code-only for detection)
    if rules.require_blank_lines_around_definitions:
        errors.extend(check_blank_lines_around_definitions(rel, code_lines, raw_lines))
=======
            if first == 0 or (lines[first - 1].strip() != "" and not lines[first - 1].strip().startswith("#include")):
                errors.append(err(rel, first + 1, "missing blank line before include block"))
        if rules.require_blank_line_after_includes:
            if last + 1 >= len(lines) or (lines[last + 1].strip() != "" and not lines[last + 1].strip().startswith("#include")):
                errors.append(err(rel, last + 1, "missing blank line after include block"))

    # operator spacing
    if rules.require_space_around_operators:
        for i, l in enumerate(lines, 1):
            if OPERATOR_RE.search(l):
                errors.append(err(rel, i, "missing spaces around operator"))

    # keyword spacing: after + before
    if rules.require_space_after_keywords:
        for i, l in enumerate(lines, 1):
            if KW_AFTER_RE.search(l):
                errors.append(err(rel, i, "missing space after keyword (use 'if (' / 'for (' etc.)"))
            if ELSEIF_AFTER_RE.search(l):
                errors.append(err(rel, i, "missing space in 'else if ('"))

    if rules.require_space_before_keywords:
        for i, l in enumerate(lines, 1):
            m = KW_BEFORE_RE.search(l)
            if m:
                before = m.group(1)
                kw = m.group(2)
                errors.append(err(rel, i, f"missing space before keyword '{kw}' (after '{before}')"))

    # brace spacing
    if rules.require_space_around_braces:
        for i, l in enumerate(lines, 1):
            if "{" in l and not l.rstrip().endswith("{") and not l.rstrip().endswith("{;"):
                if not re.search(r"\s\{", l):
                    errors.append(err(rel, i, "missing space before '{'"))
            if "}" in l and l.strip() != "}":
                if not re.search(r"\}\s", l) and not l.rstrip().endswith("};"):
                    errors.append(err(rel, i, "missing space after '}'"))

    # pointer/reference style: allowed `int *var` / `int &var`
    if rules.pointer_reference_style == "type_space_starvar":
        for i, l in enumerate(lines, 1):
            if BAD_PTR_REF_RE.search(l) or NO_SPACE_PTR_REF_RE.search(l) or SPACE_BETWEEN_PTR_REF_RE.search(l):
                if not GOOD_PTR_REF_RE.search(l):
                    errors.append(err(rel, i, "pointer/reference style: use 'int *var' / 'int &var'"))

    # typedef struct suffix
    for i, l in enumerate(lines, 1):
        m = TYPEDEF_STRUCT_RE.search(l)
        if m:
            name = m.group(1)
            if rules.typedef_struct_suffix and not name.endswith(rules.typedef_struct_suffix):
                errors.append(err(rel, i, f"typedef struct name must end with '{rules.typedef_struct_suffix}'"))

    # class naming
    if rules.class_name_capitalized:
        for i, l in enumerate(lines, 1):
            m = CLASS_RE.search(l)
            if m and not m.group(1)[0].isupper():
                errors.append(err(rel, i, "class name must start with capital letter"))

    # NEW: blank lines around *definitions* only
    if rules.require_blank_lines_around_definitions:
        errors.extend(check_blank_lines_around_definitions(rel, lines))
>>>>>>> tests

    return errors

def should_exclude(path: Path, exclude_fragments: list[str]) -> bool:
    s = str(path).replace("\\", "/")
    return any(frag in s for frag in exclude_fragments)

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    cfg_path = repo_root / ".physim-format.yml"
    if not cfg_path.exists():
        print(f"format_check: missing config: {cfg_path}", file=sys.stderr)
        return 2

    cfg = load_simple_yaml(cfg_path)
    include_dirs = cfg.get("include", ["src", "include", "tests"])
    exclude_frags = cfg.get("exclude", ["build", ".git", "third_party", "vendor", "external"])
    exts = set(cfg.get("extensions", EXT_DEFAULT))

    r = cfg.get("rules", {})
    rules = Rules(
        max_line_length=int(r.get("max_line_length", 88)),
        forbid_trailing_whitespace=bool(r.get("forbid_trailing_whitespace", True)),
        require_newline_at_eof=bool(r.get("require_newline_at_eof", True)),
        indentation_tabs_only=bool(r.get("indentation_tabs_only", True)),
        tab_width=int(r.get("tab_width", 2)),
        indent_multiple_of=int(r.get("indent_multiple_of", 2)),
        require_space_after_keywords=bool(r.get("require_space_after_keywords", True)),
        require_space_before_keywords=bool(r.get("require_space_before_keywords", True)),
        require_space_around_operators=bool(r.get("require_space_around_operators", True)),
        require_space_around_braces=bool(r.get("require_space_around_braces", True)),
        require_blank_line_before_includes=bool(r.get("require_blank_line_before_includes", True)),
        require_blank_line_after_includes=bool(r.get("require_blank_line_after_includes", True)),
        require_blank_lines_around_definitions=bool(r.get("require_blank_lines_around_definitions", True)),
        pointer_reference_style=str(r.get("pointer_reference_style", "type_space_starvar")),
        typedef_struct_suffix=str(r.get("typedef_struct_suffix", "_t")),
        class_name_capitalized=bool(r.get("class_name_capitalized", True)),
        license_required_substring=str(r.get("license_required_substring", LICENSE)),
<<<<<<< HEAD
        license_scan_lines=int(r.get("license_scan_lines", 20)),
=======
        license_scan_lines=int(r.get("license_scan_lines", 30)),
>>>>>>> tests
    )

    all_errors: list[str] = []

    for d in include_dirs:
        base = repo_root / d
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix not in exts:
                continue
            if should_exclude(f, exclude_frags):
                continue
            all_errors.extend(check_file(repo_root, f, rules))

    if all_errors:
        for e in all_errors:
            print(e)
        print("\nformat_check: FAILED")
        return 1

    print("format_check: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
