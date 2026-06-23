# Web To Feishu Doc Sync

> 把网页、文章、技术文档和视觉页面同步到飞书文档或知识库，并尽量保留结构、代码块、图片和来源链接。

<p align="center">
  <a href="https://github.com/mumushuo/web-to-feishu-doc-sync"><img src="https://img.shields.io/badge/Codex-Skill-blue?style=flat-square"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square"/></a>
  <a href="https://github.com/mumushuo/web-to-feishu-doc-sync/issues"><img src="https://img.shields.io/github/issues/mumushuo/web-to-feishu-doc-sync?style=flat-square"/></a>
</p>

<p align="center">
  <a href="https://github.com/mumushuo/web-to-feishu-doc-sync/stargazers"><img src="https://img.shields.io/github/stars/mumushuo/web-to-feishu-doc-sync?style=social"/></a>
  <a href="https://github.com/mumushuo/web-to-feishu-doc-sync/network/members"><img src="https://img.shields.io/github/forks/mumushuo/web-to-feishu-doc-sync?style=social"/></a>
</p>

> **早期版本说明：** 当前为 v0.1.0 早期版本，适合个人或小团队把公开网页、技术资料、产品页面整理到飞书文档中。建议先用少量页面验证格式效果，再批量同步。

---

## 这个项目解决什么问题

日常整理知识库时，经常会遇到这些重复工作：

- 网页内容复制到飞书后，标题层级、列表、表格容易乱。
- 技术文档里的代码块容易丢格式。
- 图片、截图、说明文字需要人工重新整理。
- 文章、教程、落地页需要保留来源链接，方便后续追溯。
- 已有飞书文档不能直接覆盖，否则容易破坏人工补充内容。

这个 Skill 的目标是把这些动作标准化：先识别网页类型，再提取有效内容，最后写入或补充到飞书文档/知识库，并进行结果校验。

---

## 功能特性

- **网页内容同步** — 支持网页 URL、当前浏览器页面、截图列表或选中文本。
- **飞书文档/知识库写入** — 可更新已有文档，也可在 Wiki 父节点下创建子文档。
- **自动分类页面类型** — 区分技术文档、图文文章、视觉落地页三类处理方式。
- **保留关键结构** — 尽量保留标题、段落、列表、表格、代码块和来源链接。
- **图片处理策略** — 公共图片使用链接；登录态图片优先下载/截图后再插入。
- **避免重复创建** — 写入前先读取目标文档，按标题去重。
- **结果校验** — 写入后检查来源链接、标题、关键代码、图片或 Wiki 子节点。
- **结构化 Markdown 生成** — 提供脚本把结构化 JSON 转成飞书友好的 Markdown。

---

## 合规与安全边界

**本项目只处理用户已经有权访问的内容。**

- 不绕过登录、验证码、MFA、权限控制或付费墙。
- 不读取浏览器 Cookie、本地存储、保存密码或会话文件。
- 登录态页面必须由用户自行完成登录和授权。
- 遇到验证码、MFA、缺权限、账号切换或付费墙时应停止。
- 不保留浏览器会话专属图片链接作为最终文档图片。
- 已有飞书文档非空时，优先追加或局部替换，避免直接整篇覆盖。

---

## 支持的页面类型

| 类型 | 适用场景 | 处理重点 |
|---|---|---|
| `doc_code` | API 文档、SDK 示例、技术教程 | 保留代码块、表格、参数说明和完整示例 |
| `article_image` | 图文文章、指南、说明文档 | 保留正文结构、关键图片、说明文字和来源 |
| `visual_page` | 官网落地页、产品页、作品集 | 保留模块顺序、核心文案、CTA 和关键视觉证据 |

详细规则见：[references/webpage-types.md](references/webpage-types.md)

---

## 快速开始

### 安装为 Codex Skill

下载入口：

- 完整仓库下载：[Download ZIP](https://github.com/mumushuo/web-to-feishu-doc-sync/archive/refs/heads/main.zip)
- 完整 Skill 文件：[SKILL.md](https://github.com/mumushuo/web-to-feishu-doc-sync/blob/main/SKILL.md)
- Skill 文件夹版本：[skill/SKILL.md](https://github.com/mumushuo/web-to-feishu-doc-sync/blob/main/skill/SKILL.md)

下载整个仓库，并放到你的 Codex skills 目录：

```bash
git clone https://github.com/mumushuo/web-to-feishu-doc-sync.git
mkdir -p ~/.codex/skills
cp -R web-to-feishu-doc-sync ~/.codex/skills/
```

完整 Skill 文件在仓库根目录：[SKILL.md](SKILL.md)。同时也保留了一份镜像文件：[skill/SKILL.md](skill/SKILL.md)，方便只查看 Skill 内容。

### 方式一：作为 Codex Skill 使用

```text
Use $web-to-feishu-doc-sync to sync this webpage into the target Feishu document.
Source: https://example.com/docs
Target: <飞书文档或 Wiki 地址>
```

### 方式二：使用结构化 Markdown 生成脚本

```bash
git clone https://github.com/mumushuo/web-to-feishu-doc-sync.git
cd web-to-feishu-doc-sync

python3 scripts/assemble_markdown.py examples/structured-extraction.json > output.md
```

输出的 `output.md` 可以作为飞书文档写入前的中间结果。

---

## 目录结构

```text
web-to-feishu-doc-sync/
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── LICENSE
├── skill/
│   └── SKILL.md              # Codex Skill 主说明
├── references/
│   └── webpage-types.md      # 页面类型判断与提取策略
├── scripts/
│   └── assemble_markdown.py  # 结构化 JSON 转 Markdown
├── agents/
│   └── openai.yaml           # Skill 展示信息
└── examples/
    └── structured-extraction.json
```

---

## 适合场景

- 把产品文档、API 文档整理到飞书知识库。
- 把公开教程、图文资料同步到团队文档。
- 把设计感较强的官网/落地页整理为可读的飞书大纲。
- 把多篇网页资料沉淀为统一结构的知识库页面。
- 给内部文档迁移流程增加“提取-写入-验证”的标准步骤。

---

## 不适合场景

- 绕过权限抓取非公开内容。
- 大规模爬取或批量复制受版权保护内容。
- 需要像素级还原网页视觉布局。
- 自动处理验证码、MFA、付费墙或账号权限问题。

---

## License

MIT © [mumushuo](https://github.com/mumushuo)
