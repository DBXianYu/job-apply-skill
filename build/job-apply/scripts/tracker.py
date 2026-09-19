#!/usr/bin/env python3
"""Check, add, update, and list job applications stored in CSV."""

from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from profile import data_home


FIELDS = ["company", "job_title", "job_id", "job_url", "location", "job_type", "resume_used", "application_date", "status", "last_update", "notes"]
STATUSES = ("discovered", "prepared", "submitted", "oa", "interview", "rejected", "offer", "withdrawn")
TRACKING_QUERY_KEYS = {"from", "source", "ref", "referrer", "tracking", "campaign"}


def csv_path() -> Path:
    return data_home() / "applications.csv"


def normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.casefold() not in {"http", "https"} or not parts.netloc:
        raise ValueError("job URL must be an absolute http(s) URL")
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key.casefold() not in TRACKING_QUERY_KEYS and not key.casefold().startswith("utm_")]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.casefold(), parts.netloc.casefold(), path, urlencode(query), ""))


def ensure_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8-sig") as handle:
            csv.DictWriter(handle, fieldnames=FIELDS).writeheader()


def load_rows(path: Path) -> list[dict[str, str]]:
    ensure_file(path)
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"CSV header must be: {','.join(FIELDS)}")
        return list(reader)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    handle = tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8-sig", delete=False, dir=path.parent, prefix="applications-", suffix=".tmp")
    temp_path = Path(handle.name)
    try:
        with handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def matches(row: dict[str, str], url: str, company: str | None, job_id: str | None) -> bool:
    try:
        same_url = normalize_url(row["job_url"]) == normalize_url(url)
    except ValueError:
        same_url = row["job_url"].strip() == url.strip()
    same_identity = bool(company and job_id and normalize_text(row["company"]) == normalize_text(company) and normalize_text(row["job_id"]) == normalize_text(job_id))
    return same_url or same_identity


def display(rows: list[dict[str, str]]) -> None:
    if not rows:
        print("No applications found.")
        return
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="check duplicates by URL or company + job ID")
    check.add_argument("url")
    check.add_argument("--company")
    check.add_argument("--job-id")
    add = sub.add_parser("add", help="add a new application")
    add.add_argument("url")
    add.add_argument("--company", required=True)
    add.add_argument("--job-title", required=True)
    add.add_argument("--job-id", default="")
    add.add_argument("--location", default="")
    add.add_argument("--job-type", default="")
    add.add_argument("--resume-used", default="")
    add.add_argument("--status", choices=STATUSES, default="discovered")
    add.add_argument("--notes", default="")
    update = sub.add_parser("update", help="update one application selected by URL")
    update.add_argument("url")
    for field in ("company", "job_title", "job_id", "location", "job_type", "resume_used", "notes"):
        update.add_argument(f"--{field.replace('_', '-')}")
    update.add_argument("--status", choices=STATUSES)
    listing = sub.add_parser("list", help="list applications")
    listing.add_argument("--status", choices=STATUSES)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = csv_path()
    try:
        rows = load_rows(path)
        if args.command == "check":
            duplicates = [row for row in rows if matches(row, args.url, args.company, args.job_id)]
            if duplicates:
                print("DUPLICATE")
                display(duplicates)
                return 10
            print("NOT_FOUND")
            return 0
        if args.command == "add":
            if any(matches(row, args.url, args.company, args.job_id or None) for row in rows):
                print("ERROR: duplicate application; use update instead", file=sys.stderr)
                return 10
            now = datetime.now().astimezone().isoformat(timespec="seconds")
            rows.append({"company": args.company, "job_title": args.job_title, "job_id": args.job_id, "job_url": normalize_url(args.url), "location": args.location, "job_type": args.job_type, "resume_used": args.resume_used, "application_date": date.today().isoformat(), "status": args.status, "last_update": now, "notes": args.notes})
            write_rows(path, rows)
            print("ADDED")
            return 0
        if args.command == "update":
            indexes = [index for index, row in enumerate(rows) if matches(row, args.url, None, None)]
            if not indexes:
                print("ERROR: application not found", file=sys.stderr)
                return 4
            if len(indexes) > 1:
                print("ERROR: multiple records match this URL", file=sys.stderr)
                return 5
            row = rows[indexes[0]]
            for field in ("company", "job_title", "job_id", "location", "job_type", "resume_used", "status", "notes"):
                value = getattr(args, field)
                if value is not None:
                    row[field] = value
            row["last_update"] = datetime.now().astimezone().isoformat(timespec="seconds")
            write_rows(path, rows)
            print("UPDATED")
            return 0
        selected = rows if args.status is None else [row for row in rows if row["status"] == args.status]
        display(selected)
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
