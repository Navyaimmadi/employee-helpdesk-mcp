"""Run the discovery-and-invocation demonstration client."""

import asyncio

from helpdesk_mcp.client import run_demo


if __name__ == "__main__":
    asyncio.run(run_demo())

