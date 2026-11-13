.PHONY: help install serve build new

PYTHON ?= python3
VENV   ?= .venv
BIN     = $(VENV)/bin

help:  ## Show available commands
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-8s %s\n", $$1, $$2}'

install:  ## Create a virtualenv and install the site toolchain
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt

serve:  ## Live-preview the site at http://127.0.0.1:8000
	$(BIN)/mkdocs serve

build:  ## Build the site into ./site and fail on broken links
	$(BIN)/mkdocs build --strict

new:  ## New topic: make new SECTION=mcp SLUG=building-a-server TITLE="Building an MCP server"
	$(PYTHON) scripts/new_topic.py "$(SECTION)" "$(SLUG)" "$(TITLE)"
