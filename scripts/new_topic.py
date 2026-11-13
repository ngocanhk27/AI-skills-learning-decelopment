#!/usr/bin/env python3
"""Scaffold a new topic page from templates/topic.md.

Usage:
    python scripts/new_topic.py <section> <slug> "<Title>"

Example:
    python scripts/new_topic.py mcp building-a-server "Building an MCP server"

Creates docs/<section>/<slug>.md. It then shows up automatically in the
navigation, the section's topic table and the catalog.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATE = ROOT / "templates" / "topic.md"
NON_TOPIC_SECTIONS = {"assets", "resources", "start-here"}


def sections() -> list[str]:
    return sorted(
        p.name for p in DOCS.iterdir()
        if p.is_dir() and (p / "index.md").exists() and p.name not in NON_TOPIC_SECTIONS
    )


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        print("Sections:", ", ".join(sections()))
        return 1
    section, slug, title = argv[1], argv[2], argv[3]
    if section not in sections():
        print(f"Unknown section '{section}'. Choose one of: {', '.join(sections())}")
        return 1
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*", slug):
        print("Slug must be lowercase words joined by hyphens, e.g. building-a-server")
        return 1

    target = DOCS / section / f"{slug}.md"
    if target.exists():
        print(f"{target.relative_to(ROOT)} already exists")
        return 1

    # Nested slugs (e.g. claude-code/hooks) sit one folder deeper.
    depth = slug.count("/")
    content = (
        TEMPLATE.read_text()
        .replace("{{TITLE}}", title.replace('"', '\\"'))
        .replace("{{SECTION}}", section)
        .replace("{{DATE}}", dt.date.today().isoformat())
        .replace("../resources/", "../" * (depth + 1) + "resources/")
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print(f"Created {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
