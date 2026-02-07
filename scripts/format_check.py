#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Rules:
    max_line_length: int = 88
    forbid_trailing_whitespace: bool = True
    required_newline_at_eof: bool = True
    indent_multiple_of: int = 2

def load_config(path: Path) -> dict:
    data = {}
    current = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line and not line.startswith("-"):
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v == "":
                data[k] = []
                current = k
            else:
                try:
                    data[k] = int(v)
                except ValueError:
                    data[k] = v.lower() == "true" if v.lower() in ("true", "false") else v
                current = None
        elif line.startswith("-") and current:
            data[current].append(line[1:].strip())
    return data

def should_exclude(path: Path, excludes: list[str]) -> bool:
    s = str(path)
    return any(e in s for e in excludes)

def check_file(path: Path, rules: Rules) -> list[str]:
    errors: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return errors

    lines = content.splitlines(keepends=True)

    if rules.required_newline_at_eof and content and not content.endswith("\n"):
        errors.append("missing newline at end of file")

    for i, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n")

        if rules.forbid_trailing_whitespace and stripped != stripped.rstrip(" "):
            errors.append(f"line {i}: trailing whitespace")

        if rules.max_line_length > 0 and len(stripped) > rules.max_line_length:
            errors.append(f"line: {i}: exceeds max length {rules.max_line_length}")

        if rules.indent_multiple_of > 0 and stripped:
            leading = len(stripped) - len(stripped.lstrip(" "))
            if leading > 0 and leading % rules.indent_multiple_of != 0:
                errors.append(f"line {i}: indentation {leading} not multiple of {rules.indent_multiple_of}")

    return errors

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cfg = load_config(root / ".physim-format.yml")

    rules = Rules(
            max_line_length=int(cfg.get("rules.max_line_length", cfg.get("max_line_length", 88))),
            forbid_trailing_whitespace=True,
            required_newline_at_eof=True,
            indent_multiple_of=int(cfg.get("indent_multiple_of", 2)),
            )
        
    includes = [root / p for p in cfg.get("includes", ["src", "include", "tests"])]
    excludes = cfg.get("exclude", [])
    exts = set(cfg.get("extensions", []))

    failed = False

    for base in includes:
        if not base.exists():
            continue
        for file in base.rglob("*"):
            if not file.is_file():
                continue
            if should_exclude(file, excludes):
                continue
            if file.suffix not in exts:
                continue

            errors = check_file(file, rules)
            if errors:
                failed = True
                print(file.relative_to(root))
                for e in errors:
                    print("  -", e)
                print()

    if failed:
        print("format_check: FAILED")
        return 1

    print("format_check: PASSED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

