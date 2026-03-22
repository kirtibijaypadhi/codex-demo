# AGENTS.md

This repository is a teaching demo for Codex, rules, MCP, and Git-aware workflows.

## Primary Goal

When a user asks to implement a Jira ticket such as `PROJ-123`, follow this workflow:

1. Use the Jira MCP server configured in `.codex/config.toml` to fetch the issue details.
2. Summarize the ticket in plain English:
   - title
   - business goal
   - acceptance criteria
   - risks or missing information
3. Map the ticket to the local codebase before changing anything:
   - identify likely files
   - explain why those files are relevant
   - state assumptions if the ticket is underspecified
4. Implement the smallest correct change that satisfies the ticket.
5. Run lightweight verification:
   - syntax checks
   - relevant tests if they exist
   - a short summary of what was validated
6. Report back with:
   - what the ticket required
   - what changed
   - what still needs confirmation

## Jira Ticket Behavior

If a ticket is mentioned, prefer this sequence:

1. Read the Jira issue through MCP first.
2. Do not guess requirements when the ticket can answer them.
3. If the ticket is ambiguous, call that out explicitly before coding.
4. Keep the implementation minimal and traceable to the acceptance criteria.

## Repo-Specific Teaching Notes

- This repo is intentionally small and demo-friendly.
- Favor edits that juniors can understand quickly.
- Prefer visible workflows over hidden automation.
- When working with Git summaries, use the local `git_summary_local` MCP server or the repo hook flow.

## Example Prompt Style

Good prompts for this repo:

- `Implement PROJ-123 using the Jira MCP server. Start by summarizing the ticket, then make the smallest code change that satisfies it.`
- `Read PROJ-123 from Jira, explain the acceptance criteria, and tell me which files you expect to change before editing anything.`

## Constraints

- Do not fabricate Jira fields that were not returned by the MCP server.
- Do not claim a ticket is complete if acceptance criteria were not addressed.
- If Jira access is unavailable, say so clearly and fall back to asking the user for the ticket text.
