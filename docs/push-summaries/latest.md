# Push Summary

Generated: 2026-03-22 17:50:22 UTC

## Push Context

- Local ref: `refs/heads/main`
- Local sha: `fff61a4d7fbc4d2c3cb6b2b4f2252bfbd025f17e`
- Remote ref: `refs/heads/main`
- Remote sha: `d961a63dc7d4f62d6b166cbe0f7a6e54d47849c3`

## Commits In This Push

- fff61a4 add git and jira MCP demo workflow

## Files Changed

- `.codex/config.toml`
- `.codex/rules/default.rules`
- `.githooks/pre-push`
- `.gitignore`
- `AGENTS.md`
- `Makefile`
- `README.md`
- `docs/JIRA_DEMO.md`
- `docs/THEORY.md`
- `docs/push-summaries/README.md`
- `docs/push-summaries/latest.md`
- `scripts/implement-ticket.sh`
- `scripts/install-hooks.sh`
- `tools/git_mcp_server.py`
- `tools/git_summary.py`

## Diff Stat

```text
.codex/config.toml            |  16 ++++
 .codex/rules/default.rules    |  10 ++-
 .githooks/pre-push            |  28 ++++++
 .gitignore                    |   3 +
 AGENTS.md                     |  56 ++++++++++++
 Makefile                      |  13 ++-
 README.md                     | 106 ++++++++++++++++++++++-
 docs/JIRA_DEMO.md             |  73 ++++++++++++++++
 docs/THEORY.md                | 109 +++++++++++++++++++++++-
 docs/push-summaries/README.md |   5 ++
 docs/push-summaries/latest.md | 168 ++++++++++++++++++++++++++++++++++++
 scripts/implement-ticket.sh   |  22 +++++
 scripts/install-hooks.sh      |  10 +++
 tools/git_mcp_server.py       | 135 +++++++++++++++++++++++++++++
 tools/git_summary.py          | 194 ++++++++++++++++++++++++++++++++++++++++++
 15 files changed, 941 insertions(+), 7 deletions(-)
```

## Diff Excerpt

```diff
diff --git a/.codex/config.toml b/.codex/config.toml
index c261036..c6650dc 100644
--- a/.codex/config.toml
+++ b/.codex/config.toml
@@ -18,2 +18,18 @@ enabled = true
 
+# Local Git-focused MCP server for push summaries.
+[mcp.servers.git_summary_local]
+type = "stdio"
+command = "python3"
+args = ["tools/git_mcp_server.py"]
+working_dir = "."
+enabled = true
+
+# Jira MCP template for ticket-driven implementation demos.
+# Replace the placeholder token and project guidance with your real setup.
+[mcp.servers.jira_project]
+type = "streamable_http"
+url = "https://mcp.atlassian.com/v1/mcp"
+headers = { "Authorization" = "Bearer ATLASSIAN_API_TOKEN", "X-Demo-Client" = "codex-mcp-demo" }
+enabled = false
+
 # Dummy Streamable HTTP MCP server (e.g., internal API docs service).
diff --git a/.codex/rules/default.rules b/.codex/rules/default.rules
index 9a16ae4..4a9302d 100644
--- a/.codex/rules/default.rules
+++ b/.codex/rules/default.rules
@@ -20,3 +20,11 @@ rules = [
 
-    # 3) Forbidden: block clearly dangerous shell/database commands.
+    # 3) Prompt: treat pushes as high-impact actions that deserve review.
+    rule(
+        name = "prompt-git-push",
+        action = "prompt",
+        match = command_matches(r"^git push( .*)?$"),
+        reason = "Pushing publishes changes and should be reviewed explicitly.",
+    ),
+
+    # 4) Forbidden: block clearly dangerous shell/database commands.
     rule(
diff --git a/.githooks/pre-push b/.githooks/pre-push
new file mode 100755
index 0000000..5eff814
--- /dev/null
+++ b/.githooks/pre-push
@@ -0,0 +1,28 @@
+#!/usr/bin/env bash
+set -euo pipefail
+
+ROOT="$(git rev-parse --show-toplevel)"
+SUMMARY_PATH="$ROOT/docs/push-summaries/latest.md"
+
+push_input="$(cat)"
+
+if [[ -z "${push_input}" ]]; then
+  echo "pre-push: no refs received; skipping summary generation."
+  exit 0
+fi
+
+python3 "$ROOT/tools/git_summary.py" --output "$SUMMARY_PATH" <<< "$push_input"
+
+if [[ -n "$(git status --porcelain -- "$SUMMARY_PATH")" ]]; then
+  echo ""
+  echo "Push summary updated at docs/push-summaries/latest.md"
+  echo "Review it, then run:"
+  echo "  git add docs/push-summaries/latest.md"
+  echo "  git commit -m \"Add push summary\""
+  echo "  git push"
+  echo ""
+  echo "Push blocked intentionally so the summary becomes part of the visible history."
+  exit 1
+fi
+
+exit 0
diff --git a/.gitignore b/.gitignore
index f19e98c..296a03d 100644
--- a/.gitignore
+++ b/.gitignore
@@ -3 +3,4 @@ composer.lock
 .DS_Store
+.venv/
+__pycache__/
+tools/__pycache__/
diff --git a/AGENTS.md b/AGENTS.md
new file mode 100644
index 0000000..285d25a
--- /dev/null
+++ b/AGENTS.md
@@ -0,0 +1,56 @@
+# AGENTS.md
+
+This repository is a teaching demo for Codex, rules, MCP, and Git-aware workflows.
+
+## Primary Goal
+
+When a user asks to implement a Jira ticket such as `PROJ-123`, follow this workflow:
+
+1. Use the Jira MCP server configured in `.codex/config.toml` to fetch the issue details.
+2. Summarize the ticket in plain English:
+   - title
+   - business goal
+   - acceptance criteria
+   - risks or missing information
+3. Map the ticket to the local codebase before changing anything:
+   - identify likely files
+   - explain why those files are relevant
+   - state assumptions if the ticket is underspecified
+4. Implement the smallest correct change that satisfies the ticket.
+5. Run lightweight verification:
+   - syntax checks
+   - relevant tests if they exist
+   - a short summary of what was validated
+6. Report back with:
+   - what the ticket required
+   - what changed
+   - what still needs confirmation
+
+## Jira Ticket Behavior
+
+If a ticket is mentioned, prefer this sequence:
```
