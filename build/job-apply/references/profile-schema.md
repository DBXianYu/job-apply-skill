# Profile schema and formats

`profile.yaml` stores confirmed candidate facts. `profile.example.yaml` demonstrates every supported section with fictional values. Never merge examples into the real profile or use them to fill a form.

## General formats

- Dates use `YYYY-MM-DD` when the day is known and `YYYY-MM` when only the month is known. YAML date-looking values should be quoted.
- Phone numbers use `country_code` and `number` as quoted strings so leading `+` or zeroes are preserved.
- Locations use `country_or_region`, `province`, and `city` when known. Do not repeat a combined display string as the canonical value.
- Repeated records are lists. Use one mapping per education, internship, project, research item, language, award, publication, patent, conference, scholarship, certificate, attachment, or employer-specific experience.
- Narrative responsibilities and outcomes are lists of complete statements. Preserve metrics exactly as supported by the source.
- Boolean values are `true` or `false`; unknown values are `null`. Never convert an unknown into `false`.
- Paths in `attachments` are relative to `${JOB_APPLY_HOME}` when possible.

## Sections

- `basic`: names, gender, birth date, contact, current location, native place, ethnicity, political status, marital status, photo path, and confirmed self-evaluation.
- `identification`: document type, number, and issuing country/region. These fields are sensitive and require confirmation before browser entry.
- `education`: institution, location, college, major, degree, study mode, dates, adviser, ranking, GPA, courses, and campus attributes.
- `internships`: company, department, role, location, dates, `resume_text`, responsibilities, and technologies. Use `employment_type` to distinguish internship and regular work.
- `projects` and `research`: title, role, dates, `resume_text`, descriptions, responsibilities, technologies, data sets, paper references, and measured outcomes.
- `skills`: category plus a list of exact skills.
- `languages`: language, proficiency, certificate, score, and score scale.
- `publications`, `patents`, `academic_conferences`, `competition_awards`, `scholarships`, and `certificates`: optional evidence records matching common recruiting modules.
- `attachments`: resume, transcript, portfolio, and other document paths.
- `company_specific`: employer-specific facts such as prior work or relatives. These are not general profile fields and always require confirmation before use.
- `job_preferences`: job types, directions, cities, location-change and position-adjustment choices, salary, travel, overtime, and overseas assignment. Treat every value as a user choice and reconfirm on the target form.

The example template contains at least one record for every repeated section. Copy only the structure of an example, then replace or clear every fictional value.

## Resume wording

`resume_text` is the normalized direct wording from the source resume. Preserve its sentences, figures, terminology, and bullet order; remove only PDF layout artifacts such as forced line wraps or split words. It is the default source for a site's narrative responsibility, achievement, project-detail, or research-detail field.

The structured `description`, `responsibilities`, `technologies`, and `outcomes` fields remain useful for semantic matching and forms that split one resume entry into several controls. They do not replace `resume_text`. If a site imposes a length limit, make the smallest necessary cut from `resume_text`, disclose that change in the review, and do not silently substitute a rewritten summary.
