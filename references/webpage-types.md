# Webpage Type Reference

## Classification Signals

`doc_code`:
- Code blocks, API names, config examples, headings such as Schema/JS/CSS/Usage.
- Primary value is exact technical content.

`article_image`:
- Long article body, editorial headings, inline media, captions, author/date.
- Primary value is readable text plus selected images.

`visual_page`:
- Hero sections, cards, product screenshots, portfolio pieces, visual CTAs.
- Primary value is page structure, messaging, and visual evidence.

## Extraction Strategy

For all types:
- Add `来源：...` near the top.
- Preserve heading hierarchy.
- Remove unrelated navigation, sidebars, cookie banners, floating ads, and duplicate text.

For code:
- Prefer DOM/code extraction over OCR.
- Infer language from heading first, then code syntax.
- Keep exact code block content where possible.

For images:
- Prefer real image source URL only if it can be fetched without browser cookies.
- If the source requires login or anti-hotlinking, use browser download/upload or screenshot.
- Keep alt/caption text near the image.
- Avoid copying decorative icons unless they are needed to understand the content.
- Public image path: write Markdown image syntax and verify Feishu renders it.
- Private image path: save the browser-visible image or screenshot locally, upload/insert it with Feishu media/file tooling, then verify the inserted image exists in the fetched document.
- If only a screenshot is possible, label it as a screenshot backup rather than a source image.

For visual pages:
- Capture a screenshot for design-critical sections.
- Convert the page to a Feishu-readable outline:
  - Hero
  - Sections in order
  - Key copy
  - Key visuals
  - CTA/action links

## Write Strategy

Existing empty Feishu doc:
- Use `overwrite`.

Existing non-empty Feishu doc:
- Read first.
- Append only new sections or replace a clearly matching section.
- Avoid deleting comments, images, or manual edits.

Logged-in source pages:
- The user must already be logged in.
- Stop for CAPTCHA, MFA, paywall, missing permission, or account-switch prompts.
- Do not inspect cookies, local storage, saved passwords, or browser session internals.

Wiki parent:
- List child nodes before creating.
- Match by exact title first; if exact title exists, update that child.
- Create missing pages under the parent.
- Update parent/index with links after creation.
