# Site adapters

Use this file only after the generic semantic workflow has failed or when a stable, verified special flow is known. Adapters describe durable behavior, not random class names, generated IDs, or one-session selectors.

## Adapter format

```markdown
## Site or ATS name
- Recognition: stable hostname or visible product identity.
- Special flow: durable ordering, save requirements, repeated-entry behavior, or upload behavior.
- Recovery: how to return to a stable state after rerender/navigation.
- Last verified: YYYY-MM-DD and the observed flow.
```

Before adding an adapter, retry from a fresh snapshot using label, role, surrounding text, section meaning, and visible state. A one-off click failure is not evidence for an adapter.

## Known adapters

## Bilibili campus recruiting

- Recognition: hostname `jobs.bilibili.com` with campus paths such as `/campus/me` and `/campus/resume`, plus visible identity `哔哩哔哩-招聘`.
- Scope: `/campus/me` is the reusable resume view and `/campus/resume` is its editor. Treat this as `resume_update` unless a specific job is also selected. Do not run duplicate-application tracking against the campus landing page or resume URL.
- Existing data: read current input and textarea values before editing, normalize whitespace and Chinese/ASCII punctuation only for comparison, and update differences only. Preserve the current photo and attachments unless replacement is explicitly authorized.
- Resume parsing: the editor may show an uploaded file and a `解析并覆盖` action. Do not activate parsing merely to speed up form filling; it may overwrite reviewed fields. Use it only when the user explicitly requests parsing and accepts the overwrite risk.
- Date controls: birth date and education/work/project periods use read-only Ant Design pickers. Open the intended field, choose the exact year/month or date in the visible picker, and verify the collapsed input value. After one picker has been verified, equivalent month selections may be batched with fresh locators. Do not call `fill()` on the collapsed read-only input.
- Repeated records: `添加实习/工作经历` and `添加项目经历` append new blocks and rerender the section. Re-resolve locators after each add-row operation. The site has no separate research section in the verified flow, so map confirmed research records into project experience and disclose that mapping in the review. Pause only if a record limit or destructive replacement would be required.
- Ordering: new records are appended. If chronological order matters and existing records would need deletion/recreation, explain that consequence and obtain direction before destructive rebuilding.
- Save boundary: `保存` updates the reusable recruiting profile and the page states that adding the resume represents agreement to its privacy policy. Summarize changes and obtain explicit save/privacy confirmation. Saving does not authorize a job application.
- Recovery: before any user pause, preserve or hand off the `/campus/resume` tab when supported and warn that the form is unsaved. On return, verify the URL and one representative planned value. If the tab is gone or the page returned to `/campus/me`, reopen the editor and reapply only the planned differences.
- Last verified: 2026-09-19 on the campus resume view and editor. The flow exposed Ant Design date/month pickers and append-only repeated experience sections.

## Xiaomi campus recruiting

- Recognition: hostname `xiaomi.jobs.f.mioffice.cn` and visible identity `小米校园招聘`.
- Scope: the resume editor uses searchable region trees and custom month-range pickers. Their expanded accessibility trees can contain every country or more than two centuries of years. When the stable attributes below are present, use targeted browser DOM locators and verify the selected value instead of capturing the full expanded accessibility tree.
- Region fields:
  - Open the field by its visible label or combobox role. For hometown, the stable selection control is `data-cy="hometown_cityInput"` and its search input is `input[id="hometownCityCode"]`.
  - Enter the complete, user-confirmed leaf value, such as an exact district or city. Wait for search results and click the unique matching leaf result. Do not choose an intermediate country, province, or city when the field requires a deeper leaf, and do not derive a district from an ID number or another field.
  - For the preferred-work-location tree, search through the textbox labelled `filter select`, then choose the matching leaf tree item rather than an expandable ancestor.
  - Verify the collapsed control's displayed selection or selected chip. Avoid `getAXState()` while the global region tree is expanded; use a full accessibility snapshot only if targeted search or semantic locators fail.
- Month-range fields:
  - Date wrappers expose stable names such as `data-cy="education[0].periodInput"`, with labels such as `data-cy="education[0].periodInputBegin"` and `data-cy="education[0].periodInputEnd"`. Open the intended label directly.
  - Within the visible month panel, select the year and month items whose `data-cy` values equal the requested literals, for example `2027` and `06`. After selecting a begin month, the control may automatically advance to the end picker; inspect the visible label before reopening it.
  - Verify the begin and end labels show the requested `YYYY-MM` values. Do not snapshot the expanded picker, which exposes its entire 1900-2134 year range.
- Recovery: if a targeted selector is absent, the result is non-unique, or the displayed value does not match, close the popup, take a fresh small DOM snapshot of the field, and retry once with semantic locators. Then fall back to the generic workflow. Clear an unconfirmed hometown selection through the field's visible clear action before asking the user.
- Last verified: 2026-09-17 on the campus resume editor at `/campus/resume/edit`; targeted search and `data-cy` month selection avoided the large region/year accessibility trees.
