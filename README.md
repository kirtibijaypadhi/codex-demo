# codex-mcp-demo

A lightweight PHP project for demonstrating AI coding assistant capabilities, with a focus on:
- Rules engine behavior (`allow`, `prompt`, `forbidden`)
- MCP (Model Context Protocol) integrations for tool-backed workflows

## Demo Goal

Show how an AI assistant can:
1. Understand and modify a small PHP codebase.
2. Follow policy constraints from `.codex/rules/default.rules`.
3. Interact with mock MCP servers configured in `.codex/config.toml`.
4. Execute a repeatable review workflow from `.codex/SKILLS.md`.

**Deep dive (concepts + Q&A prep):** see [`docs/THEORY.md`](docs/THEORY.md).

## Project Structure

```text
codex-mcp-demo/
├── README.md
├── docs/
│   └── THEORY.md
├── composer.json
├── Makefile
├── scripts/
│   └── demo.sh
├── src/
│   └── index.php
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

## Demo Script (Step-by-Step)

### 1) Introduce the baseline app
- Open `src/index.php`.
- Explain that it is intentionally small so the audience can follow every AI-generated change.
- Run the two `curl` examples to show current behavior.

### 2) Show rules engine controls
- Open `.codex/rules/default.rules`.
- Highlight the three actions:
  - `allow` for safe git read commands (`git status`, `git diff`, `git log`)
  - `prompt` for package management (`composer update`, etc.)
  - `forbidden` for destructive commands (`rm -rf`, `DROP DATABASE`)
- Explain that policy can shape assistant behavior without changing model prompts.

### 3) Show MCP server configuration
- Open `.codex/config.toml`.
- Point out:
  - `sqlite_local` as a mock STDIO server for local data access
  - `internal_api_docs` as a mock Streamable HTTP endpoint
- Explain that MCP gives the assistant structured access to external tools and knowledge sources.

### 4) Show repeatable workflow skill
- Open `.codex/SKILLS.md`.
- Walk through "Pre-Commit Code Review":
  - Security checks first
  - Style/quality checks second
  - Severity-based commit decision
- Emphasize consistency and auditability across team usage.

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

## Suggested Presenter Notes

- Keep each segment under 2-3 minutes.
- Verbally contrast "prompt engineering" vs "policy and tooling integration."
- End with a takeaway: the assistant is more reliable when constrained by rules and augmented with MCP tools.
