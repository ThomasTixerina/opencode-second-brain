"""
Ingest Pipeline — raw → wiki

Usage:
    python ingest.py list                       List pending sources in raw/
    python ingest.py draft <raw_file>           Generate JSON template for a source
    python ingest.py commit <raw_file>          Write wiki pages from stdin JSON
    python ingest.py log                        Show recent log entries
    python ingest.py status                     Count wiki contents

Workflow for AI agents:
    1. ingest.py draft raw/<file>    →  get JSON template with source summary from raw
    2. Fill entities, concepts, summary  →  pipe JSON to:
    3. ingest.py commit raw/<file>   →  writes wiki pages, updates index + log

JSON schema for commit:
{
    "title": "Article title",
    "source_url": "",
    "date": "2026-07-08",
    "summary": "Brief one-paragraph summary",
    "key_points": ["Point 1", "Point 2"],
    "entities": [
        {"name": "...", "entityType": "person|company|tool", "context": "...", "relations": ["..."], "sources": ["[[wiki/sources/...]]"]}
    ],
    "concepts": [
        {"name": "...", "category": "architecture|pattern|idea", "definition": "...", "context": "...", "implementation": "...", "sources": ["[[wiki/sources/...]]"]}
    ]
}
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

VAULT = Path.home() / "second-brain"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
RAW_DIR = VAULT / "raw"
WIKI_DIR = VAULT / "wiki"
ENTITIES_DIR = WIKI_DIR / "entities"
CONCEPTS_DIR = WIKI_DIR / "concepts"
SOURCES_DIR = WIKI_DIR / "sources"
SYNTHESIS_DIR = WIKI_DIR / "synthesis"
INDEX_PATH = WIKI_DIR / "_index.md"
LOG_PATH = VAULT / "log.md"

TODAY = date.today().isoformat()


def slugify(name: str) -> str:
    name = re.sub(r"\.md$", "", name)
    name = re.sub(r"[^\w\s-]", "", name.lower())
    name = re.sub(r"[\s_]+", "-", name)
    return name[:80]


def read_frontmatter(path: Path) -> dict:
    """Return existing YAML frontmatter as dict (string values)."""
    content = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


def update_frontmatter_field(path: Path, field: str, value: str):
    """Update a single YAML frontmatter field in-place."""
    content = path.read_text(encoding="utf-8")
    m = re.match(r"^(---\s*\n)(.*?)(\n---)", content, re.DOTALL)
    if not m:
        return
    body = m.group(2)
    if re.search(rf"^{field}:", body, re.MULTILINE):
        body = re.sub(
            rf"^({field}:).*$", rf"\1 {value}", body, flags=re.MULTILINE
        )
    else:
        body += f"\n{field}: {value}"
    updated = m.group(1) + body + m.group(3) + content[m.end():]
    path.write_text(updated, encoding="utf-8")


def build_source_md(title: str, source_url: str, date_str: str,
                    summary: str, key_points: list[str]) -> str:
    pts = "\n".join(f"{i}. {p}" for i, p in enumerate(key_points, 1))
    url_line = f"url: {source_url}" if source_url else "url:"
    return (
        f"---\n"
        f"tags: [source, reference]\n"
        f"source: {title}\n"
        f"{url_line}\n"
        f"date: {date_str}\n"
        f"---\n"
        f"\n"
        f"# {title}\n"
        f"\n"
        f"## Resumen\n"
        f"\n"
        f"{summary}\n"
        f"\n"
        f"## Puntos clave\n"
        f"\n"
        f"{pts}\n"
        f"\n"
        f"## Relacionado con\n"
        f"\n"
        f"- \n"
        f"\n"
        f"## Enlaces\n"
        f"\n"
        f"- [[wiki/_index|Wiki principal]]\n"
    )


def build_entity_md(name: str, entity_type: str, context: str,
                    relations: list[str], sources: list[str]) -> str:
    rels = "\n".join(f"- {r}" for r in relations) if relations else "- "
    srcs = "\n".join(f"- {s}" for s in sources) if sources else "- [[wiki/sources/_index|Ver fuentes relacionadas]]"
    return (
        f"---\n"
        f"tags: [entity]\n"
        f"entityType: {entity_type}\n"
        f"aliases:\n"
        f"related:\n"
        f"created: {TODAY}\n"
        f"updated: {TODAY}\n"
        f"---\n"
        f"\n"
        f"# {name}\n"
        f"\n"
        f"## Contexto\n"
        f"\n"
        f"- {context}\n"
        f"\n"
        f"## Relaciones\n"
        f"\n"
        f"{rels}\n"
        f"\n"
        f"## Fuentes\n"
        f"\n"
        f"{srcs}\n"
        f"\n"
        f"## Enlaces\n"
        f"\n"
        f"- [[wiki/_index|Wiki principal]]\n"
    )


def build_concept_md(name: str, category: str, definition: str,
                     context: str, implementation: str,
                     sources: list[str]) -> str:
    srcs = "\n".join(f"- {s}" for s in sources) if sources else "- [[wiki/sources/_index|Ver fuentes relacionadas]]"
    return (
        f"---\n"
        f"tags: [concept]\n"
        f"category: {category}\n"
        f"related:\n"
        f"created: {TODAY}\n"
        f"updated: {TODAY}\n"
        f"---\n"
        f"\n"
        f"# {name}\n"
        f"\n"
        f"## Definición\n"
        f"\n"
        f"- {definition}\n"
        f"\n"
        f"## Contexto\n"
        f"\n"
        f"- {context}\n"
        f"\n"
        f"## Implementación\n"
        f"\n"
        f"- {implementation}\n"
        f"\n"
        f"## Fuentes\n"
        f"\n"
        f"{srcs}\n"
        f"\n"
        f"## Enlaces\n"
        f"\n"
        f"- [[wiki/_index|Wiki principal]]\n"
    )


def append_to_log(entry_type: str, title: str, detail: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"\n## [{TODAY}] {entry_type} | {title}\n\n{detail}\n"
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)


def update_index_timestamp():
    if INDEX_PATH.exists():
        update_frontmatter_field(INDEX_PATH, "updated", TODAY)


def find_existing_entity(name: str) -> Path | None:
    slug = slugify(name)
    for p in ENTITIES_DIR.glob("*.md"):
        if p.stem == slug:
            return p
    return None


def find_existing_concept(name: str) -> Path | None:
    slug = slugify(name)
    for p in CONCEPTS_DIR.glob("*.md"):
        if p.stem == slug:
            return p
    return None


def append_observation(path: Path, observation: str):
    """Append a new observation/context line to an existing page."""
    content = path.read_text(encoding="utf-8")
    content = content.rstrip() + f"\n- {observation}\n"
    path.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------


def cmd_list(args):
    sources = [f for f in sorted(RAW_DIR.iterdir())
               if f.is_file() and f.name != ".gitkeep"]
    if not sources:
        print("No pending sources in raw/")
        return
    for f in sources:
        size = f.stat().st_size
        print(f"{f.name}  ({size} bytes)")


def cmd_draft(args):
    raw_path = Path(args.raw_file)
    if not raw_path.is_absolute():
        raw_path = VAULT / raw_path
    if not raw_path.exists():
        print(f"File not found: {raw_path}", file=sys.stderr)
        sys.exit(1)

    title = raw_path.stem.replace("-", " ").replace("_", " ").title()
    slug = slugify(raw_path.stem)

    draft = {
        "title": title,
        "source_url": "",
        "date": TODAY,
        "summary": "",
        "key_points": [""],
        "entities": [
            {
                "name": "",
                "entityType": "person|company|tool",
                "context": "",
                "relations": [""],
                "sources": [f"[[wiki/sources/{slug}]]"]
            }
        ],
        "concepts": [
            {
                "name": "",
                "category": "architecture|pattern|idea",
                "definition": "",
                "context": "",
                "implementation": "",
                "sources": [f"[[wiki/sources/{slug}]]"]
            }
        ]
    }
    print(json.dumps(draft, indent=2, ensure_ascii=False))


def cmd_commit(args):
    raw_path = Path(args.raw_file)
    if not raw_path.is_absolute():
        raw_path = VAULT / raw_path
    if not raw_path.exists():
        print(f"File not found: {raw_path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"Invalid JSON on stdin: {e}", file=sys.stderr)
        sys.exit(1)

    slug = slugify(raw_path.stem)
    title = data.get("title", raw_path.stem)

    # 1. Write source summary
    source_md = build_source_md(
        title=title,
        source_url=data.get("source_url", ""),
        date_str=data.get("date", TODAY),
        summary=data.get("summary", ""),
        key_points=data.get("key_points", []),
    )
    source_path = SOURCES_DIR / f"{slug}.md"
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    source_path.write_text(source_md, encoding="utf-8")
    print(f"  → wiki/sources/{slug}.md")

    # 2. Write entities
    for entity in data.get("entities", []):
        name = entity.get("name", "").strip()
        if not name:
            continue
        existing = find_existing_entity(name)
        if existing and args.update:
            update_frontmatter_field(existing, "updated", TODAY)
            if entity.get("context"):
                append_observation(existing, entity["context"])
            print(f"  → wiki/entities/{existing.name} (updated)")
        elif not existing:
            entity_md = build_entity_md(
                name=name,
                entity_type=entity.get("entityType", ""),
                context=entity.get("context", ""),
                relations=entity.get("relations", []),
                sources=entity.get("sources", [f"[[wiki/sources/{slug}]]"]),
            )
            e_path = ENTITIES_DIR / f"{slugify(name)}.md"
            ENTITIES_DIR.mkdir(parents=True, exist_ok=True)
            e_path.write_text(entity_md, encoding="utf-8")
            print(f"  → wiki/entities/{slugify(name)}.md")

    # 3. Write concepts
    for concept in data.get("concepts", []):
        name = concept.get("name", "").strip()
        if not name:
            continue
        existing = find_existing_concept(name)
        if existing and args.update:
            update_frontmatter_field(existing, "updated", TODAY)
            if concept.get("definition"):
                append_observation(existing, concept["definition"])
            print(f"  → wiki/concepts/{existing.name} (updated)")
        elif not existing:
            concept_md = build_concept_md(
                name=name,
                category=concept.get("category", ""),
                definition=concept.get("definition", ""),
                context=concept.get("context", ""),
                implementation=concept.get("implementation", ""),
                sources=concept.get("sources", [f"[[wiki/sources/{slug}]]"]),
            )
            c_path = CONCEPTS_DIR / f"{slugify(name)}.md"
            CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
            c_path.write_text(concept_md, encoding="utf-8")
            print(f"  → wiki/concepts/{slugify(name)}.md")

    # 4. Update index timestamp
    update_index_timestamp()

    # 5. Append to log
    detail = f"Fuente: `{raw_path.name}` → `wiki/sources/{slug}.md`"
    if data.get("entities"):
        detail += f"\nEntidades: {', '.join(e['name'] for e in data['entities'] if e.get('name'))}"
    if data.get("concepts"):
        detail += f"\nConceptos: {', '.join(c['name'] for c in data['concepts'] if c.get('name'))}"
    append_to_log("ingest", title, detail)
    print(f"  → log.md (appended)")


def cmd_log(args):
    if not LOG_PATH.exists():
        print("log.md is empty.")
        return
    content = LOG_PATH.read_text(encoding="utf-8")
    entries = re.findall(r"^## \[.*", content, re.MULTILINE)
    for entry in entries[-10:]:
        print(entry)


def cmd_status(args):
    src_count = len([f for f in SOURCES_DIR.glob("*.md") if f.name != "_index.md"])
    ent_count = len([f for f in ENTITIES_DIR.glob("*.md") if f.name != "_index.md"])
    con_count = len([f for f in CONCEPTS_DIR.glob("*.md") if f.name != "_index.md"])
    syn_count = len([f for f in SYNTHESIS_DIR.glob("*.md") if f.name != "_index.md"])
    raw_count = len([f for f in RAW_DIR.iterdir() if f.is_file() and f.name != ".gitkeep"])

    print(f"Sources:     {src_count}")
    print(f"Entities:    {ent_count}")
    print(f"Concepts:    {con_count}")
    print(f"Synthesis:   {syn_count}")
    print(f"Pending raw: {raw_count}")
    print()
    print(f"RAW_DIR:   {RAW_DIR}")
    print(f"SOURCES:   {SOURCES_DIR}")
    print(f"ENTITIES:  {ENTITIES_DIR}")
    print(f"CONCEPTS:  {CONCEPTS_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Ingest Pipeline — raw → wiki")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List pending sources in raw/")

    d = sub.add_parser("draft", help="Generate JSON template for a source")
    d.add_argument("raw_file", help="Path relative to vault or absolute")

    c = sub.add_parser("commit", help="Write wiki pages from stdin JSON")
    c.add_argument("raw_file", help="Path of the source file being ingested")
    c.add_argument("--update", action="store_true",
                   help="Update existing entities/concepts instead of skipping")

    sub.add_parser("log", help="Show recent log entries")
    sub.add_parser("status", help="Count wiki contents")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "list": cmd_list,
        "draft": cmd_draft,
        "commit": cmd_commit,
        "log": cmd_log,
        "status": cmd_status,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
