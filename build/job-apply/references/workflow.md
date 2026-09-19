# Job application and resume-profile workflow

## 1. Load and validate local data

Resolve the data directory through `scripts/profile.py`; do not assume a platform-specific home path. Validate YAML before opening or changing a form. Validation reports structural errors separately from intentionally incomplete profile fields.

Read `profile.yaml`, `answers.yaml`, and `preferences.yaml`. Treat all empty values as unknown. Inventory available files under `resumes/` and `documents/` without inventing paths.

## 2. Inspect the target

First classify the request:

- `resume_update`: the supplied page is a reusable recruiting profile/resume center and the user has not selected a specific job. Continue with the profile branch below and skip duplicate-application tracking, JD extraction, and resume selection.
- `job_application`: a specific job is in scope. Continue with the existing job inspection and tracking steps.

### Resume-profile branch

Open the profile/resume editor and read the current values before making changes. Compare normalized current values with confirmed profile data and prepare four groups: unchanged, change, add, and unresolved. Fill only `change` and `add`; leave already matching values untouched.

If the site has no dedicated research section, map confirmed research records into the project section. Preserve each record's title, role, dates, `resume_text`, technologies, and outcomes without recasting it as employment or claiming publication status. Disclose this cross-section mapping in the review. Pause only when the project section has a record limit, the mapping would displace existing content, or the target controls cannot represent the research facts without material loss. Preserve the site's existing photo or attachment unless the user explicitly authorizes replacement.

Before pausing for login, a conflict, mapping choice, sensitive-data authorization, or final save, preserve the active tab when supported and state whether the form is unsaved. After the user returns, verify the editor URL and one planned changed value. If unsaved state was lost, rebuild from the difference plan rather than rediscovering the entire form.

Treat `Save`, `Update profile`, or an equivalent action as the resume-profile boundary. Summarize all changes and any attached privacy-policy or legal-consent effect, obtain explicit confirmation, save once, and inspect the resulting profile for credible success evidence. Do not record a job application or infer permission to apply for a role.

### Job-application branch

Open the supplied URL and snapshot the page. Extract company, job title, stable job ID, location, category, recruitment type, full JD, requirements, and canonical job URL. Derive values only from visible page content, the URL, structured data, or the application flow.

If the page requires login, let the user handle QR login, CAPTCHA, SMS, MFA, or face verification, then take a new snapshot.

Check duplicates first by canonical URL, then by normalized company plus job ID. A previous `withdrawn` or `rejected` record is still a duplicate signal and requires user direction before a new application.

## 3. Plan the form

Snapshot the complete visible step. Build a working table with page label, section/context, input kind, canonical field, source path, confidence, and whether user confirmation is required.

When editing a form that already contains data, include its normalized current value in the working table and mark matching fields `unchanged`. Do not send input to unchanged fields. For repeated custom controls, verify the first interaction and then batch only equivalent deterministic operations; take a fresh snapshot after any rerender or add-row action.

Use `field-mapping.md` as semantic guidance. Labels, placeholders, help text, section headings, option values, and nearby controls all contribute to meaning. Repeated education, internship, project, and research blocks map to list entries only when the page and profile clearly correspond.

For `job_application`, select the resume with the helper. More matched keywords wins; ties follow rule order. A rule may name `cv` or `cv.pdf`. If no rule matches, use `general.pdf`. Do not continue when the chosen file is absent. For `resume_update`, retain the existing attachment unless replacement was explicitly requested and authorized.

## 4. Fill in stages

Fill confirmed deterministic fields, upload the selected resume or confirmed documents, then snapshot again. After every navigation, save, add-row operation, modal, or SPA rerender, discard stale element references and inspect the new state.

For experience-detail fields, use the selected record's `resume_text` first. Use structured fields for separate controls or the smallest necessary reduction under a disclosed field limit, and include any reduction in the final review. For other open questions, compare intent with `answers.yaml`. Reuse or lightly tailor an answer only when meaning is equivalent and the change adds no facts, preferences, metrics, employers, dates, or commitments.

Pause when a required value is missing, ambiguous, sensitive, or a personal/legal choice. Present the exact question, available options, and relevant stored answer without selecting on the user's behalf.

## 5. Review boundary

Complete all reversible preparation first. Before final submission, present the review summary required by `SKILL.md`, including unchecked declarations and validation warnings. Wait for explicit confirmation tied to this application and current prepared form. A general request to help apply does not authorize final submission.

After confirmation, click the final action once. Inspect the next snapshot for an application number, success message, application-center entry, or other credible evidence. If the outcome is unclear, report it and avoid retries that might duplicate the application.

## 6. Record result

For `job_application`, add a `prepared` record before the final boundary when useful and update it to `submitted` only on evidence. Do not add an application record for `resume_update`. Store concise notes, never passwords, verification codes, identity-document numbers, or full free-text answers.

Propose learnings after the run. Changes to profile, answers, or preferences need user confirmation when they encode facts or preferences.
