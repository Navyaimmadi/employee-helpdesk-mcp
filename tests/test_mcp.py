"""Integration tests using an in-memory FastMCP client transport."""

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from helpdesk_mcp.server import mcp


@pytest.fixture
async def mcp_client():
    async with Client(mcp) as client:
        yield client


async def test_discovers_required_components(mcp_client: Client):
    tools = await mcp_client.list_tools()
    resources = await mcp_client.list_resources()
    prompts = await mcp_client.list_prompts()
    assert {tool.name for tool in tools} >= {
        "search_tickets",
        "get_ticket",
        "analyze_queue",
    }
    assert len(resources) >= 2
    assert {prompt.name for prompt in prompts} >= {"triage_ticket"}


async def test_invokes_tool_resource_and_prompt(mcp_client: Client):
    tool_result = await mcp_client.call_tool("get_ticket", {"ticket_id": "TKT-102"})
    assert tool_result.data["id"] == "TKT-102"

    resource_result = await mcp_client.read_resource(
        "helpdesk://knowledge/vpn-troubleshooting"
    )
    assert "VPN Troubleshooting" in resource_result[0].text

    prompt_result = await mcp_client.get_prompt(
        "triage_ticket", {"ticket_id": "TKT-102"}
    )
    assert "TKT-102" in prompt_result.messages[0].content.text


async def test_invalid_ticket_returns_safe_error(mcp_client: Client):
    with pytest.raises(ToolError, match="format TKT-###"):
        await mcp_client.call_tool("get_ticket", {"ticket_id": "bad"})


async def test_path_traversal_is_blocked(mcp_client: Client):
    with pytest.raises(ToolError, match="outside the allowed knowledge root"):
        await mcp_client.call_tool(
            "read_knowledge_file", {"relative_path": "../tickets.json.md"}
        )

