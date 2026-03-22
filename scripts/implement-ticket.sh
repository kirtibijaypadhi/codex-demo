#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: ./scripts/implement-ticket.sh <TICKET-ID>"
  exit 1
fi

ticket_id="$1"

cat <<EOF
Implement ${ticket_id} using the Jira MCP server configured for this repo.

Workflow:
1. Read the ticket from Jira first.
2. Summarize the requirement, acceptance criteria, and any open questions.
3. Identify the files you expect to change and why.
4. Implement the smallest correct change that satisfies the ticket.
5. Run quick verification and report what you checked.

If Jira access is unavailable, say that clearly before proceeding.
EOF
