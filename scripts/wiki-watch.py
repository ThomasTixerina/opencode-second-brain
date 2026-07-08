"""
wiki-watch.py — Background watcher and scheduler helper

Modes:
    watch       Poll raw/ every N seconds for new files (idle: no LLM calls)
    once        Check and exit (for cron / Task Scheduler)
    notify      Print pending sources to stdout (for shell prompts)

The watcher does NOT auto-ingest — it only notifies.
Human (or AI agent) decides when to run ingest.py --discuss.

Usage:
    python scripts/wiki-watch.py watch [--interval 60]
    python scripts/wiki-watch.py once
    python scripts/wiki-watch.py notify
"""

import argparse
import sys
import time
from datetime import datetime, date
from pathlib import Path

VAULT = Path.home() / "second-brain"
RAW_DIR = VAULT / "raw"
LOG_PATH = VAULT / "log.md"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def get_raw_files() -> dict[str, float]:
    """Return {filename: mtime} for files in raw/ (excluding .gitkeep)."""
    result = {}
    if not RAW_DIR.exists():
        return result
    for f in RAW_DIR.iterdir():
        if f.is_file() and f.name != ".gitkeep":
            result[f.name] = f.stat().st_mtime
    return result


def get_last_lint_date() -> date | None:
    """Parse log.md for the most recent lint entry date."""
    if not LOG_PATH.exists():
        return None
    content = LOG_PATH.read_text(encoding="utf-8")
    import re
    dates = re.findall(r"^## \[(\d{4}-\d{2}-\d{2})\] lint", content, re.MULTILINE)
    if dates:
        return datetime.strptime(dates[-1], "%Y-%m-%d").date()
    return None


def do_notify() -> bool:
    """Print pending sources and return whether lint is due."""
    raw = get_raw_files()
    if raw:
        names = "\n".join(f"  • {n}" for n in sorted(raw.keys()))
        print(f"[wiki-watch] {len(raw)} pending source(s) in raw/:\n{names}")
    else:
        print("[wiki-watch] No pending sources.")

    last_lint = get_last_lint_date()
    now = date.today()
    if last_lint:
        days_since = (now - last_lint).days
        if days_since >= 1:
            print(f"[wiki-watch] Lint due: {days_since}d since last check ({last_lint}).")
            return True
    else:
        print("[wiki-watch] No lint record found — first run?")
        return True

    return False


def cmd_watch(args):
    """Poll raw/ every N seconds, notify on new files."""
    interval = args.interval
    known: dict[str, float] = get_raw_files()
    last_lint_notify = date.today()

    print(f"[wiki-watch] Watching {RAW_DIR} every {interval}s...")
    print("[wiki-watch] Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(interval)
            current = get_raw_files()

            new_files = {k for k in current if k not in known}
            removed_files = {k for k in known if k not in current}

            if new_files:
                ts = datetime.now().strftime("%H:%M:%S")
                for name in sorted(new_files):
                    print(f"[{ts}] New source: raw/{name}")
                    print(f"  → Review with: python scripts/ingest.py draft raw/{name}")

            known = current

            # Check lint status once daily
            now = date.today()
            if now > last_lint_notify:
                last_lint = get_last_lint_date()
                if last_lint and (now - last_lint).days >= 1:
                    print(
                        f"[{datetime.now().strftime('%H:%M:%S')}] "
                        f"Lint due: {(now - last_lint).days}d since last check."
                    )
                last_lint_notify = now

    except KeyboardInterrupt:
        print("\n[wiki-watch] Stopped.")


def cmd_once(args):
    """Single check and exit (for Task Scheduler)."""
    raw = get_raw_files()
    if raw:
        print(f"[wiki-watch] {len(raw)} pending source(s) in raw/")
        for name in sorted(raw.keys()):
            print(f"  • {name}")
    else:
        print("[wiki-watch] OK — no pending sources.")

    last_lint = get_last_lint_date()
    now = date.today()
    if last_lint:
        days_since = (now - last_lint).days
        if days_since >= 1:
            print(f"[wiki-watch] Lint due: {days_since}d since last check ({last_lint}).")
    else:
        print("[wiki-watch] No lint record found.")


def cmd_notify(args):
    """Print status for shell prompt integration."""
    lint_due = do_notify()
    sys.exit(1 if lint_due else 0)


def main():
    parser = argparse.ArgumentParser(
        description="wiki-watch.py — Background watcher and scheduler helper"
    )
    sub = parser.add_subparsers(dest="command")

    w = sub.add_parser("watch", help="Poll raw/ continuously")
    w.add_argument("--interval", type=int, default=60,
                   help="Polling interval in seconds (default: 60)")

    sub.add_parser("once", help="Single check and exit (for Task Scheduler)")
    sub.add_parser("notify", help="Print status, exit code 1 if lint due")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "watch": cmd_watch,
        "once": cmd_once,
        "notify": cmd_notify,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
