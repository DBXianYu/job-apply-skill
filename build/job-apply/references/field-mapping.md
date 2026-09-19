# Canonical field mapping

Map by meaning and context, not exact string equality. Normalize case, whitespace, punctuation, full-width characters, and common Chinese/English variants. Use the page section, help text, option set, input type, and neighboring labels to disambiguate.

## Basic identity and contact

| Canonical path | Common meanings and aliases | Notes |
| --- | --- | --- |
| `basic.name_zh` | 姓名, 中文姓名, 真实姓名, candidate name/full name in a Chinese-name context | Do not split or transliterate automatically. |
| `basic.name_en` | 英文姓名, English name, name in English | Use only an explicitly stored value. |
| `basic.gender` | 性别, gender, sex | Sensitive; fill only when explicitly present. |
| `basic.birth_date` | 出生日期, 生日, date of birth, DOB | Adapt display format only. |
| `basic.phone.number` | 手机, 手机号码, 联系电话, mobile, phone | Pair with `basic.phone.country_code` when separated. |
| `basic.email` | 邮箱, 电子邮箱, email, e-mail | Use the exact stored value. |
| `basic.current_location.city` | 现居城市, 当前城市, 居住地, current city | Distinguish from preferred work city. |
| `basic.native_place` | 籍贯, native place | Do not confuse with nationality/citizenship. |
| `basic.ethnicity` | 民族, ethnicity | Sensitive; use only confirmed data. |
| `basic.political_status` | 政治面貌, political status | Sensitive; always confirm before entry. |
| `basic.marital_status` | 婚姻状况, marital status | Sensitive; always confirm before entry. |
| `basic.self_evaluation` | 自我评价, 个人评价, personal summary | Preserve confirmed claims and wording. |
| `identification.document_type` | 证件类型, ID type, credential type | Sensitive; always confirm before entry. |
| `identification.document_number` | 证件号码, 身份证号, credential number | Sensitive; never expose in review summaries. |
| `identification.issuing_country_or_region` | 证件签发国家/地区 | Do not infer citizenship from this field. |

Political status, marital/fertility status, health, disability, ethnicity, nationality, ID numbers, household registration, and work authorization are never inferred.

## Education

| Canonical path | Common meanings and aliases |
| --- | --- |
| `education[].school` | 学校, 毕业院校, 就读院校, university, school |
| `education[].college` | 学院, 院系, department, faculty, college |
| `education[].major` | 专业, 专业名称, major, field of study |
| `education[].degree` | 学历, 最高学历, 学位, degree, education level |
| `education[].start_date` | 入学时间, 教育开始时间, start date |
| `education[].end_date` | 毕业时间, 预计毕业时间, end/graduation date |
| `education[].gpa` | GPA, 平均绩点, 绩点 |
| `education[].gpa_scale` | GPA 满分, 绩点总分, scale |
| `education[].rank` | 排名, 专业排名, 班级排名, rank |
| `education[].student_id` | 学号, student ID |
| `education[].country_or_region` | 毕业院校所在国家/地区, school country/region |
| `education[].study_mode` | 学制, 学习形式, full-time/part-time |
| `education[].research_direction` | 研究方向, research direction |
| `education[].advisor_name` | 导师姓名, supervisor/adviser |
| `education[].is_national_key_laboratory` | 是否国家重点实验室 |
| `education[].is_student_cadre` | 是否学生干部 |
| `education[].courses` | 主修课程, relevant coursework |

Use the relevant education entry based on level, dates, and form section. “Highest degree” usually selects one record; a history repeater may require multiple records. Do not infer degree equivalence or convert GPA/rank without confirmation.

## Experience and qualifications

| Canonical path | Common meanings and aliases | Mapping rule |
| --- | --- | --- |
| `internships[]` | 实习经历, internship, student work experience | Use confirmed entries only. |
| `projects[]` | 项目经历, project experience, portfolio project | Select relevant entries without changing facts. |
| `research[]` | 科研经历, research experience, publication/research project | Prefer a dedicated research section. If none exists, map confirmed research records into project experience while preserving title, role, dates, `resume_text`, technologies, and outcomes; disclose the mapping and do not invent publication status. |
| `awards[]` | 奖项, 荣誉, scholarship, award | Preserve title, issuer, level, and date. |
| `skills[]` | 技术栈, 技能, programming language, tools | Choose stored relevant skills. |
| `languages[]` | 语言情况, 语言名称, 熟练程度, 语言证书及成绩 | Keep certificate score as a quoted string. |
| `publications[]` | 发表论文, publication | Preserve publication status and author order. |
| `patents[]` | 发明专利, patent | Preserve application/grant status. |
| `academic_conferences[]` | 参加学术会议, conference | Store role and confirmed details. |
| `competition_awards[]` | 竞赛奖项, competition award | Distinguish from scholarship. |
| `scholarships[]` | 奖学金, scholarship | Preserve level and date. |
| `certificates[]` | 资格证书, certification | General certificates outside language records. |
| `company_specific.<company>` | 曾在该公司任职, 亲属任职, employer-specific history | Always confirm before use. |
| `links.github` | GitHub, 代码仓库, repository profile | Use exact URL. |
| `links.homepage` | 个人主页, portfolio, homepage | Use exact URL. |

Narrative text may format structured facts but must not add claims, numbers, dates, technologies, or responsibilities absent from the data.

For a free-text responsibility, achievement, project-detail, or research-detail box, map first to `internships[].resume_text`, `projects[].resume_text`, or `research[].resume_text`. Use structured subfields when the page provides separate controls or when a disclosed character limit requires a shorter extract.

## Preferences and uploads

| Canonical source | Common meanings and aliases | Rule |
| --- | --- | --- |
| `job_preferences.job_types` | 求职类型, 招聘类型, campus/internship/experienced | Match confirmed preferences and role. |
| `job_preferences.directions` | 求职方向, 意向岗位, function, track | Do not choose a different track. |
| `job_preferences.preferred_cities` | 意向城市, 工作地点志愿, preferred location | Ask before ranking or choosing. |
| selected resume | 简历, 附件简历, resume, CV | Run `profile.py choose-resume`; verify uploaded name. |
| confirmed document | 成绩单, transcript, supporting document | Upload only the matching file from `documents/`. |
| `answers.objective.self_introduction` | 自我介绍, personal statement | Light tailoring may not add facts. |
| `answers.objective.strengths` or profile facts | 自我评价, strengths, why you | Ask if no suitable answer exists. |

## Always-confirm topics

Do not decide relocation, position adjustment, city ranking, salary, travel, overtime, overseas assignment, non-compete status, political status, marital/fertility information, health declarations, identity attestations, truthfulness declarations, privacy terms, background checks, or employment agreements. Show the exact prompt and choices.

Low confidence, conflicting sources, changed option meanings, or a required field with no confirmed source always resolves to a pause.
