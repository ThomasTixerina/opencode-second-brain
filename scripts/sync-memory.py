"""
OpenCode ↔ Obsidian Memory Sync

Bidirectional sync between OpenCode's JSONL memory stores and
the Obsidian vault's markdown notes.

Commands:
    python sync-memory.py to-vault                        Memory JSONL → vault memory/
    python sync-memory.py to-vault --client <c> --project <p>   → clients/<c>/projects/<p>/memory/
    python sync-memory.py from-vault                      Vault memory/ → stdout as JSONL
    python sync-memory.py import-sessions   OpenCode session .md → vault clients/<client>/projects/<project>/daily/
    python sync-memory.py watch             Auto-sync on changes (polling)
"""

import sys
import os
import json
import argparse
import re
import glob
from datetime import datetime
from pathlib import Path
from difflib import SequenceMatcher

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path.home() / "second-brain"
MEMORY_DIR = Path.home() / ".opencode-memory"
SESSION_DIR = Path.home() / ".opencode-sessions"

CLIENTS = {
    "cmasdental": {
        "projects": ["whatsapp-automation"],
    },
    "dr-tomas-tijerina": {
        "projects": ["miconsuluno", "nestjs-supabase-auth", "voice-cli"],
    },
    "personal": {
        "projects": ["flet-primer-app"],
    },
}

SAFE_PATH = "C_Users_user"
MEMORY_FILE = MEMORY_DIR / f"{SAFE_PATH}.jsonl"
GLOBAL_FILE = MEMORY_DIR / "global.jsonl"


def sanitize_name(name: str) -> str:
    """Convert entity name to a safe filename."""
    safe = name.lower().strip()
    safe = re.sub(r"[^\w\s-]", "", safe)
    safe = re.sub(r"[\s_]+", "-", safe)
    return safe[:80] + ".md"


def read_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items


def write_jsonl(path: Path, items: list):
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def entity_to_md(entity: dict, rel_index: str = "memory/_index") -> str:
    name = entity.get("name", "Untitled")
    etype = entity.get("entityType", "")
    observations = entity.get("observations", [])

    tags = [etype.lower()] if etype else []
    tags.append("memory")
    if "project" in etype.lower():
        tags.append("project")

    lines = ["---"]
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    if etype:
        lines.append(f"entityType: {etype}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {name}")
    lines.append("")

    for obs in observations:
        lines.append(f"- {obs}")

    lines.append("")
    lines.append("## Enlaces")
    lines.append(f"- [[{rel_index}|Todas las memorias]]")
    lines.append("")

    return "\n".join(lines)


def md_to_entity(content: str, filename: str) -> dict:
    name = filename.replace(".md", "").replace("-", " ").title()
    etype = "Memory"
    observations = []
    body = content

    # Extract YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for line in fm.split("\n"):
            if line.startswith("entityType:"):
                etype = line.split(":", 1)[1].strip()
        body = content[fm_match.end() :]

    # Extract list items as observations
    for line in body.split("\n"):
        line = line.strip()
        if (
            line.startswith("- ")
            and not line.startswith("- [")
            and not line.startswith("- ``")
        ):
            observations.append(line[2:].strip())

    # Title after frontmatter as name fallback
    title_match = re.search(r"^#\s+(.+)", body, re.MULTILINE)
    if title_match:
        name = title_match.group(1).strip()

    return {
        "type": "entity",
        "name": name,
        "entityType": etype,
        "observations": observations,
    }


def _sync_to_dir(entities: dict, target: Path, label: str, rel_index: str = "memory/_index") -> int:
    """Write entities as .md files into target directory. Returns count written."""
    target.mkdir(parents=True, exist_ok=True)
    written = 0
    for name, entity in sorted(entities.items()):
        filename = sanitize_name(name)
        path = target / filename
        content = entity_to_md(entity, rel_index)
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            if (
                len(content) == len(existing)
                and SequenceMatcher(None, content, existing).ratio() > 0.98
            ):
                continue
        path.write_text(content, encoding="utf-8")
        written += 1
        print(f"  → {filename}")

    print(f"\nSynced {written} entities to vault {label}/")
    return written


def _resolve_client_project(client: str, project: str) -> tuple[Path | None, str]:
    """Resolve (target_path, label) for a (client, project) tuple, or None if invalid."""
    if client not in CLIENTS:
        print(f"Warning: unknown client '{client}'. Skipping client sync.")
        return None, ""
    if project:
        if project not in CLIENTS[client]["projects"]:
            print(f"Warning: unknown project '{project}' for client '{client}'. Skipping.")
            return None, ""
        target = VAULT / "clients" / client / "projects" / project / "memory"
        label = f"clients/{client}/projects/{project}/memory"
    else:
        target = VAULT / "clients" / client / "memory"
        label = f"clients/{client}/memory"
    return target, label


def cmd_to_vault(args):
    """Sync memory JSONL → vault markdown notes."""
    entities = {}
    for mem_file in [MEMORY_FILE, GLOBAL_FILE]:
        for item in read_jsonl(mem_file):
            if item.get("type") == "entity":
                name = item["name"]
                if name not in entities:
                    entities[name] = item
                else:
                    entities[name]["observations"].extend(
                        o
                        for o in item.get("observations", [])
                        if o not in entities[name]["observations"]
                    )

    # Always sync to global vault memory/
    _sync_to_dir(entities, VAULT / "memory", "memory")
    update_index(VAULT / "memory" / "_index.md", entities)

    # If --client specified, sync also to the client/project subtree
    if args.client:
        target, label = _resolve_client_project(args.client, args.project)
        if target:
            # rel_index: for client/project memory, the _index is in the same dir
            rel_index = "_index"
            rel_prefix = str(target.relative_to(VAULT))
            _sync_to_dir(entities, target, label, rel_index)
            target.parent.mkdir(parents=True, exist_ok=True)
            update_index(target / "_index.md", entities, rel_prefix)


def cmd_from_vault(args):
    """Read vault memory/ and output JSONL to stdout."""
    mem_dir = VAULT / "memory"
    if not mem_dir.exists():
        print("[]")
        return

    entities = []
    for md_file in sorted(mem_dir.glob("*.md")):
        if md_file.name == "_index.md":
            continue
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        entity = md_to_entity(content, md_file.stem)
        entities.append(entity)

    print(json.dumps(entities, indent=2, ensure_ascii=False))
    print(f"\n({len(entities)} entities found)", file=sys.stderr)


def cmd_import_sessions(args):
    """Import OpenCode session backups into vault daily/ or client/project daily/."""
    session_dir = Path.home() / ".opencode-sessions"
    if not session_dir.exists():
        print("No sessions directory found.")
        return

    # If --client is specified, sync to client/project daily instead of global daily/
    if args.client:
        target, label = _resolve_client_project(args.client, args.project)
        if not target:
            return
        # Replace "memory" with "daily" in the path
        daily_dir = target.parent / "daily" if args.project else VAULT / "clients" / args.client / "daily"
    else:
        daily_dir = VAULT / "daily"

    daily_dir.mkdir(parents=True, exist_ok=True)

    imported = 0
    for session_file in sorted(session_dir.glob("*.md")):
        date_str = session_file.stem  # YYYY-MM-DD
        tgt = daily_dir / f"{date_str}.md"

        if tgt.exists() and not args.force:
            continue

        content = session_file.read_text(encoding="utf-8", errors="ignore")
        obsidian_content = (
            f"---\ndate: {date_str}\ntags: [daily, session]\n---\n\n{content}"
        )
        tgt.write_text(obsidian_content, encoding="utf-8")
        imported += 1
        print(f"  → {daily_dir.name}/{date_str}.md")

    print(f"\nImported {imported} sessions to vault {daily_dir.relative_to(VAULT)}/")


def update_index(index_path: Path, entities: dict, rel_prefix: str = "memory"):
    """Update a memory/_index.md with a Dataview-compatible listing."""
    lines = [
        "---",
        "tags: [memory, index]",
        "---",
        "",
        "# Memoria Persistente",
        "",
        "> Sincronizado desde OpenCode memory stores. Última actualización: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Entradas",
        "",
    ]

    for name in sorted(entities.keys()):
        filename = sanitize_name(name)
        etype = entities[name].get("entityType", "")
        obs_count = len(entities[name].get("observations", []))
        lines.append(
            f"- [[{rel_prefix}/{filename}|{name}]] — *{etype}* ({obs_count} observaciones)"
        )

    lines.extend(
        [
            "",
            "## Templates",
            "- [[templates/memory|Template de Memoria]]",
            "",
        ]
    )

    index_path.write_text("\n".join(lines), encoding="utf-8")


def cmd_watch(args):
    """Watch for changes and auto-sync."""
    import time

    last_mtime = {}
    for f in [MEMORY_FILE, GLOBAL_FILE]:
        if f.exists():
            last_mtime[str(f)] = f.stat().st_mtime

    print(f"Watching memory stores in {MEMORY_DIR}...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(5)
            changed = []
            for f in [MEMORY_FILE, GLOBAL_FILE]:
                key = str(f)
                if f.exists():
                    mtime = f.stat().st_mtime
                    if key not in last_mtime:
                        last_mtime[key] = mtime
                        changed.append(f.name)
                    elif mtime > last_mtime[key]:
                        last_mtime[key] = mtime
                        changed.append(f.name)

            if changed:
                print(
                    f"\n[{datetime.now().strftime('%H:%M:%S')}] Change detected: {', '.join(changed)}"
                )
                # Watch always syncs to global memory/ only
                class WatchArgs:
                    client = None
                    project = None
                cmd_to_vault(WatchArgs())
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="OpenCode ↔ Obsidian Memory Sync")
    sub = parser.add_subparsers(dest="command")

    tv = sub.add_parser("to-vault", help="Sync memory JSONL → vault .md notes")
    tv.add_argument("--client", help="Sync to a specific client subtree (e.g. cmasdental)")
    tv.add_argument("--project", help="Sync to a specific project within client")

    sub.add_parser("from-vault", help="Vault memory/ → stdout as JSONL")

    imp = sub.add_parser("import-sessions", help="OpenCode sessions → vault daily/")
    imp.add_argument("--client", help="Import to a specific client daily/ instead of global daily/")
    imp.add_argument("--project", help="Import to a specific project daily/ within client")
    imp.add_argument("--force", action="store_true", help="Overwrite existing daily notes")

    sub.add_parser("watch", help="Auto-sync on changes (polling)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "to-vault": cmd_to_vault,
        "from-vault": cmd_from_vault,
        "import-sessions": cmd_import_sessions,
        "watch": cmd_watch,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
