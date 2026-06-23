#!/usr/bin/env python3
"""Assemble Feishu-friendly Markdown from structured webpage extraction JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def escape_text(text: str) -> str:
    """Escape Markdown-sensitive characters in normal text."""
    replacements = {
        "\\": "\\\\",
        "`": "\\`",
        "*": "\\*",
        "_": "\\_",
        "[": "\\[",
        "]": "\\]",
        "$": "\\$",
        "~": "\\~",
        "<": "\\<",
    }
    return "".join(replacements.get(char, char) for char in text)


def escape_table_cell(text: str) -> str:
    return escape_text(text).replace("|", "\\|").replace("\n", "<br>")


def escape_link_text(text: str) -> str:
    return escape_text(text).replace("\n", " ")


def fence_language(language: str | None) -> str:
    if not language:
        return ""
    language = language.strip().lower()
    aliases = {
        "js": "javascript",
        "ts": "typescript",
        "shell": "bash",
        "sh": "bash",
        "plain": "",
        "text": "",
    }
    return aliases.get(language, language)


def normalize_heading_level(value: Any) -> int:
    try:
        level = int(value)
    except (TypeError, ValueError):
        return 2
    return min(max(level, 2), 6)


def assemble(data: dict[str, Any]) -> str:
    title = str(data.get("title") or "Untitled").strip()
    url = str(data.get("url") or "").strip()
    blocks = data.get("blocks") or []

    lines: list[str] = [f"# {escape_text(title)}", ""]
    if url:
        lines.extend([f"来源：[{escape_link_text(title)}]({url})。", ""])

    for block in blocks:
        if not isinstance(block, dict):
            continue
        block_type = str(block.get("type") or block.get("kind") or "paragraph")
        text = str(block.get("text") or "").strip()
        if block_type == "heading":
            if not text:
                continue
            level = normalize_heading_level(block.get("level"))
            lines.extend([f"{'#' * level} {escape_text(text)}", ""])
        elif block_type == "code":
            if not text:
                continue
            language = fence_language(block.get("language") or block.get("lang"))
            lines.extend([f"```{language}", text, "```", ""])
        elif block_type == "image":
            src = str(block.get("src") or block.get("url") or "").strip()
            alt = str(block.get("alt") or block.get("caption") or "").strip()
            if src:
                lines.extend([f"![{escape_link_text(alt)}]({src})", ""])
            elif alt:
                lines.extend([f"[图片：{escape_text(alt)}]", ""])
        elif block_type in {"list", "ul"}:
            items = block.get("items") or []
            if isinstance(items, list):
                for item in items:
                    item_text = str(item).strip()
                    if item_text:
                        lines.append(f"- {escape_text(item_text)}")
                lines.append("")
        elif block_type == "ol":
            items = block.get("items") or []
            if isinstance(items, list):
                for index, item in enumerate(items, start=1):
                    item_text = str(item).strip()
                    if item_text:
                        lines.append(f"{index}. {escape_text(item_text)}")
                lines.append("")
        elif block_type == "blockquote":
            if text:
                for quote_line in text.splitlines():
                    lines.append(f"> {escape_text(quote_line)}")
                lines.append("")
        elif block_type == "table":
            headers = block.get("headers") or []
            rows = block.get("rows") or []
            if isinstance(headers, list) and headers:
                header_cells = [escape_table_cell(str(cell)) for cell in headers]
                lines.append("| " + " | ".join(header_cells) + " |")
                lines.append("|" + "|".join(["-" for _ in header_cells]) + "|")
                if isinstance(rows, list):
                    for row in rows:
                        if not isinstance(row, list):
                            continue
                        cells = [escape_table_cell(str(cell)) for cell in row]
                        if len(cells) < len(header_cells):
                            cells.extend([""] * (len(header_cells) - len(cells)))
                        lines.append("| " + " | ".join(cells[: len(header_cells)]) + " |")
                lines.append("")
        else:
            if text:
                lines.extend([escape_text(text), ""])

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: assemble_markdown.py input.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sys.stdout.write(assemble(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
