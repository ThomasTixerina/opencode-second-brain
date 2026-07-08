# Super Second Brain — Architecture & Implementation

> A hybrid approach combining a traditional Obsidian vault structure with Karpathy's LLM Wiki pattern for AI-assisted knowledge management.

## Overview

The Super Second Brain vault is a portable knowledge management system designed for AI-assisted workflows. It supports multiple AI agents (OpenCode, Gemini CLI, Claude Code) and integrates with both manual workflows (via Obsidian) and automated pipelines (via Python scripts and Windows Task Scheduler).

## Key Design Decisions

### 1. No n8n
Unlike prior projects that relied on n8n for orchestration, the Super Second Brain uses pure Python scripts running on a polling-based watcher (`wiki-watch.py`). This eliminates the need for an entire automation server while still providing automated lint checks, compaction, and new-source detection.

### 2. Human-in-the-loop ingestion
The watcher (`wiki-watch.py`) detects new files in `raw/` and notifies the user, but never auto-ingests. The human (or their AI agent) decides when and how to run `ingest.py commit`. This matches Karpathy's philosophy: the LLM does the synthesis, but a human (or agent) reviews it before committing.

### 3. Structured JSON interface
The `ingest.py draft` command produces a JSON template that an LLM fills with entities, concepts, and synthesis. The `ingest.py commit` command reads JSON from stdin and writes markdown files. This decouples the LLM reasoning from file I/O — any AI agent can pipe structured output into the pipeline.

### 4. Markdown + Dataview
The wiki is plain markdown with YAML frontmatter. The `_index.md` files use Obsidian Dataview queries to auto-generate catalogs, eliminating manual index maintenance.

## Scripts

| Script | Purpose |
|--------|---------|
| `ingest.py` | Pipeline: raw/ → wiki/ with commands list, draft, commit, status, log |
| `lint-wiki.py` | Health check: orphans, broken wikilinks, stale sources; --report flag |
| `wiki-watch.py` | Background watcher (60s polling); notifies on new sources + due lint |
| `setup-automation.ps1` | Task Scheduler registration for lint (24h), compact (7d), watcher (logon) |
| `sync-memory.py` | Bidirectional sync between OpenCode JSONL memory and vault |

## Architecture Flow

```
Source (web/article/chat)
       │
       ▼
  raw/<file>.md           ← Immutable, never modified
       │
       ▼
  ingest.py draft         ← LLM fills JSON template
       │
       ▼
  ingest.py commit        ← Writes: sources/<slug>.md
                                   entities/<entity>.md
                                   concepts/<concept>.md
       │                                   │
       ▼                                   ▼
  log.md                           _index.md (Dataview)
```

## Source of Inspiration

This project is inspired by Andrej Karpathy's concept of an "LLM Wiki" — a knowledge base where LLMs do the writing, but humans (or agents acting on their behalf) control what gets written. The vault structure builds on the existing second-brain conventions that were already in place.
