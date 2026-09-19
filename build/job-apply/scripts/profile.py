#!/usr/bin/env python3
"""Read job-apply data and choose a resume without modifying personal facts."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install it with: python -m pip install PyYAML") from exc


DATA_FILES = ("profile.yaml", "answers.yaml", "preferences.yaml")


def data_home() -> Path:
    configured = os.environ.get("JOB_APPLY_HOME")
    return Path(configured).expanduser().resolve() if configured else (Path.home() / ".codex" / "job-apply").resolve()


def load_yaml(name: str, *, home: Path | None = None) -> dict[str, Any]:
    if name not in DATA_FILES:
        raise ValueError(f"Unsupported data file: {name}")
    path = (home or data_home()) / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}")
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping at the top level")
    return value


def get_path(value: Any, dotted_path: str) -> Any:
    current = value
    for part in dotted_path.split("."):
        match = re.fullmatch(r"([^\[\]]+)(?:\[(\d+)\])?", part)
        if not match or not isinstance(current, dict) or match.group(1) not in current:
            raise KeyError(dotted_path)
        current = current[match.group(1)]
        if match.group(2) is not None:
            if not isinstance(current, list):
                raise KeyError(dotted_path)
            index = int(match.group(2))
            if index >= len(current):
                raise KeyError(dotted_path)
            current = current[index]
    return current


def is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def choose_resume(jd: str, preferences: dict[str, Any], *, home: Path | None = None) -> tuple[Path, str, int]:
    rules = preferences.get("resume_rules", {})
    if rules is None:
        rules = {}
    if not isinstance(rules, dict):
        raise ValueError("preferences.yaml: resume_rules must be a mapping")
    normalized_jd = jd.casefold()
    resume_home = (home or data_home()) / "resumes"
    candidates: list[tuple[int, int, str, Path]] = []
    for order, (rule_name, rule) in enumerate(rules.items()):
        if not isinstance(rule_name, str) or not isinstance(rule, dict):
            continue
        keywords = rule.get("keywords", [])
        if not isinstance(keywords, list):
            raise ValueError(f"resume_rules.{rule_name}.keywords must be a list")
        score = sum(1 for keyword in keywords if isinstance(keyword, str) and keyword.strip() and keyword.casefold() in normalized_jd)
        name = rule_name if rule_name.lower().endswith(".pdf") else f"{rule_name}.pdf"
        path = resume_home / name
        if score > 0 and path.is_file():
            candidates.append((score, -order, name, path))
    if candidates:
        score, _, name, path = max(candidates)
        return path.resolve(), name, score
    name = "general.pdf"
    path = resume_home / name
    return path.resolve(), name, 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("home", help="print the resolved job-apply data directory")
    show = sub.add_parser("show", help="print a YAML data file")
    show.add_argument("file", choices=[name.removesuffix(".yaml") for name in DATA_FILES])
    get = sub.add_parser("get", help="read a dotted profile path, e.g. education[0].school")
    get.add_argument("path")
    choose = sub.add_parser("choose-resume", help="select the resume matching a JD")
    source = choose.add_mutually_exclusive_group(required=True)
    source.add_argument("--jd", help="JD text")
    source.add_argument("--jd-file", type=Path, help="UTF-8 file containing the JD")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    home = data_home()
    try:
        if args.command == "home":
            print(home)
        elif args.command == "show":
            value = load_yaml(f"{args.file}.yaml", home=home)
            print(yaml.safe_dump(value, allow_unicode=True, sort_keys=False).rstrip())
        elif args.command == "get":
            value = get_path(load_yaml("profile.yaml", home=home), args.path)
            if is_empty(value):
                print(f"UNKNOWN: {args.path}", file=sys.stderr)
                return 2
            print(yaml.safe_dump(value, allow_unicode=True, sort_keys=False).rstrip())
        elif args.command == "choose-resume":
            jd = args.jd if args.jd is not None else args.jd_file.read_text(encoding="utf-8")
            path, name, score = choose_resume(jd, load_yaml("preferences.yaml", home=home), home=home)
            print(path)
            print(f"selection={name} keyword_matches={score}")
            if not path.is_file():
                print(f"MISSING_RESUME: {path}", file=sys.stderr)
                return 3
        return 0
    except (FileNotFoundError, KeyError, ValueError, OSError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
