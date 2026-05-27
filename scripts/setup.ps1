#Requires -Version 5.1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  opencode-second-brain — Setup (Windows)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Prerequisites ---
$hasGit = $false
$hasPython = $false

try { git --version | Out-Null; $hasGit = $true } catch { Write-Warning "git not found — install from https://git-scm.com" }
try { python --version | Out-Null; $hasPython = $true } catch { Write-Warning "Python not found — install from https://python.org" }

# --- Clone if needed ---
if (-not (Test-Path "_index.md")) {
    if ($hasGit) {
        Write-Host "Cloning opencode-second-brain..."
        git clone https://github.com/ThomasTixerina/opencode-second-brain.git
        Set-Location opencode-second-brain
    } else {
        Write-Error "git is required to clone. Install git, then run:"
        Write-Host "  git clone https://github.com/ThomasTixerina/opencode-second-brain.git"
        exit 1
    }
}

$vaultDir = (Get-Location).Path

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ Setup complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 NEXT STEPS" -ForegroundColor Yellow
Write-Host "─────────────"
Write-Host ""
Write-Host "1. Open the vault in Obsidian:"
Write-Host "   Open Obsidian → 'Open folder as vault' → select:"
Write-Host "   $vaultDir"
Write-Host ""
Write-Host "2. Install Community Plugins:"
Write-Host "   Settings → Community Plugins → Browse → search each:"
Write-Host ""
Write-Host "   🔹 Dataview      (sql-like queries for your vault)"
Write-Host "   🔹 Templater      (advanced templates — press Ctrl+T)"
Write-Host "   🔹 Kanban         (visual project boards)"
Write-Host "   🔹 Omnisearch     (full-text search)"
Write-Host "   🔹 Excalidraw     (hand-drawn diagrams)"
Write-Host ""
Write-Host "   → After installing EACH plugin, click Enable"
Write-Host "   → Config is already in the vault — no setup needed"
Write-Host ""
Write-Host "3. Press Ctrl+T inside a note to insert a template"
Write-Host ""
Write-Host "🤖 OPencode CLI" -ForegroundColor Yellow
Write-Host "──────────────"
Write-Host "  opencode $vaultDir"
Write-Host ""
Write-Host "  OpenCode will read AGENTS.md and connect to your vault."
Write-Host ""
Write-Host "🌐 n8n automation (optional)" -ForegroundColor Yellow
Write-Host "───────────────────────────"
Write-Host "  Import workflows from automation/*.workflow.json"
Write-Host "  in n8n: Settings → Import → From File"
Write-Host ""
Write-Host "📚 More info: $vaultDir\guides\" -ForegroundColor Gray
Write-Host ""
