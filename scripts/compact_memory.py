#!/usr/bin/env python3
"""
compact_memory.py
==================

Motor de compactación jerárquica de memoria para el "segundo cerebro" en Obsidian.

Arquitectura que implementa:

    daily/*.md  --(ventana de N días)-->  weekly/*.md
    weekly/*.md --(umbral de M semanas)--> archive-summary.md (mensual acumulado)
    weekly/*.md más reciente --> re-síntesis de project-context.md
    project-context.md de TODOS los proyectos --> regenera master-index.md global

Estructura de carpetas:

    <vault_root>/
        00-global/
            master-index.md
            conventions.md
        clients/
            <client_name>/
                client-context.md
                projects/
                    <project_name>/
                        daily/YYYY-MM-DD.md
                        weekly/YYYY-Www.md
                        archive-summary.md
                        project-context.md
                        .archive/YYYY-MM-DD.md.gz

Requisitos:
    pip install anthropic --break-system-packages

Variables de entorno:
    ANTHROPIC_API_KEY   (obligatoria)

Uso:
    python compact_memory.py --vault /ruta/a/vault
    python compact_memory.py --vault /ruta/a/vault --client cmasdental
    python compact_memory.py --vault /ruta/a/vault --client cmasdental --project whatsapp-automation
    python compact_memory.py --vault /ruta/a/vault --dry-run
    python compact_memory.py --vault /ruta/a/vault --window-days 7 --weekly-threshold 6
"""

import argparse
import gzip
import logging
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from anthropic import Anthropic
except ImportError:
    print("Falta la librería 'anthropic'. Instala con:")
    print("  pip install anthropic --break-system-packages")
    sys.exit(1)


MODEL = "claude-sonnet-5"
MAX_TOKENS = 2000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("compact_memory")


# --------------------------------------------------------------------------
# Utilidades de fecha / ISO week
# --------------------------------------------------------------------------

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})\.md$")


def parse_date_from_filename(path: Path) -> Optional[date]:
    m = DATE_RE.search(path.name)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y-%m-%d").date()


def iso_week_label(d: date) -> str:
    year, week, _ = d.isocalendar()
    return f"{year}-W{week:02d}"


def month_label(d: date) -> str:
    return d.strftime("%Y-%m")


# --------------------------------------------------------------------------
# Cliente Claude
# --------------------------------------------------------------------------


class Synthesizer:
    """Envoltura delgada sobre la API de Anthropic para tareas de síntesis."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.client = None if dry_run else Anthropic()

    def _call(self, system: str, user_content: str) -> str:
        if self.dry_run:
            preview = user_content[:120].replace("\n", " ")
            return f"[DRY-RUN] Resumen simulado de: {preview}..."

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )
        parts = [block.text for block in response.content if block.type == "text"]
        return "\n".join(parts).strip()

    def synth_weekly(self, project: str, daily_texts: List[str], week_label: str) -> str:
        system = (
            "Eres un asistente que comprime notas diarias de trabajo técnico en un "
            "resumen semanal denso y accionable. Estructura SIEMPRE en estas secciones "
            "markdown: '## Decisiones tomadas', '## Pendientes / siguientes pasos', "
            "'## Aprendizajes técnicos', '## Bugs o riesgos identificados'. "
            "Sé concreto, no repitas texto de las notas, sintetiza. Español técnico."
        )
        joined = "\n\n---\n\n".join(daily_texts)
        user = f"Proyecto: {project}\nSemana: {week_label}\n\nNotas diarias crudas:\n\n{joined}"
        return self._call(system, user)

    def synth_monthly(self, project: str, weekly_texts: List[str], month_lbl: str) -> str:
        system = (
            "Comprimes varios resúmenes semanales de un proyecto en un resumen mensual "
            "de alto nivel. Mantén solo lo que importa a mediano plazo: decisiones "
            "arquitectónicas, features entregadas, deuda técnica pendiente. "
            "Máximo 300 palabras. Español técnico, formato markdown."
        )
        joined = "\n\n---\n\n".join(weekly_texts)
        user = f"Proyecto: {project}\nMes: {month_lbl}\n\nResúmenes semanales:\n\n{joined}"
        return self._call(system, user)

    def resynth_project_context(
        self, project: str, previous_context: str, new_weekly_summary: str
    ) -> str:
        system = (
            "Mantienes el archivo project-context.md de un proyecto: es una 'foto "
            "actual' del estado del proyecto, NO un log acumulativo. Recibes el "
            "contexto anterior y el resumen semanal más reciente. Devuelve una NUEVA "
            "versión completa y fusionada de project-context.md, con estas secciones "
            "fijas: '## Estado actual' (1-3 líneas), '## Objetivo del proyecto', "
            "'## Arquitectura / stack', '## Pendientes activos', "
            "'## Decisiones clave (histórico corto)'. Elimina información obsoleta o "
            "ya resuelta. Sé denso, esto se carga en cada sesión de opencode."
        )
        user = (
            f"Proyecto: {project}\n\n"
            f"--- project-context.md ACTUAL ---\n{previous_context or '(vacío, es la primera síntesis)'}\n\n"
            f"--- Resumen semanal nuevo a incorporar ---\n{new_weekly_summary}"
        )
        return self._call(system, user)

    def extract_status_line(self, project: str, project_context: str) -> str:
        system = (
            "Extrae SOLO la sección '## Estado actual' de este project-context.md "
            "y devuélvela como 1 a 3 líneas de texto plano, sin encabezado markdown, "
            "sin viñetas. Si no existe la sección, infiere el estado en 1-2 líneas."
        )
        user = f"Proyecto: {project}\n\n{project_context}"
        return self._call(system, user)


# --------------------------------------------------------------------------
# Lógica de vault - Adaptada para estructura clients/<client>/projects/<project>
# --------------------------------------------------------------------------


@dataclass
class ProjectPaths:
    root: Path
    client_name: str
    project_name: str
    daily: Path
    weekly: Path
    archive_raw: Path
    archive_summary: Path
    context: Path

    @classmethod
    def for_project(
        cls, clients_root: Path, client_name: str, project_name: str
    ) -> "ProjectPaths":
        root = clients_root / client_name / "projects" / project_name
        return cls(
            root=root,
            client_name=client_name,
            project_name=project_name,
            daily=root / "daily",
            weekly=root / "weekly",
            archive_raw=root / ".archive",
            archive_summary=root / "archive-summary.md",
            context=root / "project-context.md",
        )

    def ensure(self):
        self.daily.mkdir(parents=True, exist_ok=True)
        self.weekly.mkdir(parents=True, exist_ok=True)
        self.archive_raw.mkdir(parents=True, exist_ok=True)


def list_projects(vault_root: Path) -> List[Tuple[str, str]]:
    """Retorna [(client_name, project_name), ...] recorriendo clients/ -> projects/."""
    clients_root = vault_root / "clients"
    if not clients_root.exists():
        return []
    result = []
    for client_dir in sorted(clients_root.iterdir()):
        if client_dir.is_dir() and not client_dir.name.startswith("."):
            projects_dir = client_dir / "projects"
            if projects_dir.exists():
                for proj_dir in sorted(projects_dir.iterdir()):
                    if proj_dir.is_dir() and not proj_dir.name.startswith("."):
                        result.append((client_dir.name, proj_dir.name))
    return result


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, content: str, dry_run: bool):
    if dry_run:
        log.info(f"[DRY-RUN] escribiría {path} ({len(content)} chars)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    log.info(f"Escrito: {path}")


def archive_raw_daily(path: Path, dest_dir: Path, dry_run: bool):
    dest = dest_dir / f"{path.name}.gz"
    if dry_run:
        log.info(f"[DRY-RUN] archivaría {path} -> {dest}")
        return
    with open(path, "rb") as f_in, gzip.open(dest, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    path.unlink()
    log.info(f"Archivado y comprimido: {path.name} -> {dest}")


# --------------------------------------------------------------------------
# Paso 1: daily -> weekly
# --------------------------------------------------------------------------


def compact_daily_to_weekly(
    paths: ProjectPaths, project: str, window_days: int,
    synth: Synthesizer, dry_run: bool
):
    """Agrupa daily notes fuera de ventana por semana ISO y genera weekly + re-sintetiza project-context."""
    cutoff = date.today() - timedelta(days=window_days)
    daily_files = sorted(
        f for f in paths.daily.glob("*.md") if parse_date_from_filename(f)
    )

    to_compact = [f for f in daily_files if parse_date_from_filename(f) < cutoff]
    if not to_compact:
        log.info(f"[{project}] No hay daily notes fuera de la ventana ({window_days}d).")
        return

    # Agrupar por semana ISO
    by_week: dict[str, List[Path]] = {}
    for f in to_compact:
        wk = iso_week_label(parse_date_from_filename(f))
        by_week.setdefault(wk, []).append(f)

    for week_label, files in by_week.items():
        weekly_path = paths.weekly / f"{week_label}.md"
        if weekly_path.exists():
            log.info(f"[{project}] {week_label} ya sintetizada, solo archivo dailies.")
        else:
            daily_texts = [read_text(f) for f in sorted(files)]
            summary = synth.synth_weekly(project, daily_texts, week_label)
            header = f"# {project} — Semana {week_label}\n\n"
            write_text(weekly_path, header + summary, dry_run)

            # Re-sintetizar project-context.md con este nuevo resumen semanal
            prev_context = read_text(paths.context)
            new_context = synth.resynth_project_context(project, prev_context, summary)
            write_text(paths.context, new_context, dry_run)

        for f in sorted(files):
            archive_raw_daily(f, paths.archive_raw, dry_run)


# --------------------------------------------------------------------------
# Paso 2: weekly -> monthly (archive-summary.md acumulado)
# --------------------------------------------------------------------------


def compact_weekly_to_monthly(
    paths: ProjectPaths, project: str, weekly_threshold: int,
    synth: Synthesizer, dry_run: bool
):
    """Comprime weekly/*.md en archive-summary.md cuando se alcanza el umbral."""
    weekly_files = sorted(paths.weekly.glob("*.md"))
    if len(weekly_files) < weekly_threshold:
        return

    weekly_texts = [read_text(f) for f in weekly_files]
    month_lbl = month_label(date.today())
    monthly_summary = synth.synth_monthly(project, weekly_texts, month_lbl)

    existing_archive = read_text(paths.archive_summary)
    new_section = f"\n\n## {month_lbl}\n\n{monthly_summary}\n"
    write_text(paths.archive_summary, existing_archive + new_section, dry_run)

    if not dry_run:
        for f in weekly_files:
            f.unlink()
    log.info(
        f"[{project}] {len(weekly_files)} weekly comprimidos en archive-summary.md "
        f"({month_lbl})."
    )


# --------------------------------------------------------------------------
# Paso 3: regenerar master-index.md global (agrupado por cliente)
# --------------------------------------------------------------------------


def regenerate_master_index(
    vault_root: Path, projects: List[Tuple[str, str]], synth: Synthesizer, dry_run: bool
):
    """Regenera 00-global/master-index.md con estado de todos los proyectos agrupados por cliente."""
    global_dir = vault_root / "00-global"
    global_dir.mkdir(parents=True, exist_ok=True)
    index_path = global_dir / "master-index.md"

    lines = ["# Master Index — Estado global de proyectos", ""]
    lines.append(f"_Última actualización: {datetime.now().isoformat(timespec='minutes')}_")
    lines.append("")

    current_client = None
    clients_root = vault_root / "clients"

    for client_name, project_name in projects:
        if client_name != current_client:
            lines.append(f"## {client_name}")
            lines.append("")
            current_client = client_name

        paths = ProjectPaths.for_project(clients_root, client_name, project_name)
        context = read_text(paths.context)
        if not context.strip():
            status = "(sin síntesis todavía)"
        else:
            status = synth.extract_status_line(project_name, context)
        lines.append(f"### {project_name}")
        lines.append(status)
        lines.append("")

    write_text(index_path, "\n".join(lines), dry_run)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Compactación jerárquica del vault de memoria (estructura clients/)."
    )
    parser.add_argument(
        "--vault", required=True,
        help="Ruta raíz del vault (contiene 00-global/ y clients/)"
    )
    parser.add_argument(
        "--client", help="Procesar solo este cliente (default: todos)"
    )
    parser.add_argument(
        "--project", help="Procesar solo este proyecto (default: todos)"
    )
    parser.add_argument(
        "--window-days", type=int, default=7,
        help="Días que se mantienen como daily crudo (default: 7)"
    )
    parser.add_argument(
        "--weekly-threshold", type=int, default=6,
        help="Nº de weekly antes de comprimir a mensual (default: 6)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="No escribe ni llama a la API, solo simula"
    )
    args = parser.parse_args()

    vault_root = Path(args.vault).expanduser().resolve()
    if not vault_root.exists():
        log.error(f"No existe el vault: {vault_root}")
        sys.exit(1)

    all_projects = list_projects(vault_root)
    if not all_projects:
        log.warning("No se encontraron proyectos en <vault>/clients/<client>/projects/")
        sys.exit(0)

    projects = all_projects
    if args.client:
        projects = [(c, p) for c, p in projects if c == args.client]
    if args.project:
        projects = [(c, p) for c, p in projects if p == args.project]

    if not projects:
        log.warning(f"No hay proyectos que procesar con los filtros dados.")
        sys.exit(0)

    synth = Synthesizer(dry_run=args.dry_run)
    clients_root = vault_root / "clients"

    for client_name, project_name in projects:
        log.info(f"=== Procesando: {client_name}/{project_name} ===")
        paths = ProjectPaths.for_project(clients_root, client_name, project_name)
        paths.ensure()
        compact_daily_to_weekly(
            paths, f"{client_name}/{project_name}",
            args.window_days, synth, args.dry_run
        )
        compact_weekly_to_monthly(
            paths, f"{client_name}/{project_name}",
            args.weekly_threshold, synth, args.dry_run
        )

    # Reconstruir master-index con todos los proyectos globales
    regenerate_master_index(vault_root, projects, synth, args.dry_run)
    log.info("Compactación completa.")


if __name__ == "__main__":
    main()
