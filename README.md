# codex-mcp-demo

A lightweight PHP project for demonstrating AI coding assistant capabilities, with a focus on:
- Rules engine behavior (`allow`, `prompt`, `forbidden`)
- MCP (Model Context Protocol) integrations for tool-backed workflows
- Git-aware MCP automation for visible, reviewable push summaries
- Jira-driven implementation workflows using MCP and repo instructions

## Demo Goal

Show how an AI assistant can:
1. Understand and modify a small PHP codebase.
2. Follow policy constraints from `.codex/rules/default.rules`.
3. Interact with mock MCP servers configured in `.codex/config.toml`.
4. Execute a repeatable review workflow from `.codex/SKILLS.md`.
5. Generate Git push summaries through a local MCP server and a repo-local hook.
6. Turn a Jira ticket into a grounded implementation workflow using MCP plus `AGENTS.md`.

**Deep dive (concepts + Q&A prep):** see [`docs/THEORY.md`](docs/THEORY.md).

## Project Structure

```text
codex-mcp-demo/
├── README.md
├── AGENTS.md
├── docs/
│   ├── JIRA_DEMO.md
│   └── THEORY.md
├── composer.json
├── Makefile
├── .githooks/
│   └── pre-push
├── scripts/
│   ├── demo.sh
│   ├── implement-ticket.sh
│   └── install-hooks.sh
├── src/
│   └── index.php
├── tools/
│   ├── git_mcp_server.py
│   └── git_summary.py
└── .codex/
    ├── SKILLS.md
    ├── config.toml
    └── rules/
        └── default.rules
```

## Quick Start

### Option A — one command (recommended for demos)

Pick any of these; they all start the same PHP dev server on `localhost:8080`:

```bash
./scripts/demo.sh
# or
make demo
# or
composer run demo
```

Optional: use a different host/port (shell script only):

```bash
HOST=127.0.0.1 PORT=9090 ./scripts/demo.sh
```

### Option B — manual

```bash
php -S localhost:8080 -t src
```

### Verify before presenting

```bash
composer run demo:check   # PHP version + syntax check
# or
make check
```

### Install the Git summary demo hook

```bash
make install-hooks
```

This activates the repo-local `.githooks/pre-push` hook. On `git push`, it refreshes `docs/push-summaries/latest.md` and intentionally blocks the push if the summary changed, so you can review and commit it first.
This activates the repo-local `.githooks/pre-push` hook. On `git push`, it refreshes `docs/push-summaries/latest.md` and prints an advisory message if the file changed. It does not block the push.

### Test the API

With the server running in another terminal:

```bash
curl "http://localhost:8080/index.php"
curl "http://localhost:8080/index.php?user_id=2"
# optional smoke test (requires server running):
make curl
```

### Composer (optional)

There are no runtime Composer packages; `composer.json` exists so `composer update` / `composer require` are meaningful when demonstrating the **prompt** rule in `.codex/rules/default.rules`. If you use Composer locally:

```bash
composer install   # creates vendor/ (gitignored) if you add dependencies later
```

## Jira MCP Demo Flow

This repo now also supports a Jira-ticket implementation teaching flow.

The pieces are:
- `AGENTS.md` to tell Codex how to behave when a Jira ticket is mentioned
- `.codex/config.toml` with a `jira_project` MCP server template
- `scripts/implement-ticket.sh` to print a polished ticket-implementation prompt

### Why this is useful for teaching

It lets you show that Codex should not invent requirements from a ticket number alone.

The intended flow is:
- connect Jira through MCP
- ask Codex to read the ticket first
- summarize requirements and acceptance criteria
- map the work to local files
- implement the change
- verify the result

### Prompt examples

```text
Implement PROJ-123 using the Jira MCP server. First summarize the ticket, acceptance criteria, and affected files. Then make the smallest correct implementation and run quick verification.
```

```bash
make implement-ticket TICKET=PROJ-123
```

That helper script prints a ready-to-paste prompt so you can simulate a lightweight `/implement PROJ-123` style workflow.

## Git MCP Demo Flow

This repo includes a local STDIO MCP server at `tools/git_mcp_server.py`.

It exposes two demo tools:
- `summarize_push` to turn a Git pre-push ref line into a Markdown summary
- `write_push_summary` to save that summary into `docs/push-summaries/latest.md`

### Why this flow is good for teaching

Instead of silently changing a push behind the user’s back, the demo makes the automation visible:
- Git decides what is about to be pushed
- MCP-style tooling summarizes it
- The summary becomes a real file in the repo
- The hook can refresh the file during push, or you can refresh it explicitly before push

That gives juniors a much clearer mental model of **tooling + policy + human approval**.

### Manual demo command

You can generate a summary without pushing by passing a sample pre-push line:

```bash
make push-summary PUSH_LINE="refs/heads/main $(git rev-parse HEAD) refs/heads/main 0000000000000000000000000000000000000000"
```

Or refresh the summary against your current `origin/main` before pushing:

```bash
make refresh-summary
```

## Demo Script (Step-by-Step)

### 1) Introduce the baseline app
- Open `src/index.php`.
- Explain that it is intentionally small so the audience can follow every AI-generated change.
- Run the two `curl` examples to show current behavior.

### 2) Show rules engine controls
- Open `.codex/rules/default.rules`.
- Highlight the four actions:
  - `allow` for safe git read commands (`git status`, `git diff`, `git log`)
  - `prompt` for package management (`composer update`, etc.)
  - `prompt` for `git push`, because publishing changes deserves explicit review
  - `forbidden` for destructive commands (`rm -rf`, `DROP DATABASE`)
- Explain that policy can shape assistant behavior without changing model prompts.

### 3) Show MCP server configuration
- Open `.codex/config.toml`.
- Point out:
  - `sqlite_local` as a mock STDIO server for local data access
  - `git_summary_local` as a real local STDIO server for Git-aware summaries
  - `jira_project` as a Jira MCP template for ticket-driven implementation
  - `internal_api_docs` as a mock Streamable HTTP endpoint
- Explain that MCP gives the assistant structured access to external tools and knowledge sources.

### 3.5) Show Git-aware automation
- Open `tools/git_mcp_server.py` and `tools/git_summary.py`.
- Explain that the MCP server can inspect Git context and write a Markdown summary file.
- Run `make install-hooks`.
- Show `.githooks/pre-push` and explain that it refreshes the summary during push without blocking delivery.
- Run `make refresh-summary` to show the explicit workflow.
- Explain that the hook is advisory only, so the summary demo is visible without interrupting delivery.

### 4) Show repeatable workflow skill
- Open `.codex/SKILLS.md`.
- Walk through "Pre-Commit Code Review":
  - Security checks first
  - Style/quality checks second
  - Severity-based commit decision
- Emphasize consistency and auditability across team usage.

### 4.5) Show repo-level Jira workflow instructions
- Open `AGENTS.md`.
- Explain that this is where you teach Codex how to behave for `Implement PROJ-123` style requests.
- Highlight the sequence: fetch ticket, explain requirements, map to files, implement, verify.
- Open `docs/JIRA_DEMO.md` for the presenter script.

### 5) Run live prompts in the IDE
- Paste one prompt at a time (examples below).
- Narrate how the assistant references code, follows rules, and (when available) uses MCP tools.

## Explaining the Rules File

The rules file is a mock Starlark-style policy that demonstrates command governance:
- **Allow rule**: permits low-risk inspection commands so routine development is frictionless.
- **Prompt rule**: inserts human approval for dependency changes that can affect lockfiles and runtime behavior.
- **Forbidden rule**: blocks irreversible or dangerous operations that should never be automated blindly.

## Explaining the MCP Configuration

The MCP config demonstrates two integration patterns:
- **STDIO server** (`sqlite_local`): local process tool adapter, useful for scripts, databases, and offline utilities.
- **Streamable HTTP server** (`internal_api_docs`): remote service integration, useful for internal docs, APIs, and platform tools.

In a real environment, replace demo endpoints, commands, and tokens with production-safe values.

## Copy/Paste Prompts for Live Demo

1. **PHP code interaction**
   > Review `src/index.php` for security and style issues using the "Pre-Commit Code Review" skill in `.codex/SKILLS.md`, then propose minimal fixes.

2. **Rules engine behavior**
   > I want to run `composer update` for this project. Based on `.codex/rules/default.rules`, what should happen and why?

3. **MCP usage scenario**
   > Use the MCP configuration in `.codex/config.toml` to explain which server you would query to fetch API reference data for this PHP endpoint and which one you would use to inspect local SQLite records.

4. **Git summary automation**
   > Use the `git_summary_local` MCP server to generate a summary of what my next push would contain, write it to `docs/push-summaries/latest.md`, and explain whether I should commit it before pushing.

5. **Jira-driven implementation**
   > Implement PROJ-123 using the Jira MCP server configured for this repo. First summarize the ticket, acceptance criteria, and likely files to change. Then make the smallest correct implementation and run quick verification.

## Suggested Presenter Notes

- Keep each segment under 2-3 minutes.
- Verbally contrast "prompt engineering" vs "policy and tooling integration."
- End with a takeaway: the assistant is more reliable when constrained by rules and augmented with MCP tools.
