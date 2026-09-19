---
name: job-apply
description: Prepare and track a single job application from a recruiting-site URL by reading the JD, semantically mapping form fields to confirmed profile data, selecting and uploading a resume, and pausing for user decisions, verification, legal consent, and final submission. Use for campus, internship, or experienced-hire applications; do not use for bulk applications or bypassing access controls.
---

# Job Apply

Prepare one application safely from URL to a completed, reviewable form. Personal data lives outside this skill in `${JOB_APPLY_HOME:-$HOME/.codex/job-apply}`. Never copy personal facts into the skill directory.

## Start

1. Resolve the data home with `python scripts/profile.py home` and run `python scripts/validate_profile.py`. Read [references/profile-schema.md](references/profile-schema.md) when interpreting or updating personal data. `${JOB_APPLY_HOME}/profile.example.yaml` contains format examples only and must never be used as candidate facts.
2. Read [references/workflow.md](references/workflow.md) for the end-to-end procedure and stopping rules.
3. Before filling, run `python scripts/tracker.py check <job-url>`; after extracting company and job ID, also pass `--company` and `--job-id`. Stop on a submitted or otherwise active duplicate unless the user explicitly decides how to proceed.
4. Read [references/field-mapping.md](references/field-mapping.md) when mapping form labels and sections to profile or answer keys. Read [references/site-adapters.md](references/site-adapters.md) only after the generic workflow fails or a known stable special flow is encountered.

## Browser strategy

Prefer the current Codex browser/computer-use capability. Use a repeated `open -> snapshot -> understand -> fill/select/click/upload -> snapshot` loop. Locate controls by label, role, nearby text, section, input type, and semantic meaning; do not rely on brittle selectors alone.

If terminal browser automation is genuinely needed, first check `npx` and `${CODEX_HOME:-$HOME/.codex}/skills/playwright`. Use the official Playwright skill when available. Do not create a Selenium or Playwright framework inside this skill.

Extract and retain the company, title, job ID, location, category, full JD, recruitment type, and canonical URL. Use generic semantic handling first. When the page rerenders or a control fails, take a fresh snapshot and remap it before consulting a site adapter.

## Data and answer rules

- Fill only facts present in validated `profile.yaml`, documents the user supplied, or answers the user confirmed in the current conversation.
- Treat `profile.example.yaml` and any key named `example` as documentation, never as fillable data.
- For internship, project, and research narrative fields, use the record's `resume_text` by default when it is present. It preserves the resume's direct wording with layout-only line breaks removed. Keep the structured fields for matching, short fields, and form sections. Shorten or reorganize `resume_text` only when the target field requires it, and never change facts or metrics.
- Reuse `answers.yaml` when a question is semantically equivalent. Lightly tailor wording to the JD while preserving every fact, commitment, and preference.
- Select a resume with `python scripts/profile.py choose-resume --jd-file <file>`. The command applies `preferences.yaml` keyword rules and falls back to `general.pdf`. If the selected file does not exist, pause and report its path.
- Treat empty strings, null values, missing keys, and empty lists as unknown. Never infer an unknown value from convention or from another field.

Pause for CAPTCHA, SMS codes, MFA, QR login, face verification, personal choices, sensitive attributes, legal declarations, privacy/background-check consent, non-compete statements, or any uncertain fact. The user must perform authentication steps and explicitly decide or consent where required.

## Submission boundary

Never activate the final `Submit`, `Apply`, `Confirm Application`, or an equivalent localized control without explicit confirmation for the prepared form. Before asking, show:

- company, title, location, job ID, and job type;
- selected resume and other uploaded documents;
- fields filled from confirmed facts;
- reused or adapted free-text answers;
- any resume wording that was shortened or reorganized because of a field limit;
- every unresolved field, choice, warning, and declaration.

After explicit confirmation, submit once and inspect the resulting page. Record `submitted` only when the site provides credible success evidence. Otherwise record `prepared` or a truthful note; never manufacture success.

## Tracking and learning

Use `scripts/tracker.py` to add or update `applications.csv`. Supported statuses are `discovered`, `prepared`, `submitted`, `oa`, `interview`, `rejected`, `offer`, and `withdrawn`.

After a run, propose durable field aliases, stable site-flow notes, or answer-memory additions when useful. Do not silently change personal facts or preferences. V1 handles one job at a time; do not expand into crawling, bulk applying, account creation, anti-detection, or CAPTCHA bypass.
