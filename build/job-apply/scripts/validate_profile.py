#!/usr/bin/env python3
"""Validate job-apply YAML structure and report incomplete profile fields."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from profile import DATA_FILES, data_home, is_empty, load_yaml


TOP_LEVEL = {
    "schema_version": int,
    "basic": dict,
    "identification": dict,
    "education": list,
    "internships": list,
    "projects": list,
    "research": list,
    "skills": list,
    "languages": list,
    "publications": list,
    "patents": list,
    "academic_conferences": list,
    "competition_awards": list,
    "scholarships": list,
    "certificates": list,
    "attachments": list,
    "company_specific": dict,
    "links": dict,
    "job_preferences": dict,
}
BASIC_KEYS = (
    "name_zh", "name_en", "gender", "birth_date", "phone", "email",
    "current_location", "native_place", "ethnicity", "political_status",
    "marital_status", "photo_path", "self_evaluation",
)
EDUCATION_KEYS = (
    "school", "country_or_region", "province", "city", "college", "major",
    "degree", "study_mode", "start_date", "end_date", "gpa", "gpa_scale",
    "rank", "student_id", "research_direction", "advisor_name",
    "is_national_key_laboratory", "is_student_cadre", "courses",
)
INTERNSHIP_KEYS = (
    "company", "department", "role", "employment_type", "location",
    "start_date", "end_date", "resume_text", "responsibilities", "technologies",
)
PROJECT_KEYS = (
    "name", "role", "start_date", "end_date", "resume_text", "description",
    "responsibilities", "technologies", "outcomes",
)
RESEARCH_KEYS = (
    "name", "role", "start_date", "end_date", "resume_text", "paper_title", "datasets",
    "responsibilities", "technologies", "outcomes",
)
JOB_PREFERENCE_KEYS = (
    "job_types", "directions", "preferred_cities", "accept_location_change",
    "accept_position_adjustment", "expected_salary", "willing_to_travel",
    "willing_to_work_overtime", "willing_for_overseas_assignment",
)
ANSWER_SECTIONS = {"objective": dict, "behavioral": dict, "preferences": dict, "companies": dict}
DATE_PATTERN = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])(?:-(?:0[1-9]|[12]\d|3[01]))?$")


def type_label(expected: type) -> str:
    return {dict: "mapping", list: "list", str: "string", int: "integer"}.get(expected, expected.__name__)


def require_shape(data: dict[str, Any], shape: dict[str, type], prefix: str, errors: list[str]) -> None:
    for key, expected in shape.items():
        path = f"{prefix}.{key}" if prefix else key
        if key not in data:
            errors.append(f"missing key: {path}")
        elif not isinstance(data[key], expected) or isinstance(data[key], bool) and expected is int:
            errors.append(f"{path} must be a {type_label(expected)}")


def require_keys(record: dict[str, Any], keys: tuple[str, ...], prefix: str, errors: list[str]) -> None:
    for key in keys:
        if key not in record:
            errors.append(f"missing key: {prefix}.{key}")


def validate_date(value: Any, path: str, errors: list[str]) -> None:
    if value is not None and (not isinstance(value, str) or not DATE_PATTERN.fullmatch(value)):
        errors.append(f"{path} must be null, YYYY-MM, or YYYY-MM-DD")


def validate_string_list(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{path} must be a list of non-empty strings")


def collect_empty_paths(value: Any, path: str, incomplete: list[str]) -> None:
    if value is None or value == "":
        incomplete.append(path)
    elif isinstance(value, dict):
        for key, child in value.items():
            collect_empty_paths(child, f"{path}.{key}" if path else key, incomplete)
    elif isinstance(value, list):
        if not value:
            incomplete.append(f"{path}[]")
        else:
            for index, child in enumerate(value):
                collect_empty_paths(child, f"{path}[{index}]", incomplete)


def validate_record_list(data: dict[str, Any], section: str, keys: tuple[str, ...], errors: list[str]) -> None:
    records = data.get(section)
    if not isinstance(records, list):
        return
    for index, record in enumerate(records):
        prefix = f"profile.{section}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        require_keys(record, keys, prefix, errors)


def validate_profile(profile: dict[str, Any], errors: list[str], incomplete: list[str]) -> None:
    require_shape(profile, TOP_LEVEL, "profile", errors)
    if profile.get("schema_version") != 2:
        errors.append("profile.schema_version must be 2")

    basic = profile.get("basic")
    if isinstance(basic, dict):
        require_keys(basic, BASIC_KEYS, "profile.basic", errors)
        validate_date(basic.get("birth_date"), "profile.basic.birth_date", errors)
        email = basic.get("email")
        if email and (not isinstance(email, str) or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email)):
            errors.append("profile.basic.email is not a plausible email address")
        phone = basic.get("phone")
        if isinstance(phone, dict):
            require_keys(phone, ("country_code", "number"), "profile.basic.phone", errors)
            if phone.get("country_code") is not None and not isinstance(phone.get("country_code"), str):
                errors.append("profile.basic.phone.country_code must be a string or null")
            if phone.get("number") is not None and not isinstance(phone.get("number"), str):
                errors.append("profile.basic.phone.number must be a string or null")
        elif phone is not None:
            errors.append("profile.basic.phone must be a mapping or null")
        location = basic.get("current_location")
        if isinstance(location, dict):
            require_keys(location, ("country_or_region", "province", "city"), "profile.basic.current_location", errors)
        elif location is not None:
            errors.append("profile.basic.current_location must be a mapping or null")

    identification = profile.get("identification")
    if isinstance(identification, dict):
        require_keys(identification, ("document_type", "document_number", "issuing_country_or_region"), "profile.identification", errors)

    validate_record_list(profile, "education", EDUCATION_KEYS, errors)
    validate_record_list(profile, "internships", INTERNSHIP_KEYS, errors)
    validate_record_list(profile, "projects", PROJECT_KEYS, errors)
    validate_record_list(profile, "research", RESEARCH_KEYS, errors)
    for section in ("education", "internships", "projects", "research"):
        for index, record in enumerate(profile.get(section, [])):
            if not isinstance(record, dict):
                continue
            validate_date(record.get("start_date"), f"profile.{section}[{index}].start_date", errors)
            validate_date(record.get("end_date"), f"profile.{section}[{index}].end_date", errors)
            if section in ("internships", "projects", "research"):
                resume_text = record.get("resume_text")
                if not isinstance(resume_text, str) or not resume_text.strip():
                    errors.append(f"profile.{section}[{index}].resume_text must be a non-empty string")

    for index, record in enumerate(profile.get("skills", [])):
        if not isinstance(record, dict):
            errors.append(f"profile.skills[{index}] must be a mapping")
            continue
        require_keys(record, ("category", "items"), f"profile.skills[{index}]", errors)
        validate_string_list(record.get("items"), f"profile.skills[{index}].items", errors)
    for index, record in enumerate(profile.get("languages", [])):
        if not isinstance(record, dict):
            errors.append(f"profile.languages[{index}] must be a mapping")
            continue
        require_keys(record, ("language", "proficiency", "certificate", "score", "score_scale"), f"profile.languages[{index}]", errors)
    for index, record in enumerate(profile.get("attachments", [])):
        if not isinstance(record, dict):
            errors.append(f"profile.attachments[{index}] must be a mapping")
            continue
        require_keys(record, ("type", "path", "description"), f"profile.attachments[{index}]", errors)

    links = profile.get("links")
    if isinstance(links, dict):
        require_keys(links, ("github", "homepage"), "profile.links", errors)
    preferences = profile.get("job_preferences")
    if isinstance(preferences, dict):
        require_keys(preferences, JOB_PREFERENCE_KEYS, "profile.job_preferences", errors)
        for key in ("job_types", "directions", "preferred_cities"):
            if key in preferences:
                validate_string_list(preferences[key], f"profile.job_preferences.{key}", errors)


def validate_preferences(preferences: dict[str, Any], errors: list[str]) -> None:
    rules = preferences.get("resume_rules")
    if not isinstance(rules, dict):
        errors.append("preferences.resume_rules must be a mapping")
        return
    for name, rule in rules.items():
        if not isinstance(name, str) or not name.strip():
            errors.append("each resume rule name must be a non-empty string")
        if not isinstance(rule, dict) or not isinstance(rule.get("keywords"), list):
            errors.append(f"preferences.resume_rules.{name}.keywords must be a list")
        elif any(not isinstance(keyword, str) or not keyword.strip() for keyword in rule["keywords"]):
            errors.append(f"preferences.resume_rules.{name}.keywords must contain non-empty strings")


def load_example(home: Path, errors: list[str]) -> None:
    path = home / "profile.example.yaml"
    if not path.is_file():
        errors.append(f"missing example template: {path}")
        return
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"invalid {path}: {exc}")
        return
    if not isinstance(value, dict):
        errors.append(f"{path} must contain a YAML mapping")
        return
    example_errors: list[str] = []
    validate_profile(value, example_errors, [])
    errors.extend(f"profile.example.yaml: {error}" for error in example_errors)
    for section in (
        "education", "internships", "projects", "research", "skills", "languages",
        "publications", "patents", "academic_conferences", "competition_awards",
        "scholarships", "certificates", "attachments",
    ):
        if not value.get(section):
            errors.append(f"profile.example.yaml must include at least one {section} example")


def main() -> int:
    home = data_home()
    errors: list[str] = []
    incomplete: list[str] = []
    values: dict[str, dict[str, Any]] = {}
    for name in DATA_FILES:
        try:
            values[name] = load_yaml(name, home=home)
        except (FileNotFoundError, ValueError, OSError, yaml.YAMLError) as exc:
            errors.append(str(exc))
    if "profile.yaml" in values:
        validate_profile(values["profile.yaml"], errors, incomplete)
        collect_empty_paths(values["profile.yaml"], "", incomplete)
    if "answers.yaml" in values:
        require_shape(values["answers.yaml"], ANSWER_SECTIONS, "answers", errors)
    if "preferences.yaml" in values:
        validate_preferences(values["preferences.yaml"], errors)
    load_example(home, errors)
    for directory in ("resumes", "documents"):
        if not (home / directory).is_dir():
            errors.append(f"missing directory: {home / directory}")
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID: {home}")
    if incomplete:
        print("NEEDS_USER_INPUT:")
        for path in dict.fromkeys(incomplete):
            print(f"- {path}")
    else:
        print("PROFILE_COMPLETE_FOR_SCHEMA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
