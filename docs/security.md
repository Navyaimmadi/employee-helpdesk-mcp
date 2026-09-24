# Security Design Summary

## Authentication

The local stdio client launches the server as a subprocess, so the operating-system user and filesystem permissions form the authentication boundary for this demonstration. There is no network listener. A remote Streamable HTTP deployment would require TLS and OAuth bearer-token validation; anonymous access would be rejected.

## Least privilege

- The server exposes read-only help-desk operations; it cannot close, delete, or modify tickets.
- The client advertises only the project `data/` directory as its MCP root.
- The file tool independently resolves every requested path and rejects traversal outside `data/knowledge/`.
- Only Markdown knowledge files are readable through the file tool.
- Tool results contain sample operational data and omit credentials or employee secrets.

## Error handling

Expected failures, such as malformed ticket IDs, unknown tickets, invalid status values, missing files, and path traversal, return short actionable `ToolError` messages. Unexpected exceptions are logged on stderr with diagnostic detail, while the client receives only a generic failure message. This prevents stack traces, host paths, and backing-store details from leaking through the MCP result.

## Observability

Each tool records its name, outcome, and elapsed time. Logs go to stderr because stdout is reserved for stdio MCP protocol messages. Production telemetry should add request IDs, authenticated subject identifiers, rate-limit events, and centralized retention controls while excluding ticket descriptions and secrets.

