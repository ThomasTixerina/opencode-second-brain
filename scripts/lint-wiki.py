"""
lint-wiki.py — Health check for the wiki

Scans all wiki pages and reports:
  - Orphans (pages with no inbound links from other wiki pages)
  - Broken wikilinks ([[wiki/...]] pointing to non-existent files)
  - Stale sources (older than N days)
  - Summary statistics

Usage:
    python scripts/lint-wiki.py                    Print report to stdout
    python scripts/lint-wiki.py --report           Write wiki/lint-report-YYYY-MM-DD.md
    python scripts/lint-wiki.py --fix              Auto-fix: remove stale .gitkeep entries
    python scripts/lint-wiki.py --stale-days 90    Custom stale threshold
"""

import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from collections import defaultdict

VAULT = Path.home() / "second-brain"
WIKI_DIR = VAULT / "wiki"
REPORT_DIR = WIKI_DIR
LOG_PATH = VAULT / "log.md"

WIKI_SUBDIRS = {"entities", "concepts", "synthesis", "sources"}

WIKILINK_RE = re.compile(r"\[\[([^\]]+?)(?:#[^\]]*)?(?:\|[^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def today() -> str:
    return date.today().isoformat()


def all_wiki_files() -> list[Path]:
    files = []
    for subdir in WIKI_SUBDIRS:
        d = WIKI_DIR / subdir
        if d.exists():
            for f in sorted(d.glob("*.md")):
                if f.name != "_index.md":
                    files.append(f)
    return files


def all_vault_md_files() -> list[Path]:
    """Return all .md files in the vault (excluding .obsidian and scripts)."""
    files = []
    for f in VAULT.rglob("*.md"):
        parts = f.relative_to(VAULT).parts
        if ".obsidian" in parts or parts[0] in ("scripts",):
            continue
        files.append(f)
    return files


def parse_wikilinks(content: str) -> list[str]:
    """Extract all [[wikilink]] targets from content."""
    links = []
    for m in WIKILINK_RE.finditer(content):
        target = m.group(1).strip()
        links.append(target)
    return links


def resolve_wikilink(target: str) -> Path | None:
    """Try to resolve a wikilink target to an actual file in the vault."""
    # Normalise
    if not target.endswith(".md"):
        target_md = target + ".md"
    else:
        target_md = target

    # Try direct path
    candidate = VAULT / target_md
    if candidate.exists():
        return candidate

    # Try from wiki subdirs
    for subdir in WIKI_SUBDIRS:
        candidate = WIKI_DIR / subdir / target_md
        if candidate.exists():
            return candidate
        # Try just the filename without subdir
        candidate = WIKI_DIR / target_md
        if candidate.exists():
            return candidate

    # Try without prefixes (e.g., [[entity/foo]] → wiki/entities/foo.md)
    if "/" in target:
        parts = target.split("/")
        candidate = VAULT / "wiki" / target_md
        if candidate.exists():
            return candidate

    return None


def is_wiki_page(path: Path) -> bool:
    """Check if a path is inside wiki/."""
    try:
        rel = path.relative_to(VAULT)
        return rel.parts[0] == "wiki"
    except ValueError:
        return False


def strip_section(target: str) -> str:
    """Remove #section from a wikilink target."""
    return target.split("#")[0].strip()


def lint(args):
    stale_days = args.stale_days
    report_lines = []
    report_lines.append(f"# Wiki Lint Report — {today()}")
    report_lines.append("")
    report_lines.append(f"> Escaneo automático de la wiki. Generado: {datetime.now().isoformat(timespec='minutes')}")
    report_lines.append("")

    all_files = all_wiki_files()
    all_vault = all_vault_md_files()

    # 1. Build link graph
    inbound = defaultdict(set)
    outbound = defaultdict(set)
    wiki_paths_set = {str(f.resolve()) for f in all_files}

    for f in all_vault:
        content = f.read_text(encoding="utf-8", errors="ignore")
        links = parse_wikilinks(content)
        for link in links:
            clean = strip_section(link)
            resolved = resolve_wikilink(clean)
            if resolved:
                resolved_str = str(resolved.resolve())
                inbound[resolved_str].add(str(f.resolve()))
                outbound[str(f.resolve())].add(resolved_str)

    # 2. Orphans — wiki pages with no inbound links from other wiki pages
    orphans = []
    for f in all_files:
        f_str = str(f.resolve())
        # Only count inbound links from OTHER wiki pages
        wiki_inbound = {
            src for src in inbound.get(f_str, set())
            if is_wiki_page(Path(src)) and src != f_str
        }
        if not wiki_inbound:
            rel = f.relative_to(VAULT)
            orphans.append(rel)

    report_lines.append(f"## Resultados")
    report_lines.append("")
    report_lines.append(f"- **Total wiki pages:** {len(all_files)}")
    report_lines.append(f"- **Orphans (sin inbound links):** {len(orphans)}")
    report_lines.append("")
    if orphans:
        report_lines.append("### Paginas huerfanas")
        report_lines.append("")
        for rel in orphans:
            report_lines.append(f"- `{rel}`")
        report_lines.append("")

    # 3. Broken wikilinks across all vault files
    broken = []
    for f in all_vault:
        content = f.read_text(encoding="utf-8", errors="ignore")
        links = parse_wikilinks(content)
        for link in links:
            clean = strip_section(link)
            # Only check wiki links
            if clean.startswith("wiki/") or any(
                clean.startswith(s) for s in WIKI_SUBDIRS
            ):
                resolved = resolve_wikilink(clean)
                if not resolved:
                    rel = f.relative_to(VAULT)
                    broken.append((str(rel), clean))

    # Also check for [[wiki/sources/_index]], [[wiki/entities/foo]] etc
    for f in all_vault:
        content = f.read_text(encoding="utf-8", errors="ignore")
        links = parse_wikilinks(content)
        for link in links:
            clean = strip_section(link)
            if clean.startswith("wiki/entities/") or clean.startswith("entities/"):
                resolved = resolve_wikilink(clean)
                if not resolved:
                    rel = f.relative_to(VAULT)
                    broken.append((str(rel), clean))
            elif clean.startswith("wiki/concepts/") or clean.startswith("concepts/"):
                resolved = resolve_wikilink(clean)
                if not resolved:
                    rel = f.relative_to(VAULT)
                    broken.append((str(rel), clean))
            elif clean.startswith("wiki/sources/") or clean.startswith("sources/"):
                resolved = resolve_wikilink(clean)
                if not resolved:
                    rel = f.relative_to(VAULT)
                    broken.append((str(rel), clean))
            elif clean.startswith("wiki/synthesis/") or clean.startswith("synthesis/"):
                resolved = resolve_wikilink(clean)
                if not resolved:
                    rel = f.relative_to(VAULT)
                    broken.append((str(rel), clean))

    # Deduplicate
    broken = list(set(broken))

    report_lines.append(f"- **Broken wikilinks:** {len(broken)}")
    report_lines.append("")
    if broken:
        report_lines.append("### Enlaces rotos a la wiki")
        report_lines.append("")
        report_lines.append("| Pagina | Enlace roto |")
        report_lines.append("|--------|-------------|")
        for src, tgt in sorted(broken):
            report_lines.append(f"| `{src}` | `{tgt}` |")
        report_lines.append("")

    # 4. Stale sources
    stale_cutoff = date.today() - timedelta(days=stale_days)
    stale_sources = []
    sources_dir = WIKI_DIR / "sources"
    if sources_dir.exists():
        for f in sorted(sources_dir.glob("*.md")):
            if f.name == "_index.md":
                continue
            content = f.read_text(encoding="utf-8", errors="ignore")
            fm_match = FRONTMATTER_RE.search(content)
            if fm_match:
                fm_text = fm_match.group(1)
                date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", fm_text)
                if date_match:
                    src_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
                    if src_date < stale_cutoff:
                        rel = f.relative_to(VAULT)
                        stale_sources.append((str(rel), src_date.isoformat()))

    report_lines.append(f"- **Stale sources (>{stale_days}d):** {len(stale_sources)}")
    report_lines.append("")
    if stale_sources:
        report_lines.append("### Fuentes desactualizadas")
        report_lines.append("")
        report_lines.append("| Fuente | Fecha |")
        report_lines.append("|--------|-------|")
        for rel, sdate in stale_sources:
            report_lines.append(f"| `{rel}` | {sdate} |")
        report_lines.append("")

    # 5. Summary stats by type
    report_lines.append("### Desglose por tipo")
    report_lines.append("")
    for subdir in WIKI_SUBDIRS:
        d = WIKI_DIR / subdir
        if d.exists():
            count = len([f for f in d.glob("*.md") if f.name != "_index.md"])
            report_lines.append(f"- **{subdir}:** {count}")
    report_lines.append("")

    report_text = "\n".join(report_lines)

    if args.report:
        report_path = REPORT_DIR / f"lint-report-{today()}.md"
        report_path.write_text(report_text, encoding="utf-8")
        print(f"Report written: {report_path}")
    else:
        print(report_text)


def cmd_lint(args):
    lint(args)


def main():
    parser = argparse.ArgumentParser(
        description="lint-wiki.py — Health check for the wiki"
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Write report to wiki/lint-report-YYYY-MM-DD.md"
    )
    parser.add_argument(
        "--stale-days", type=int, default=365,
        help="Days after which a source is considered stale (default: 365)"
    )
    args = parser.parse_args()
    lint(args)


if __name__ == "__main__":
    main()
