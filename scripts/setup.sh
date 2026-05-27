#!/usr/bin/env bash
set -e

echo "========================================"
echo "  opencode-second-brain — Setup (Linux/Mac)"
echo "========================================"
echo ""

# --- Prerequisites ---
HAS_GIT=false
HAS_PYTHON=false

command -v git >/dev/null 2>&1 && HAS_GIT=true || echo "[WARN] git not found — install from https://git-scm.com"
command -v python3 >/dev/null 2>&1 && HAS_PYTHON=true || echo "[WARN] python3 not found — install from https://python.org"

# --- Clone if needed ---
if [ ! -f "_index.md" ]; then
    if [ "$HAS_GIT" = true ]; then
        echo "Cloning opencode-second-brain..."
        git clone https://github.com/ThomasTixerina/opencode-second-brain.git
        cd opencode-second-brain
    else
        echo "ERROR: git is required to clone. Install git, then run:"
        echo "  git clone https://github.com/ThomasTixerina/opencode-second-brain.git"
        exit 1
    fi
fi

VAULT_DIR=$(pwd)

# --- Obsidian check ---
echo ""
echo "Checking for Obsidian..."
if command -v obsidian >/dev/null 2>&1; then
    echo "Obsidian CLI found. Open the vault:"
    echo "  obsidian \"$VAULT_DIR\""
else
    echo "Open Obsidian → 'Open folder as vault' → select: $VAULT_DIR"
fi

echo ""
echo "========================================"
echo "  ✅ Setup complete!"
echo "========================================"
echo ""
echo "📖 NEXT STEPS"
echo "─────────────"
echo ""
echo "1. Open the vault in Obsidian (see above)"
echo "2. Install Community Plugins:"
echo "   Settings → Community Plugins → Browse → search each:"
echo ""
echo "   🔹 Dataview      (sql-like queries for your vault)"
echo "   🔹 Templater      (advanced templates — press Ctrl+T)"
echo "   🔹 Kanban         (visual project boards)"
echo "   🔹 Omnisearch     (full-text search)"
echo "   🔹 Excalidraw     (hand-drawn diagrams)"
echo ""
echo "   → After installing EACH plugin, click Enable"
echo "   → Config is already in the vault — no setup needed"
echo ""
echo "3. Press Ctrl+T inside a note to insert a template"
echo ""
echo "🤖 OPencode CLI"
echo "──────────────"
echo "  opencode $VAULT_DIR"
echo ""
echo "  OpenCode will read AGENTS.md and connect to your vault."
echo ""
echo "🌐 n8n automation (optional)"
echo "───────────────────────────"
echo "  Import workflows from automation/*.workflow.json"
echo "  in n8n: Settings → Import → From File"
echo ""
echo "📚 More info: $VAULT_DIR/guides/"
echo ""
