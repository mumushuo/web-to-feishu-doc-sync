---
name: web-to-feishu-doc-sync
description: Sync or supplement content from arbitrary webpages into Feishu/Lark Docs or Wiki documents. Use when the user asks to copy a webpage, article, documentation page, image-heavy page, visual landing page, or a list of webpage sections into a Feishu document or knowledge-base node while preserving structure, key images, code blocks, source URLs, and existing Feishu content.
---

# Web To Feishu Doc Sync

## Goal

Copy useful content from a webpage into Feishu/Lark Docs or Wiki in a reusable, verified way.

Default behavior: read the target Feishu document or Wiki node first, deduplicate by title, then update in place or create missing child pages under the requested parent.

## Inputs

Accept any of these:

- A URL.
- The currently open browser page.
- A screenshot or selected text containing webpage titles.
- A Feishu document/wiki target URL, token, or a known knowledge-base parent.

If the target is ambiguous and cannot be inferred from context, ask one concise question before writing.

## Workflow

1. Identify source pages.
   - Use this skill only for personal learning, testing, internal knowledge management, or content the user is legally allowed to access and reuse.
   - Do not use it for illegal profit, copyright infringement, unauthorized scraping, redistribution of protected content, privacy violations, account abuse, or other activity that infringes third-party rights.
   - Prefer browser/Chrome for pages that require login, dynamic rendering, or sidebar navigation.
   - Prefer direct URL fetch only when the page is public and static.
   - For a screenshot list, use the visible order as the sync order and locate each source page through the site's own navigation or current browser state.
   - For login-gated pages, use only already-visible browser state. The user must complete login, CAPTCHA, MFA, permission approval, or paywall steps.
   - Do not inspect cookies, local storage, saved passwords, or session stores.

2. Identify target.
   - For Feishu/Lark, prefer `lark-cli` or an available Feishu/Lark connector.
   - For Wiki targets, list child nodes first and match existing titles.
   - If a same-title target exists, read it before writing.
   - If no same-title target exists under a clear parent, create a child document there.

3. Classify webpage type.
   - `doc_code`: documentation, API docs, examples, tutorials with code.
   - `article_image`: article or guide with important inline images.
   - `visual_page`: marketing/product/portfolio page where layout and visuals matter.

4. Extract content according to type.
   - Always preserve title, source URL, meaningful headings, paragraphs, lists, tables, and code blocks.
   - Preserve code block boundaries and languages when possible: `json`, `javascript`, `typescript`, `css`, `html`, `bash`, `plain text`.
   - For image-heavy pages, extract important images with captions/alt text when available.
   - For visual pages, extract module order and key copy; use screenshots as backup for visuals that cannot be represented cleanly.
   - Remove unrelated navigation, sidebars, cookie banners, ads, duplicated hidden text, and purely decorative icons.

5. Write to Feishu.
   - Empty existing document: `overwrite` is acceptable.
   - Existing non-empty document: prefer append or targeted replacement; avoid full overwrite unless the user asks for a rewrite.
   - New child page: create with the extracted title and content.
   - Parent/index page: update links and scope notes after child pages are created.

6. Verify.
   - Fetch written document(s) through `lark-cli docs +fetch`.
   - Confirm source URL exists.
   - Confirm expected titles/sections exist.
   - For code docs, confirm key code tokens exist.
   - For image docs, confirm image blocks or uploaded images exist.
   - For Wiki directories, list children and confirm count/title set.

## Type-Specific Rules

### doc_code

Use for developer docs, code examples, API docs, and internal documentation pages.

- Keep code blocks complete, including long blocks outside the visible viewport.
- Label code languages when inferable from nearby headings or code content.
- Keep short explanatory prose before each code block.
- If extracted code is very long, write the whole block; do not summarize unless the user asks.

### article_image

Use for articles, guides, notes, and pages where text and images both matter.

- Preserve article title, author/date if relevant, headings, paragraphs, lists, quotes, and important images.
- Do not rely on raw image URLs if they require login, cookies, or anti-hotlinking.
- If an image URL is public, insert it into Feishu as an image.
- If an image is not public, download it from the authenticated browser or capture a screenshot, then upload/insert that image into Feishu.
- If image extraction is blocked, include a screenshot and clearly note which image could not be extracted directly.
- Preserve image order relative to the surrounding text.

### visual_page

Use for landing pages, product pages, portfolios, and highly styled pages.

- Do not try to recreate pixel-perfect layout in Feishu.
- Preserve section order, major headings, important body copy, CTAs, and key visuals.
- Use screenshots for design-heavy sections where text extraction loses meaning.
- Prefer a structured Feishu document over a raw screenshot-only archive unless the user asks for screenshots only.

## Feishu/Lark Command Notes

- Read command-specific docs when `lark-cli docs +create` or `docs +update` asks for them.
- For Markdown writes, use `--doc-format markdown --content -` and feed stdin to avoid shell escaping problems.
- For Wiki child docs, create with `--parent-token <wiki_node_token>`.
- After creating child docs, list Wiki children to obtain stable Wiki URLs.
- For public images, Markdown image syntax is acceptable: `![alt](https://...)`.
- For private/login-gated images, use Feishu media/file insertion after download or screenshot; do not leave browser-session-only image URLs in the final doc.

## Helper Script

Use `scripts/assemble_markdown.py` when you already have structured extraction JSON and want deterministic Markdown assembly.

Input JSON shape:

```json
{
  "title": "Page title",
  "url": "https://example.com/page",
  "blocks": [
    {"type": "paragraph", "text": "Intro"},
    {"type": "heading", "level": 2, "text": "Schema"},
    {"type": "code", "language": "json", "text": "{}"},
    {"type": "image", "src": "https://example.com/a.png", "alt": "Preview"},
    {"type": "table", "headers": ["Name", "Value"], "rows": [["A", "1"]]},
    {"type": "blockquote", "text": "Quoted text"}
  ]
}
```

Run:

```bash
python3 scripts/assemble_markdown.py input.json > output.md
```

## References

- Read `references/webpage-types.md` when deciding how to handle image-heavy or visual pages.
