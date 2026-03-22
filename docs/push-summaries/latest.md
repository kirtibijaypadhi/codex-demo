# Push Summary

Generated: 2026-03-22 17:40:03 UTC

## Push Context

- Local ref: `refs/heads/main`
- Local sha: `d961a63dc7d4f62d6b166cbe0f7a6e54d47849c3`
- Remote ref: `refs/heads/main`
- Remote sha: `0000000000000000000000000000000000000000`

## Commits In This Push

- d961a63 Initial commit

## Files Changed

- `.codex/SKILLS.md`
- `.codex/config.toml`
- `.codex/rules/default.rules`
- `.gitignore`
- `Makefile`
- `README.md`
- `composer.json`
- `docs/THEORY.md`
- `scripts/demo.sh`
- `src/index.php`

## Diff Stat

```text
.codex/SKILLS.md           |  47 +++++++++++
 .codex/config.toml         |  28 +++++++
 .codex/rules/default.rules |  31 +++++++
 .gitignore                 |   3 +
 Makefile                   |  19 +++++
 README.md                  | 154 +++++++++++++++++++++++++++++++++++
 composer.json              |  16 ++++
 docs/THEORY.md             | 197 +++++++++++++++++++++++++++++++++++++++++++++
 scripts/demo.sh            |  20 +++++
 src/index.php              |  45 +++++++++++
 10 files changed, 560 insertions(+)
```

## Diff Excerpt

```diff
diff --git a/.codex/SKILLS.md b/.codex/SKILLS.md
new file mode 100644
index 0000000..bdc9158
--- /dev/null
+++ b/.codex/SKILLS.md
@@ -0,0 +1,47 @@
+# Skills for `codex-mcp-demo`
+
+## Skill: Pre-Commit Code Review
+
+Use this skill before creating a commit for any PHP code change.
+
+### Goal
+Catch security vulnerabilities and style/quality issues early so demo commits stay safe and readable.
+
+### Inputs
+- Changed files (`git diff` or staged diff)
+- Target runtime assumptions (PHP version, dependencies)
+
+### Workflow
+1. **Scope the change**
+   - Identify edited PHP files under `src/`.
+   - Summarize behavior changes in one sentence.
+2. **Run security checks**
+   - Validate user input handling (`filter_input`, sanitization, validation).
+   - Check for injection risks (SQL injection, command execution, unsafe eval usage).
+   - Review authentication/authorization assumptions for endpoints.
+   - Ensure sensitive data is not leaked in responses or logs.
+3. **Run style and quality checks**
+   - Confirm `declare(strict_types=1);` usage for PHP files where appropriate.
+   - Check naming clarity, dead code, and duplicated logic.
+   - Verify response codes and error paths are explicit and consistent.
+   - Validate JSON responses are predictable and documented.
+4. **Report findings**
+   - Output issues ordered by severity: `critical`, `high`, `medium`, `low`.
+   - Include file path and a suggested fix for each finding.
+5. **Gate commit**
+   - If `critical` or `high` issues exist, block commit and request fixes.
+   - If only `medium`/`low` issues exist, allow commit with follow-up recommendations.
+
+### Output Template
+```md
+Pre-Commit Code Review Result
+
+Risk Level: <low|medium|high>
+
+Findings:
+1) [severity] <issue title> - <file path>
+   - Why it matters:
+   - Suggested fix:
+
+Commit Decision: <approve|changes requested>
+```
diff --git a/.codex/config.toml b/.codex/config.toml
new file mode 100644
index 0000000..c261036
--- /dev/null
+++ b/.codex/config.toml
@@ -0,0 +1,28 @@
+# Mock Codex configuration for MCP demo integrations.
+
+[project]
+name = "codex-mcp-demo"
+language = "php"
+entrypoint = "src/index.php"
+
+[rules]
+default = ".codex/rules/default.rules"
+
+# Dummy local STDIO MCP server (e.g., SQLite connector).
+[mcp.servers.sqlite_local]
+type = "stdio"
+command = "python3"
+args = ["tools/sqlite_mcp_server.py", "--db", "data/demo.sqlite"]
+working_dir = "."
+enabled = true
+
+# Dummy Streamable HTTP MCP server (e.g., internal API docs service).
+[mcp.servers.internal_api_docs]
+type = "streamable_http"
+url = "https://internal-docs.example.local/mcp"
+headers = { "Authorization" = "Bearer DEMO_TOKEN", "X-Demo-Client" = "codex-mcp-demo" }
+enabled = true
+
+[mcp.defaults]
+timeout_seconds = 20
+retry_attempts = 2
diff --git a/.codex/rules/default.rules b/.codex/rules/default.rules
new file mode 100644
index 0000000..9a16ae4
--- /dev/null
+++ b/.codex/rules/default.rules
@@ -0,0 +1,31 @@
+# Mock Codex rules engine policy (Starlark-style example).
+# This file is intentionally simple for demo purposes.
+
+rules = [
+    # 1) Allow: low-risk read-only git commands.
+    rule(
+        name = "allow-safe-git-read",
+        action = "allow",
+        match = command_matches(r"^git (status|diff|log)( .*)?$"),
+        reason = "Allow standard read-only git inspection commands.",
+    ),
+
+    # 2) Prompt: ask for explicit approval on package changes.
+    rule(
+        name = "prompt-package-management",
+        action = "prompt",
+        match = command_matches(r"^composer (update|require|remove)( .*)?$"),
+        reason = "Package operations can change lockfiles and runtime behavior.",
+    ),
+
+    # 3) Forbidden: block clearly dangerous shell/database commands.
+    rule(
+        name = "forbid-destructive-ops",
+        action = "forbidden",
+        match = any_of([
+            command_matches(r"^rm -rf( .*)?$"),
+            command_matches(r".*\bDROP\s+DATABASE\b.*"),
```
