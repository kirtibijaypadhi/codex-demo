# Codex Demo Runbook

Use this runbook to present a complete demo of Codex with:
- a real codebase
- rules
- MCP integrations
- Git-aware summaries
- Jira-driven implementation workflow

---

## Demo Goal

Show that Codex becomes much more useful when it is:

- grounded in a real repo
- constrained by explicit rules
- connected to external tools through MCP
- guided by repo-level workflow instructions

**Core idea:** this is not just "AI writes code." This is **governed, tool-connected software development**.

---

## Repo Overview

Key files in this repo:

- `src/index.php`  
  Tiny PHP API for live code walkthroughs and small edits.

- `.codex/rules/default.rules`  
  Mock rules engine policy showing `allow`, `prompt`, and `forbidden`.

- `.codex/config.toml`  
  MCP configuration for:
  - local Git summary MCP
  - Jira MCP template
  - mock internal docs MCP
  - mock SQLite MCP

- `.codex/SKILLS.md`  
  Repeatable pre-commit review workflow.

- `AGENTS.md`  
  Repo-level instructions for how Codex should behave when implementing Jira tickets.

- `tools/git_mcp_server.py`  
  Local MCP server for Git-aware push summaries.

- `tools/git_summary.py`  
  Summary generator used by the MCP workflow and Git hook.

- `.githooks/pre-push`  
  Advisory hook that refreshes the Git summary during push.

- `docs/JIRA_DEMO.md`  
  Presenter notes for Jira workflow.

- `docs/THEORY.md`  
  Deeper theory and Q&A prep.

- `docs/push-summaries/latest.md`  
  Generated Git push summary artifact.

---

## What This Demo Teaches

This repo demonstrates four layers working together:

| Layer | Purpose | In This Repo |
|------|---------|--------------|
| Code | Something real for Codex to inspect and modify | `src/index.php` |
| Rules | Guardrails around risky actions | `.codex/rules/default.rules` |
| MCP | Structured access to external tools and data | `.codex/config.toml` |
| Workflow | Standardized behavior and review process | `AGENTS.md`, `.codex/SKILLS.md` |

You can explain it like this:

> Codex is strongest when it does not work from chat alone.  
> It works better when it can read real code, follow rules, use tools through MCP, and behave consistently through repo instructions.

---

## Pre-Demo Setup

Run everything from the repo root.

### 1. Verify the codebase

```bash
make check
```

### 2. Install the advisory Git hook

```bash
make install-hooks
```

### 3. Refresh the Git summary artifact

```bash
make refresh-summary
```

### 4. Start the PHP app

```bash
./scripts/demo.sh
```

### 5. Verify the app in another terminal

```bash
curl "http://localhost:8080/index.php"
curl "http://localhost:8080/index.php?user_id=2"
```

---

## Optional Jira Setup

If you want the Jira part of the demo to be real instead of conceptual:

1. Open `.codex/config.toml`
2. Find the `jira_project` server entry
3. Replace the placeholder token
4. Set:

```toml
enabled = true
```

### Important note

If Jira is not connected yet, you can still demo the workflow honestly by showing:
- the Jira MCP config template
- `AGENTS.md`
- the generated helper prompt from `make implement-ticket TICKET=PROJ-123`

---

## Recommended Demo Order

---

## 1. Show the Small Codebase

Open:

```text
src/index.php
```

### What to say

- This project is intentionally tiny.
- The audience can follow every change Codex makes.
- A small codebase makes the workflow easier to understand.

### Show live

- endpoint returns JSON
- optional `user_id` lookup
- validation via `filter_input`
- 404 behavior for unknown user

### Example prompt

```text
Review src/index.php for security and style issues using the Pre-Commit Code Review skill in .codex/SKILLS.md, then propose minimal fixes.
```

---

## 2. Show the Rules Engine

Open:

```text
.codex/rules/default.rules
```

### What to point out

- `allow` for safe Git read commands
- `prompt` for Composer package operations
- `prompt` for `git push`
- `forbidden` for destructive commands

### What to say

- prompts influence behavior
- rules enforce boundaries
- rules are better for consistent safety and governance

### Good explanation line

> Prompts steer behavior. Rules define boundaries.

### Example prompt

```text
I want to run composer update for this project. Based on .codex/rules/default.rules, what should happen and why?
```

---

## 3. Show MCP Configuration

Open:

```text
.codex/config.toml
```

### What to point out

- `sqlite_local`  
  mock local STDIO tool

- `git_summary_local`  
  real local Git-focused MCP workflow

- `jira_project`  
  Jira MCP template for ticket-driven implementation

- `internal_api_docs`  
  mock remote HTTP MCP endpoint

### What to say

- MCP lets Codex use structured tools and systems
- this is better than expecting the model to guess
- local tools and remote services can both be exposed through MCP

### Good explanation line

> MCP gives Codex structured access to tools, not just more text.

### Example prompt

```text
Use the MCP configuration in .codex/config.toml to explain which server you would use for local Git summaries and which one you would use for Jira ticket data.
```

---

## 4. Show Repo Workflow Instructions

Open:

```text
AGENTS.md
```

### What to point out

This file tells Codex how to behave when a Jira ticket is mentioned.

Workflow in `AGENTS.md`:

1. Read the ticket through Jira MCP
2. Summarize the requirement
3. Extract acceptance criteria
4. Map the change to local files
5. Implement minimally
6. Run lightweight verification
7. Report what changed and what still needs confirmation

### What to say

- MCP gives access to Jira
- `AGENTS.md` defines the repo's working style
- this makes behavior more consistent across users

### Good explanation line

> MCP provides the data, and `AGENTS.md` provides the behavior.

---

## 5. Show Git-Aware MCP Workflow

Open:

```text
tools/git_mcp_server.py
tools/git_summary.py
```

Then run:

```bash
make refresh-summary
```

Open:

```text
docs/push-summaries/latest.md
```

### What to point out

- the summary includes push context
- commits in the push
- changed files
- diff stat
- diff excerpt

### What to say

- Git already knows what is changing
- Codex can use MCP-style tooling to turn that into a readable artifact
- this is useful for code review, changelog generation, and developer awareness

### Good explanation line

> Git provides the facts, MCP tooling turns those facts into a reviewable artifact.

### Example prompt

```text
Use the git_summary_local MCP server to explain what the next push contains and whether I should refresh docs/push-summaries/latest.md.
```

---

## 6. Show Jira-Driven Implementation

Open:

```text
docs/JIRA_DEMO.md
```

Then run:

```bash
make implement-ticket TICKET=PROJ-123
```

That prints a ready-to-paste prompt.

### Example prompt

```text
Implement PROJ-123 using the Jira MCP server configured for this repo. First summarize the ticket, acceptance criteria, and likely files to change. Then make the smallest correct implementation and run quick verification.
```

### What to say

- the ticket ID is not the magic part
- the real value is that Codex reads the ticket through Jira MCP
- then it explains requirements before touching code
- then it changes only relevant files

### Good explanation line

> The magic is not `/implement`. The magic is grounded tool use plus a repeatable workflow.

---

## Suggested Live Prompt Set

Use these prompts during the demo.

### Prompt 1: Code Review

```text
Review src/index.php for security and style issues using the Pre-Commit Code Review skill in .codex/SKILLS.md, then propose minimal fixes.
```

### Prompt 2: Rules

```text
I want to run composer update for this project. Based on .codex/rules/default.rules, what should happen and why?
```

### Prompt 3: MCP Explanation

```text
Use the MCP configuration in .codex/config.toml to explain which server you would use for local Git summaries and which one you would use for Jira ticket data.
```

### Prompt 4: Git Summary

```text
Use the git_summary_local MCP server to explain what the next push contains and whether I should refresh docs/push-summaries/latest.md.
```

### Prompt 5: Jira Implementation

```text
Implement PROJ-123 using the Jira MCP server configured for this repo. First summarize the ticket, acceptance criteria, and likely files to change. Then make the smallest correct implementation and run quick verification.
```

---

## Demo Talking Points

### When showing the code

- Codex is working against a real codebase, not an abstract example.
- Small repos are ideal for learning.

### When showing rules

- Rules are about governance, not just convenience.
- High-impact actions should be explicitly reviewed.

### When showing MCP

- MCP is how Codex gets structured access to external context.
- This avoids relying only on chat history or pasted text.

### When showing AGENTS.md

- This file standardizes how Codex works in this repo.
- It makes the workflow teachable and repeatable.

### When showing Git summary

- This is a good example of local, practical MCP use.
- It turns repo state into a visible artifact.

### When showing Jira

- The goal is not "AI magically codes from a ticket."
- The goal is "Codex reads the real ticket, explains it, maps it to the codebase, and implements carefully."

---

## Best Commands To Use During The Demo

```bash
make check
./scripts/demo.sh
make install-hooks
make refresh-summary
make implement-ticket TICKET=PROJ-123
git status
git diff
```

---

## If Jira Is Not Connected

You can still present the workflow.

### Show:

- `AGENTS.md`
- `.codex/config.toml`
- `docs/JIRA_DEMO.md`

### Then run:

```bash
make implement-ticket TICKET=PROJ-123
```

### What to say

- once the Jira MCP credentials are configured
- and `jira_project` is enabled
- the same prompt becomes a real implementation workflow

### Honest phrasing

> Right now this is wired as a template. Once Jira MCP is connected, Codex can fetch the ticket directly instead of relying on pasted issue text.

---

## What Not To Overcomplicate

Avoid saying:

- Codex just automatically knows everything
- slash commands are the important part
- hooks should rewrite pushes
- MCP is only for remote APIs

Prefer saying:

- Codex is strongest when grounded
- rules improve safety
- MCP improves context
- repo instructions improve consistency
- visible workflows are easier to trust and teach

---

## Troubleshooting

### If the PHP app does not start

Run:

```bash
php -v
make check
```

### If the Git summary looks stale

Run:

```bash
make refresh-summary
```

### If the hook is annoying

It is advisory only now.  
Pushes should continue even if the summary file changes.

### If Jira implementation does not work

Check:
- Jira token in `.codex/config.toml`
- `jira_project` is enabled
- Codex client has MCP enabled
- your ticket ID is valid

---

## 30-Second Opening

> This repo is a teaching demo for how Codex works best in a real engineering workflow. We have a small codebase, explicit rules for risky actions, MCP servers for structured tool access, and repo instructions that standardize how Codex behaves. The result is not just code generation. It is governed, tool-connected software development.

---

## 30-Second Closing

> The takeaway is that Codex is most useful when it is grounded. It should read real code, follow explicit rules, use external tools through MCP, and operate within a clear workflow. That is how you make AI coding assistants more reliable, reviewable, and teachable for a team.

---

## Optional 5-Minute Demo Flow

### Minute 1

Show `src/index.php` and the running API.

### Minute 2

Show `.codex/rules/default.rules`.

### Minute 3

Show `.codex/config.toml` and explain MCP.

### Minute 4

Show `AGENTS.md` and `make refresh-summary`.

### Minute 5

Show `make implement-ticket TICKET=PROJ-123` and explain the Jira workflow.

---

## Appendix: Quick Commands

### Start app

```bash
./scripts/demo.sh
```

### Verify app

```bash
curl "http://localhost:8080/index.php"
curl "http://localhost:8080/index.php?user_id=2"
```

### Verify code

```bash
make check
```

### Install hooks

```bash
make install-hooks
```

### Refresh Git summary

```bash
make refresh-summary
```

### Generate ticket implementation prompt

```bash
make implement-ticket TICKET=PROJ-123
```

---
