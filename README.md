# Web To Feishu Doc Sync

Sync useful content from webpages into Feishu/Lark Docs or Wiki while preserving structure, source URLs, code blocks, tables, and important images.

[中文介绍](README.zh-CN.md)

This repository contains a reusable Agent Skill plus a small Markdown assembly helper. It is designed for documentation migration, article archiving, product page summarization, and knowledge-base maintenance.

## What It Does

- Reads a source webpage, browser page, screenshot list, or selected page sections.
- Classifies the page as technical documentation, image-rich article, or visual landing page.
- Extracts useful content while removing navigation, ads, duplicate hidden text, and decorative noise.
- Writes or updates Feishu/Lark Docs and Wiki pages.
- Verifies the written result by checking source URLs, section titles, code tokens, image blocks, or Wiki child nodes.

## Core Principles

1. Read the target document before writing.
2. Deduplicate by title before creating new child pages.
3. Preserve source URLs near the top of the synced document.
4. Keep code blocks complete and language-labelled when possible.
5. Do not inspect cookies, local storage, saved passwords, or browser session stores.
6. Stop for CAPTCHA, MFA, paywalls, missing permissions, or account-switch prompts.
7. Prefer targeted updates over full overwrites when the target document already has content.

## Repository Structure

```text
web-to-feishu-doc-sync/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── skill/
│   └── SKILL.md
├── references/
│   └── webpage-types.md
├── scripts/
│   └── assemble_markdown.py
├── agents/
│   └── openai.yaml
└── examples/
    └── structured-extraction.json
```

## Quick Start

### Download and Installation

See the Chinese guide for download links and installation steps for common Agent environments: [README.zh-CN.md#快速开始](README.zh-CN.md#快速开始).

### Use the Skill

Use the skill when you need to copy a webpage into Feishu/Lark:

```text
Use $web-to-feishu-doc-sync to sync this webpage into the target Feishu document.
Source: https://example.com/docs
Target: <Feishu document or Wiki URL>
```

For structured extraction JSON, generate Feishu-friendly Markdown:

```bash
python3 scripts/assemble_markdown.py examples/structured-extraction.json > output.md
```

## Supported Page Types

| Type | Best For | Handling |
|---|---|---|
| `doc_code` | API docs, tutorials, SDK examples | Preserve headings, code blocks, tables, and exact examples |
| `article_image` | Guides, articles, image-heavy notes | Preserve article flow and important images |
| `visual_page` | Landing pages, product pages, portfolios | Preserve section order, key copy, CTAs, and screenshots when useful |

See [references/webpage-types.md](references/webpage-types.md) for classification and extraction details.

## Safety Boundary

This project does not bypass login, CAPTCHA, MFA, permission controls, anti-hotlinking, or paywalls. For login-gated pages, it only uses already-visible browser content and asks the user to complete any required access steps manually.

## License

MIT © mumushuo
