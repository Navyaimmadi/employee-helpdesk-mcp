---
name: complete-employee-helpdesk-mcp-lab
description: Test, document, and finish the Module 4 production MCP server and client lab in this repository.
---

# Employee Help Desk MCP Lab Skill

## Working rules

1. Read `README.md` and every file under `docs/` before editing.
2. Treat the assignment requirements summarized in the README as authoritative.
3. Keep the Employee Help Desk scenario and stdio transport unless the user explicitly requests a change.
4. Use FastMCP 4 APIs that match the pinned range in `pyproject.toml`.
5. Do not add an LLM API, model key, SharedLLM dependency, database, or remote service; none is required for this lab.
6. Preserve client-side root scoping and the server's independent path validation.
7. Never print application logs to stdout in the stdio server; stdout is reserved for MCP protocol traffic.
8. Never invent demonstration output. Capture it from a real successful client run.
9. Make small changes and rerun the relevant test after each change.
10. Do not commit `.venv`, caches, secrets, or unrelated files.

## Completion workflow

1. Run `uv sync --extra dev`.
2. Run `uv run pytest` and fix any failures.
3. Run `uv run python client.py`.
4. Save the exact client output to `samples/demo-session.txt`.
5. Confirm discovery lists at least three tools, two resources, and one prompt.
6. Confirm the client successfully invokes a tool, reads a resource, and renders a prompt.
7. Confirm the invalid-ticket demonstration returns a safe error without a stack trace or local path.
8. Review the Mermaid diagram against the implementation.
9. Review `docs/components.md` and `docs/security.md` against the final code.
10. Check every README requirement row and report anything incomplete.
11. Review `git status` for secrets, caches, or accidental files.
12. Commit and push to a new public GitHub repository only after all checks pass.

## Definition of done

The project is complete when tests pass, the local stdio demo succeeds, a genuine demo log is committed, all tools/resources/prompts are documented, client-side root scoping remains visible, safe error handling is demonstrated, and the public repository contains every deliverable in the brief.
