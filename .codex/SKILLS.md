# Skills for `codex-mcp-demo`

## Skill: Pre-Commit Code Review

Use this skill before creating a commit for any PHP code change.

### Goal
Catch security vulnerabilities and style/quality issues early so demo commits stay safe and readable.

### Inputs
- Changed files (`git diff` or staged diff)
- Target runtime assumptions (PHP version, dependencies)

### Workflow
1. **Scope the change**
   - Identify edited PHP files under `src/`.
   - Summarize behavior changes in one sentence.
2. **Run security checks**
   - Validate user input handling (`filter_input`, sanitization, validation).
   - Check for injection risks (SQL injection, command execution, unsafe eval usage).
   - Review authentication/authorization assumptions for endpoints.
   - Ensure sensitive data is not leaked in responses or logs.
3. **Run style and quality checks**
   - Confirm `declare(strict_types=1);` usage for PHP files where appropriate.
   - Check naming clarity, dead code, and duplicated logic.
   - Verify response codes and error paths are explicit and consistent.
   - Validate JSON responses are predictable and documented.
4. **Report findings**
   - Output issues ordered by severity: `critical`, `high`, `medium`, `low`.
   - Include file path and a suggested fix for each finding.
5. **Gate commit**
   - If `critical` or `high` issues exist, block commit and request fixes.
   - If only `medium`/`low` issues exist, allow commit with follow-up recommendations.

### Output Template
```md
Pre-Commit Code Review Result

Risk Level: <low|medium|high>

Findings:
1) [severity] <issue title> - <file path>
   - Why it matters:
   - Suggested fix:

Commit Decision: <approve|changes requested>
```
