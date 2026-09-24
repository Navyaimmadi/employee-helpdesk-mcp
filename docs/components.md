# MCP Components

## Tools

| Tool | Input | Purpose |
|---|---|---|
| `search_tickets` | `query`, optional `status` | Searches ticket ID, title, description, category, and assignee. |
| `get_ticket` | `ticket_id` | Returns one ticket after validating the `TKT-###` format. |
| `analyze_queue` | None | Counts tickets by status and priority. |
| `read_knowledge_file` | `relative_path` | Reads only Markdown files inside the approved knowledge root. |

## Resources

| URI | Content |
|---|---|
| `helpdesk://knowledge/password-reset` | Approved employee password-reset procedure. |
| `helpdesk://knowledge/vpn-troubleshooting` | Approved VPN troubleshooting procedure. |
| `helpdesk://queue/summary` | Aggregate queue statistics without sensitive employee fields. |

## Prompt

`triage_ticket(ticket_id)` produces a reusable instruction that asks the client to retrieve the ticket, consult an appropriate resource, determine urgency and category, recommend a safe next step, and cite the resource URI without inventing facts or taking write actions.
