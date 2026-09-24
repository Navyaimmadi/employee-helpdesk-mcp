"""MCP client that discovers and invokes every required component type."""

from __future__ import annotations

import json
from pathlib import Path

from fastmcp import Client
from fastmcp.exceptions import ToolError

from .store import DATA_ROOT, PROJECT_ROOT


def _display(value: object) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, indent=2, default=str)


async def run_demo() -> None:
    server_path = PROJECT_ROOT / "server.py"

    # Client-side safety control: advertise only the project data directory as a root.
    # The server independently enforces the same boundary for file access.
    client = Client(
        Path(server_path),
        roots=[DATA_ROOT.as_uri()],
        timeout=15.0,
    )

    async with client:
        print("=== SERVER ===")
        print(f"Connected: {client.server_info.name if client.server_info else 'unknown'}")

        print("\n=== DISCOVERY ===")
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        print("Tools:", [tool.name for tool in tools])
        print("Resources:", [str(resource.uri) for resource in resources])
        print("Prompts:", [prompt.name for prompt in prompts])
        print("Advertised client root: project data/ directory")

        print("\n=== TOOL INVOCATION ===")
        search_result = await client.call_tool(
            "search_tickets",
            {"query": "vpn", "status": "open"},
            meta={"demo_step": "tool_invocation"},
        )
        print(_display(search_result.data))

        print("\n=== RESOURCE INVOCATION ===")
        resource_result = await client.read_resource(
            "helpdesk://knowledge/vpn-troubleshooting"
        )
        print(resource_result[0].text)

        print("\n=== PROMPT INVOCATION ===")
        prompt_result = await client.get_prompt(
            "triage_ticket",
            {"ticket_id": "TKT-102"},
        )
        for message in prompt_result.messages:
            text = getattr(message.content, "text", str(message.content))
            print(f"{message.role}: {text}")

        print("\n=== EXPECTED ERROR HANDLING ===")
        try:
            await client.call_tool("get_ticket", {"ticket_id": "INVALID"})
        except ToolError as exc:
            print(f"Safe client error: {exc}")
