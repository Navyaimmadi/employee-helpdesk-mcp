"""FastMCP server exposing help-desk tools, resources, and prompts."""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from . import store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("helpdesk_mcp")

mcp = FastMCP(name="Employee Help Desk")


def _run_tool(name: str, operation) -> Any:
    started = time.perf_counter()
    try:
        result = operation()
        logger.info("tool=%s outcome=success duration_ms=%.2f", name, (time.perf_counter() - started) * 1000)
        return result
    except store.StoreError as exc:
        logger.warning("tool=%s outcome=expected_error duration_ms=%.2f", name, (time.perf_counter() - started) * 1000)
        raise ToolError(str(exc)) from exc
    except Exception as exc:
        logger.exception("tool=%s outcome=internal_error", name)
        raise ToolError("The help-desk service could not complete the request.") from exc


@mcp.tool
def search_tickets(query: str, status: str | None = None) -> list[dict[str, Any]]:
    """Search support tickets by text and optional status."""
    return _run_tool("search_tickets", lambda: store.search_tickets(query, status))


@mcp.tool
def get_ticket(ticket_id: str) -> dict[str, Any]:
    """Retrieve one support ticket by its TKT-### identifier."""
    return _run_tool("get_ticket", lambda: store.get_ticket(ticket_id))


@mcp.tool
def analyze_queue() -> dict[str, Any]:
    """Summarize ticket counts by status and priority."""
    return _run_tool("analyze_queue", store.analyze_queue)


@mcp.tool
def read_knowledge_file(relative_path: str) -> str:
    """Read a Markdown file within the approved help-desk knowledge root."""
    return _run_tool(
        "read_knowledge_file",
        lambda: store.read_knowledge_file(relative_path),
    )


@mcp.resource(
    "helpdesk://knowledge/password-reset",
    name="Password reset guide",
    description="Approved password reset procedure for employees.",
    mime_type="text/markdown",
)
def password_reset_guide() -> str:
    return store.read_knowledge_file("password-reset.md")


@mcp.resource(
    "helpdesk://knowledge/vpn-troubleshooting",
    name="VPN troubleshooting guide",
    description="Approved first-line troubleshooting for remote-access VPN issues.",
    mime_type="text/markdown",
)
def vpn_troubleshooting_guide() -> str:
    return store.read_knowledge_file("vpn-troubleshooting.md")


@mcp.resource(
    "helpdesk://queue/summary",
    name="Current queue summary",
    description="Current aggregate ticket counts without employee-sensitive fields.",
    mime_type="application/json",
)
def queue_summary() -> str:
    return json.dumps(store.analyze_queue(), indent=2)


@mcp.prompt
def triage_ticket(ticket_id: str) -> str:
    """Create a reusable instruction for reviewing and triaging one ticket."""
    return (
        f"Review help-desk ticket {ticket_id}. Use get_ticket for the record, "
        "consult an appropriate knowledge resource, identify urgency and likely category, "
        "and recommend the next safe support step. Do not invent missing facts or perform "
        "a write action. Cite the resource URI used."
    )

