"""
Second Brain Bridge — Gemini ↔ Obsidian Vault

CLI tool for reading, writing, searching, and organizing the Obsidian vault.
Designed to be used by Gemini CLI, OpenCode CLI, or directly from the terminal.

Usage:
    python bridge.py read <path>              Read a note from the vault
    python bridge.py write <path>             Write content to a note (from stdin)
    python bridge.py search <query>           Search vault content
    python bridge.py daily                    Create today's daily note
    python bridge.py list [dir]               List notes in a directory
    python bridge.py graph                    Show the vault's link graph (basic)
    python bridge.py template <name>          Generate a note from a template
"""

import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "second-brain"

TEMPLATES = {
    "memory": """---
tags: [memory]
date: {date}
ai-generated: true
---

# {title}

## Contexto

{content}

## Enlaces
- [[memory/_index|Todas las memorias]]
""",
    "reference": """---
tags: [reference]
source: {source}
date: {date}
ai-generated: true
---

# {title}

## Resumen

{content}

## Enlaces
- [[references/_index|Todas las referencias]]
""",
    "daily": """---
date: {date}
tags: [daily]
---

# {date}

## 🎯 Enfoque del día

- 

## ✅ Hecho

- 

## 🧠 Aprendizajes

- 

## 🔗 Enlaces
- [[_index|Volver al MOC]]
""",
}


def ensure_vault():
    if not VAULT.exists():
        print(f"Error: Vault not found at {VAULT}", file=sys.stderr)
        sys.exit(1)


def cmd_read(args):
    ensure_vault()
    path = VAULT / args.path
    if not path.exists():
        # Try with .md extension
        path = path.with_suffix(".md")
    if not path.exists():
        print(f"Note not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    print(path.read_text(encoding="utf-8"))


def cmd_write(args):
    ensure_vault()
    path = VAULT / args.path
    if not path.suffix:
        path = path.with_suffix(".md")
    path.parent.mkdir(parents=True, exist_ok=True)
    content = sys.stdin.read()
    path.write_text(content, encoding="utf-8")
    print(f"Written: {path.relative_to(VAULT)}")


def cmd_search(args):
    ensure_vault()
    query = args.query.lower()
    results = []
    for md_file in VAULT.rglob("*.md"):
        if ".obsidian" in md_file.parts or "scripts" in md_file.parts:
            continue
        rel = md_file.relative_to(VAULT)
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        if query in content.lower():
            # Find the matching line
            for i, line in enumerate(content.split("\n"), 1):
                if query in line.lower():
                    results.append((rel, i, line.strip()[:120]))
                    break
            else:
                results.append((rel, 0, "(matched in content)"))
    for rel, line, snippet in results:
        print(f"{rel}:{line}  {snippet}")
    if not results:
        print("No matches found.")


def cmd_daily(args):
    ensure_vault()
    today = datetime.now().strftime("%Y-%m-%d")
    daily_dir = VAULT / "daily"
    daily_dir.mkdir(exist_ok=True)
    path = daily_dir / f"{today}.md"
    if path.exists():
        print(path.read_text(encoding="utf-8"))
    else:
        content = TEMPLATES["daily"].format(date=today)
        path.write_text(content, encoding="utf-8")
        print(f"Created: daily/{today}.md")


def cmd_list(args):
    ensure_vault()
    target = VAULT / (args.dir or "")
    if not target.exists() or not target.is_dir():
        print(f"Directory not found: {args.dir or '/'}", file=sys.stderr)
        sys.exit(1)
    for f in sorted(target.iterdir()):
        if f.is_file() and f.suffix == ".md" and not f.name.startswith("."):
            rel = f.relative_to(VAULT)
            size = f.stat().st_size
            print(f"{rel}  ({size} bytes)")
        elif f.is_dir() and not f.name.startswith("."):
            rel = f.relative_to(VAULT)
            count = len(list(f.rglob("*.md")))
            print(f"{rel}/  ({count} notes)")


def cmd_template(args):
    ensure_vault()
    name = args.name.lower()
    if name not in TEMPLATES:
        print(f"Available templates: {', '.join(TEMPLATES.keys())}", file=sys.stderr)
        sys.exit(1)
    date = datetime.now().strftime("%Y-%m-%d")
    content = TEMPLATES[name].format(
        date=date,
        title=args.title or name,
        content=args.content or "",
        source=args.source or "",
    )
    print(content)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Second Brain Bridge")
    sub = parser.add_subparsers(dest="command")

    r = sub.add_parser("read", help="Read a note")
    r.add_argument("path", help="Path relative to vault (e.g. projects/foo)")

    w = sub.add_parser("write", help="Write a note (content from stdin)")
    w.add_argument("path", help="Path relative to vault")

    s = sub.add_parser("search", help="Search vault content")
    s.add_argument("query", help="Search query")

    sub.add_parser("daily", help="Create/open today's daily note")

    l = sub.add_parser("list", help="List notes in a directory")
    l.add_argument("dir", nargs="?", default="", help="Subdirectory (optional)")

    t = sub.add_parser("template", help="Generate content from a template")
    t.add_argument("name", help="Template name")
    t.add_argument("--title", default="", help="Note title")
    t.add_argument("--content", default="", help="Note content")
    t.add_argument("--source", default="", help="Source URL (for references)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "read": cmd_read,
        "write": cmd_write,
        "search": cmd_search,
        "daily": cmd_daily,
        "list": cmd_list,
        "template": cmd_template,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
