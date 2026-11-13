"""MkDocs hook that turns topic front matter into live indexes.

Any Markdown page with a ``status`` field in its front matter is a *topic*.
This hook reads every topic's front matter at build time and expands these
markers wherever they appear in a page:

    <!-- topics -->            table of topics in the current section folder
    <!-- topic-catalog -->     every topic, grouped by section
    <!-- recent-topics -->     the most recently reviewed topics
    <!-- topic-count:<dir> --> number of topics in a section folder

It also adds a small metadata line (level, status, last reviewed, time
estimate) under the H1 of each topic page.

The result: drop a new topic file into a section folder and it shows up in the
navigation, the section table, the catalog and the counts — no index to edit.
"""

from __future__ import annotations

import datetime as dt
import posixpath
import re

from mkdocs.utils.meta import get_data

STATUS = {
    "planned": ":material-calendar-blank-outline: Planned",
    "draft": ":material-pencil-outline: Draft",
    "stable": ":material-check-decagram: Stable",
    "needs-update": ":material-update: Needs update",
}
LEVEL = {
    "beginner": ":material-signal-cellular-1: Beginner",
    "intermediate": ":material-signal-cellular-2: Intermediate",
    "advanced": ":material-signal-cellular-3: Advanced",
}
REVIEW_EVERY_DAYS = 180  # topics older than this are flagged as stale

_topics: list[dict] = []
_section_titles: dict[str, str] = {}


def _as_date(value) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def _title(meta: dict, markdown: str, fallback: str) -> str:
    if meta.get("title"):
        return str(meta["title"])
    match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def on_files(files, config):
    _topics.clear()
    _section_titles.clear()
    for file in files.documentation_pages():
        markdown, meta = get_data(file.content_string)
        src = file.src_uri
        section = src.split("/", 1)[0] if "/" in src else ""
        if posixpath.basename(src) == "index.md" and section and src.count("/") == 1:
            _section_titles[section] = _title(meta, markdown, section.title())
        if "status" not in meta:
            continue
        _topics.append(
            {
                "src": src,
                "dir": posixpath.dirname(src),
                "section": section,
                "title": _title(meta, markdown, posixpath.basename(src)[:-3]),
                "description": str(meta.get("description", "")).strip(),
                "status": str(meta.get("status", "")).strip().lower(),
                "level": str(meta.get("level", "")).strip().lower(),
                "reviewed": _as_date(meta.get("last_reviewed")),
                "time": str(meta.get("time", "")).strip(),
            }
        )
    _topics.sort(key=lambda t: (t["section"], t["title"].lower()))
    return files


def _link(topic: dict, from_src: str) -> str:
    rel = posixpath.relpath(topic["src"], posixpath.dirname(from_src) or ".")
    return f"[{topic['title']}]({rel})"


def _reviewed(topic: dict) -> str:
    date = topic["reviewed"]
    if not date:
        return "—"
    stale = (dt.date.today() - date).days > REVIEW_EVERY_DAYS
    return f"{date.isoformat()} :material-alert:{{ title='Due for review' }}" if stale else date.isoformat()


def _table(topics: list[dict], from_src: str, empty: str) -> str:
    if not topics:
        return f'!!! note "No topics yet"\n    {empty}\n'
    rows = [
        "| Topic | Summary | Level | Status | Last reviewed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for t in topics:
        rows.append(
            "| {link} | {desc} | {level} | {status} | {reviewed} |".format(
                link=_link(t, from_src),
                desc=t["description"].replace("|", "\\|") or "—",
                level=LEVEL.get(t["level"], t["level"] or "—"),
                status=STATUS.get(t["status"], t["status"]),
                reviewed=_reviewed(t),
            )
        )
    return "\n".join(rows) + "\n"


def _meta_line(topic: dict) -> str:
    parts = []
    if topic["level"]:
        parts.append(LEVEL.get(topic["level"], topic["level"]))
    parts.append(STATUS.get(topic["status"], topic["status"]))
    if topic["time"]:
        parts.append(f":material-clock-outline: {topic['time']}")
    if topic["reviewed"]:
        parts.append(f":material-calendar-check: Reviewed {_reviewed(topic)}")
    return '<p class="topic-meta" markdown>' + " &nbsp;·&nbsp; ".join(parts) + "</p>"


def on_page_markdown(markdown, page, config, files):
    src = page.file.src_uri
    here = posixpath.dirname(src)
    empty = (
        "Topics will appear here automatically. Create one with "
        "`make new SECTION=<folder> SLUG=<name> TITLE=\"...\"` "
        "or copy `templates/topic.md` into this folder."
    )

    if "<!-- topics -->" in markdown:
        own = [t for t in _topics if t["dir"] == here or t["dir"].startswith(here + "/")]
        markdown = markdown.replace("<!-- topics -->", _table(own, src, empty))

    if "<!-- topic-catalog -->" in markdown:
        blocks = []
        for section in sorted({t["section"] for t in _topics}):
            group = [t for t in _topics if t["section"] == section]
            blocks.append(f"### {_section_titles.get(section, section.title())}\n\n" + _table(group, src, empty))
        markdown = markdown.replace(
            "<!-- topic-catalog -->", "\n".join(blocks) if blocks else _table([], src, empty)
        )

    if "<!-- recent-topics -->" in markdown:
        dated = sorted((t for t in _topics if t["reviewed"]), key=lambda t: t["reviewed"], reverse=True)[:6]
        if dated:
            lines = [f"- {_link(t, src)} — {t['reviewed'].isoformat()}" for t in dated]
            recent = "\n".join(lines) + "\n"
        else:
            recent = "_Nothing reviewed yet — your first topics will show up here._\n"
        markdown = markdown.replace("<!-- recent-topics -->", recent)

    def count(match: re.Match) -> str:
        n = sum(1 for t in _topics if t["section"] == match.group(1))
        return f"{n} topic" + ("" if n == 1 else "s")

    markdown = re.sub(r"<!-- topic-count:([\w-]+) -->", count, markdown)

    topic = next((t for t in _topics if t["src"] == src), None)
    if topic:
        markdown = re.sub(r"^(#\s+.+)$", lambda m: m.group(1) + "\n\n" + _meta_line(topic), markdown, count=1, flags=re.M)

    return markdown
