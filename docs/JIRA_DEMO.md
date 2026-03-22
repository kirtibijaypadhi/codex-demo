# Jira Ticket Demo

Use this file when teaching how Codex can turn a Jira ticket into implementation work.

## Demo Goal

Show that once Jira is connected through MCP, Codex can:

1. read the ticket directly
2. explain the requirement back to the user
3. identify likely files to change
4. implement the change
5. verify the result

## Recommended Live Demo Flow

### 1. Show the MCP connection

Open `.codex/config.toml` and point out the `jira_project` server entry.

Explain:
- Jira is not pasted into chat manually
- Codex can use MCP to fetch structured issue data
- access should be scoped to the right project and permissions

### 2. Show the repo instructions

Open `AGENTS.md`.

Explain:
- the repo tells Codex how to behave when a Jira ticket is mentioned
- the workflow is fetch, explain, map to code, implement, verify

### 3. Run the prompt

Use a prompt like:

```text
Implement PROJ-123 using the Jira MCP server. First summarize the ticket, acceptance criteria, and affected files. Then make the smallest correct implementation and run quick verification.
```

### 4. Narrate what Codex is doing

Call out the stages:
- reading the ticket via MCP
- grounding implementation in actual acceptance criteria
- changing only the relevant files
- validating the result

## Teaching Point

The most important lesson is not "Codex can code from Jira."

The important lesson is:

- rules can govern risky actions
- MCP can supply structured context
- repo instructions can standardize workflow
- Git can keep the results reviewable

## If You Want a Slash-Command Feel

This repo includes `scripts/implement-ticket.sh`.

It does not create a native Codex slash command. Instead, it prints a polished prompt template so you can run:

```bash
./scripts/implement-ticket.sh PROJ-123
```

Then paste the output into Codex.

That gives a nice `/implement PROJ-123` style demo without depending on undocumented client features.
