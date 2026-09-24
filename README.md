# Employee Help Desk MCP Server and Client

This Module 4 lab turns a small internal support-ticket queue and knowledge base into a local Model Context Protocol service. It includes a FastMCP server, a stdio client, client-side root scoping, safe errors, documentation, tests, and a reproducible demo.

## Requirements coverage

| Lab requirement | Implementation |
|---|---|
| At least 3 tools | Four tools in `src/helpdesk_mcp/server.py` |
| At least 2 URI resources | Three `helpdesk://` resources |
| At least 1 prompt | `triage_ticket` prompt |
| Discover and invoke each type | `src/helpdesk_mcp/client.py` |
| Transport and justification | stdio; see `docs/architecture.md` |
| Client-side safety | Client advertises only the project `data/` root |
| Security summary | `docs/security.md` |
| Realistic error handling | Invalid input, missing records, unavailable data, and blocked path traversal |

## Project structure

```text
employee-helpdesk-mcp/
├── client.py
├── server.py
├── data/
│   ├── tickets.json
│   └── knowledge/
├── docs/
│   ├── architecture.md
│   ├── components.md
│   └── security.md
├── samples/
├── src/helpdesk_mcp/
├── tests/
├── pyproject.toml
└── SKILL.md
```

## Setup

Install `uv` if it is not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then open this project folder in Terminal:

```bash
uv sync --extra dev
uv run pytest
uv run python client.py
```

The client launches the server automatically over stdio; no external service is required. A verified run is included in `samples/demo-session.txt`; rerun it after any code change.

## Documentation

- [Architecture and transport choice](docs/architecture.md)
- [Tools, resources, and prompt](docs/components.md)
- [Security design summary](docs/security.md)
- [Demonstration evidence instructions](samples/README.md)

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP documentation](https://gofastmcp.com/)


