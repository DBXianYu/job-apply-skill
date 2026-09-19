# Job Apply Skill

一个面向 Codex 的求职申请技能：从招聘页面读取职位信息，基于已确认的候选人资料填写申请表，选择匹配的简历，并在最终提交前停下来供用户复核。

它强调安全和可追溯性：不猜测个人信息、不绕过验证码、不批量投递，并将每次申请记录到本地 CSV。

## 功能

- 读取职位描述并提取公司、职位、地点、职位 ID 等信息
- 将表单字段语义映射到结构化候选人资料
- 按职位关键词选择对应简历
- 检查重复申请并跟踪申请状态
- 在验证码、身份验证、法律声明和最终提交等关键节点暂停
- 将技能代码与个人资料分开存放，避免敏感信息进入仓库

## 仓库结构

```text
build/job-apply/
├── SKILL.md                 # 技能入口与安全规则
├── agents/openai.yaml       # Codex 展示信息与默认提示
├── references/              # 工作流、字段映射、数据结构和站点适配说明
└── scripts/                 # 配置读取、校验、简历选择和申请跟踪工具

data/
├── profile.yaml             # 空白候选人资料模板
├── profile.example.yaml     # 完整的虚构示例
├── answers.yaml             # 常见开放题答案模板
├── preferences.yaml         # 简历关键词匹配规则
└── applications.csv         # 空白申请记录表
```

`data/` 中的文件是初始化模板。真实个人资料应存放在项目目录之外，默认位置为 `~/.codex/job-apply`，也可以通过 `JOB_APPLY_HOME` 指定其他目录。

## 安装

### 1. 安装依赖

脚本需要 Python 3.10 或更高版本以及 PyYAML：

```bash
python -m pip install PyYAML
```

### 2. 安装技能

将 `build/job-apply` 复制到 Codex 的技能目录：

```text
~/.codex/skills/job-apply
```

### 3. 初始化个人数据目录

创建 `~/.codex/job-apply`，将 `data/` 中的模板复制进去，并创建两个仅存放在本地的目录：

```text
~/.codex/job-apply/
├── profile.yaml
├── profile.example.yaml
├── answers.yaml
├── preferences.yaml
├── applications.csv
├── resumes/
└── documents/
```

然后只在该目录的 `profile.yaml` 和 `answers.yaml` 中填写真实信息。不要把个人资料、简历或证明材料复制到技能目录或提交到 Git。

## 配置与验证

从已安装的技能目录运行：

```bash
python scripts/profile.py home
python scripts/validate_profile.py
```

校验器会检查 YAML 结构、必需目录和示例文件。未填写的候选人字段会显示在 `NEEDS_USER_INPUT` 下，但不会被自动推断。

如需使用自定义数据目录：

```bash
export JOB_APPLY_HOME=/path/to/job-apply-data
```

PowerShell：

```powershell
$env:JOB_APPLY_HOME = "C:\path\to\job-apply-data"
```

## 使用

在 Codex 中提供一个招聘职位链接，并调用技能：

```text
使用 $job-apply 帮我准备这个职位的申请：<job-url>
```

技能会读取职位信息、检查重复记录、填写可确定的字段并选择简历。到达最终提交按钮前，它会汇总已填写内容、附件、未解决字段和声明，并等待明确确认。

### 常用辅助命令

读取一个候选人字段：

```bash
python scripts/profile.py get education[0].school
```

根据职位描述选择简历：

```bash
python scripts/profile.py choose-resume --jd-file jd.txt
```

检查是否重复申请：

```bash
python scripts/tracker.py check "https://example.com/jobs/123"
```

查看申请记录：

```bash
python scripts/tracker.py list
python scripts/tracker.py list --status interview
```

## 安全边界

- 一次只处理一个职位，不用于爬取或批量投递
- 不绕过验证码、短信、MFA、扫码登录或人脸验证
- 不根据常识补全未知个人信息
- 涉及敏感属性、法律声明、隐私授权或不确定事实时暂停
- 未得到用户对已准备表单的明确确认，不执行最终提交
- 只有页面提供可信成功证据后，才将状态记录为 `submitted`

更完整的行为约束请参阅 [`build/job-apply/SKILL.md`](build/job-apply/SKILL.md)。

## 许可证

本项目采用 [MIT License](LICENSE)。
