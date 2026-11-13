# AI Learning Hub

A living knowledge base for **learning and applying AI** — fundamentals, LLM models, harness systems,
skills, MCP, connectors and automation — published as a searchable website.

**Site:** https://ngocanhk27.github.io/AI-skills-learning-decelopment/ *(after GitHub Pages is enabled — see below)*

## Areas

| Area | Folder | What goes there |
| --- | --- | --- |
| Fundamentals | [`docs/fundamentals`](docs/fundamentals/index.md) | How LLMs work, prompting, context engineering, agents, evaluation, safety |
| LLM Models | [`docs/models`](docs/models/index.md) | Model families, capabilities, pricing, limits, selection |
| Harness Systems | [`docs/harnesses`](docs/harnesses/index.md) | Agent runtimes: coding agents, IDE assistants, agent SDKs |
| Skills | [`docs/skills`](docs/skills/index.md) | Packaged, reusable agent know-how |
| MCP | [`docs/mcp`](docs/mcp/index.md) | Model Context Protocol: using, building and securing servers |
| Connectors | [`docs/connectors`](docs/connectors/index.md) | Ready-made integrations with docs, code and data services |
| Automation | [`docs/automation`](docs/automation/index.md) | Scheduled, triggered and CI-driven AI |
| Playbooks | [`docs/playbooks`](docs/playbooks/index.md) | End-to-end recipes combining all of the above |

Cross-cutting pages live in [`docs/start-here`](docs/start-here/index.md) (orientation, learning paths)
and [`docs/resources`](docs/resources/index.md) (catalog, tags, glossary, contributing guide, changelog).

## Add a topic

```bash
make new SECTION=mcp SLUG=building-a-server TITLE="Building an MCP server"
```

This creates `docs/mcp/building-a-server.md` from [`templates/topic.md`](templates/topic.md). The new
topic appears automatically in the navigation, the area's topic table, the catalog, the home-page
counts and the tags page. Full workflow: [How to add & update topics](docs/resources/contribute/index.md).

Every topic has front matter that drives the indexes:

```yaml
status: draft            # planned | draft | stable | needs-update
level: beginner          # beginner | intermediate | advanced
time: 30 min
last_reviewed: 2026-11-13  # topics older than 180 days get a "due for review" flag
tags: [mcp]
```

## Preview locally

```bash
make install   # once: creates .venv and installs requirements.txt
make serve     # http://127.0.0.1:8000 with live reload
make build     # strict build, same as CI
```

## Publish

`.github/workflows/deploy.yml` builds the site on every push and pull request (a strict build that
fails on broken links) and deploys `main` to GitHub Pages.

**One-time setup:** in the repository on GitHub, go to **Settings → Pages → Build and deployment**
and set **Source** to **GitHub Actions**.

## How it's built

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) on MkDocs 1.6 (pinned in
  [`requirements.txt`](requirements.txt))
- [`mkdocs-awesome-nav`](https://lukasgeiter.github.io/mkdocs-awesome-nav/) — navigation follows the
  folder structure; top-level order is set in [`docs/.nav.yml`](docs/.nav.yml)
- [`hooks/topic_index.py`](hooks/topic_index.py) — builds topic tables, the catalog, counts and the
  per-topic metadata line from front matter
- [`scripts/new_topic.py`](scripts/new_topic.py) — topic scaffolding

```
├── docs/                 # all site content (Markdown)
│   ├── index.md          # landing page
│   ├── start-here/       # orientation & learning paths
│   ├── fundamentals/ … playbooks/   # the eight learning areas
│   ├── resources/        # catalog, tags, glossary, contribute guide, changelog
│   └── assets/           # CSS, favicon
├── templates/topic.md    # template for every new topic
├── hooks/topic_index.py  # build-time indexes from front matter
├── scripts/new_topic.py  # `make new` scaffolder
├── mkdocs.yml            # site configuration
└── .github/              # deploy workflow, topic-request issue form
```
