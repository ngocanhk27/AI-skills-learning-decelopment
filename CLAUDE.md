# AI Learning Hub — notes for AI assistants

This repo is a MkDocs (Material) knowledge base. Content is Markdown under `docs/`.

## Adding or editing topics

- Create topics with `python3 scripts/new_topic.py <area> <slug> "<Title>"` — never hand-build
  front matter from scratch. Areas: fundamentals, models, harnesses, skills, mcp, connectors,
  automation, playbooks.
- A page is a *topic* only if its front matter has `status`. Section `index.md` pages must not.
- Keep the template's section order: TL;DR, Why it matters, Core concepts, Hands-on, Practical
  applications, Pitfalls & gotchas, Checklist, Resources, Changelog.
- When editing a topic, bump `last_reviewed` and add a row to its Changelog table.
- Date any volatile fact (prices, limits, versions) inline, e.g. "(checked 2026-11)".
- Do not edit section topic tables or the catalog by hand — `hooks/topic_index.py` generates them
  from the markers in those pages.
- Structural changes (new area, new convention) go in `docs/resources/changelog.md`.

## Checking your work

```bash
make install && make build   # strict build; must pass with no warnings
```
