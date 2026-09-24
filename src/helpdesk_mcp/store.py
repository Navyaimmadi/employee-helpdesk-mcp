"""Read-only data access with validation and path-scope enforcement."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = (PROJECT_ROOT / "data").resolve()
TICKETS_FILE = DATA_ROOT / "tickets.json"
KNOWLEDGE_ROOT = (DATA_ROOT / "knowledge").resolve()


class StoreError(Exception):
    """Safe, user-facing storage error."""


def _load_tickets() -> list[dict[str, Any]]:
    try:
        with TICKETS_FILE.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise StoreError("The ticket data source is temporarily unavailable.") from exc

    if not isinstance(data, list):
        raise StoreError("The ticket data source returned an invalid format.")
    return data


def search_tickets(query: str, status: str | None = None) -> list[dict[str, Any]]:
    cleaned = query.strip().lower()
    if len(cleaned) < 2:
        raise StoreError("Search query must contain at least 2 characters.")

    allowed_statuses = {"open", "in_progress", "resolved"}
    if status is not None and status not in allowed_statuses:
        raise StoreError("Status must be open, in_progress, or resolved.")

    matches: list[dict[str, Any]] = []
    for ticket in _load_tickets():
        searchable = " ".join(
            str(ticket.get(field, ""))
            for field in ("id", "title", "description", "category", "assignee")
        ).lower()
        if cleaned in searchable and (status is None or ticket.get("status") == status):
            matches.append(ticket)
    return matches


def get_ticket(ticket_id: str) -> dict[str, Any]:
    normalized = ticket_id.strip().upper()
    if not re.fullmatch(r"TKT-\d{3}", normalized):
        raise StoreError("Ticket ID must use the format TKT-###.")
    for ticket in _load_tickets():
        if ticket.get("id") == normalized:
            return ticket
    raise StoreError(f"Ticket {normalized} was not found.")


def analyze_queue() -> dict[str, Any]:
    tickets = _load_tickets()
    by_status: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    for ticket in tickets:
        status = str(ticket.get("status", "unknown"))
        priority = str(ticket.get("priority", "unknown"))
        by_status[status] = by_status.get(status, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
    open_count = sum(count for state, count in by_status.items() if state != "resolved")
    return {
        "total_tickets": len(tickets),
        "active_tickets": open_count,
        "by_status": by_status,
        "by_priority": by_priority,
    }


def read_knowledge_file(relative_path: str) -> str:
    """Read only Markdown files beneath the configured knowledge root."""
    if not relative_path.endswith(".md"):
        raise StoreError("Only Markdown knowledge files can be read.")

    candidate = (KNOWLEDGE_ROOT / relative_path).resolve()
    if not candidate.is_relative_to(KNOWLEDGE_ROOT):
        raise StoreError("Requested path is outside the allowed knowledge root.")
    if not candidate.is_file():
        raise StoreError("The requested knowledge file was not found.")
    try:
        return candidate.read_text(encoding="utf-8")
    except OSError as exc:
        raise StoreError("The knowledge source is temporarily unavailable.") from exc
