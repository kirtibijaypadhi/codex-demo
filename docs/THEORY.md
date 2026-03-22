# Complete theory guide — codex-mcp-demo

Use this document to prepare for presentations, Q&A, and interviews. It explains **concepts**, not just this repo.

---

## 1. What this demo is really about

**Goal:** Show that an AI coding assistant works best when several layers work together:

| Layer | What it does | In this repo |
|--------|----------------|--------------|
| **Code** | Something real to read, change, and break safely | `src/index.php` |
| **Policy** | What the tool is *allowed* to do without asking vs must ask vs must block | `.codex/rules/default.rules` |
| **Tools & context** | How the model gets facts from *outside* the chat (DB, docs, APIs) in a structured way | `.codex/config.toml` (MCP) |
| **Repeatable workflow** | Same quality bar every time (review before commit) | `.codex/SKILLS.md` |
| **Git-aware artifact generation** | Turn upcoming Git changes into visible review material before shipping | `tools/git_mcp_server.py` + `.githooks/pre-push` |
| **Ticket-grounded implementation** | Turn a Jira issue into a traceable code change workflow | `AGENTS.md` + `docs/JIRA_DEMO.md` |

**One-liner:** *We’re not demoing “the model is smart”—we’re demoing **governed automation**: code + policy + tool access + a repeatable process.*

---

## 1.5 Git MCP + pre-push summaries

### What this adds to the story

This repo can now demonstrate a very practical pattern:

- Git knows what is about to be pushed
- An MCP server can inspect that context
- The assistant can turn it into a structured summary
- A Git hook can force that summary to be reviewed before the push goes through

This is a strong teaching example because it connects **tool calling**, **repository state**, and **human review**.

### Why not auto-commit during push?

You *can* script Git to create commits during `pre-push`, but it is usually a poor teaching pattern:

- It hides side effects at exactly the moment users expect a straightforward push
- It can produce confusing history
- It makes failures harder for juniors to debug

So this demo uses a safer pattern:

1. Generate `docs/push-summaries/latest.md`
2. Optionally refresh it before push, or let the hook refresh it during push
3. Let the user decide whether to commit the refreshed summary

That keeps the automation visible and auditable.

### What the MCP server does

The local STDIO server `tools/git_mcp_server.py` exposes tools that:

- read Git ref information from a pre-push line
- collect commit subjects
- list changed files
- compute diff stats
- write a Markdown artifact inside the repo

### What the hook does

The repo-local hook `.githooks/pre-push` calls `tools/git_summary.py` and updates the summary file. If the file changes, it prints an advisory message but still allows the push to continue.

**Sound bite:** *The push summary is visible and reviewable, without making every push fragile.*

---

## 1.6 Jira MCP + implement-ticket workflow

### What this demonstrates

This repo can also show a second important pattern:

- the developer gives a ticket ID
- Codex reads the ticket through Jira MCP
- Codex explains the requirement before coding
- Codex maps the request to local files
- Codex implements and verifies the change

This is often the most convincing real-world use case for juniors because it connects external product requirements to actual code changes.

### Why `AGENTS.md` matters here

Jira access alone is not enough.

You also want repo-specific behavior such as:
- always read the ticket first
- summarize acceptance criteria
- avoid guessing missing details
- keep changes minimal and traceable

That instruction layer lives well in `AGENTS.md`.

### Why not rely on a custom slash command?

A slash command such as `/implement PROJ-123` is a nice UX idea, but the important capability is not the slash command itself.

The real building blocks are:
- MCP access to Jira
- repo instructions in `AGENTS.md`
- a strong prompt convention

If a client later supports native custom commands, it can sit on top of the same workflow.

**Sound bite:** *The magic is not `/implement`; the magic is grounded tool use plus a repeatable implementation workflow.*

---

## 2. Rules engine — theory

### What it is

A **rules engine** (here, mock Starlark-style **policy**) evaluates **proposed actions**—often shell commands or tool calls—and returns an outcome:

- **`allow`** — proceed without extra friction  
- **`prompt`** — stop and get human approval  
- **`forbidden`** — do not run  

The assistant isn’t only following instructions in the chat; it can also be constrained by **machine-readable policy** (when the host enforces it).

### Why it exists

- **Safety:** Block destructive patterns (`rm -rf`, `DROP DATABASE`) even if a prompt is sloppy or malicious.  
- **Consistency:** Same org rules for every user and session.  
- **Auditability:** “Why was this blocked?” maps to a named rule and reason.  
- **Separation of concerns:** Product/security defines policy; engineers don’t re-encode it in every prompt.

### How it differs from “better prompting”

| Prompting | Rules engine |
|-----------|----------------|
| Soft; model may still suggest bad commands | Hard boundary on *classes* of actions |
| Varies by person | Same policy for everyone |
| Hard to prove compliance | Easier to point to explicit rules |

**Sound bite:** *Prompts steer behavior; rules enforce boundaries.*

### This repo’s four rules (how to explain each)

1. **`allow` + git read commands**  
   - **Idea:** Low risk, high value for understanding the repo.  
   - **Common question:** “Why not allow all git?”  
   - **Answer:** Read-only is different from `git push --force` or rewriting history—you’d add more rules for higher-risk git operations.

2. **`prompt` + Composer**  
   - **Idea:** Dependency changes affect lockfiles, supply chain, and runtime; worth a human gate.  
   - **Common question:** “Why prompt and not forbid?”  
   - **Answer:** Updates are *often* necessary; we don’t block—we **confirm** because impact is high.

3. **`prompt` + git push**  
   - **Idea:** Publishing code has external impact, so the workflow should surface it clearly.  
   - **Common question:** “Why prompt if Git already asks me for nothing?”  
   - **Answer:** Because the point is governance: the assistant should still stop and let a human confirm high-impact actions.

4. **`forbidden` + destructive ops**  
   - **Idea:** Some actions have asymmetric downside; automation shouldn’t do them lightly.  
   - **Common question:** “What about false positives?”  
   - **Answer:** Rules should be **specific** (patterns) and **reviewed**; you tune for your org.

### Limitations (honest answers)

- Rules often match **syntax** of commands; clever obfuscation or indirect scripts can be harder to catch—**defense in depth** (reviews, sandboxes) still matters.  
- Policy doesn’t replace **secure code**; it reduces **tool misuse**.  
- A **mock** rules file in a demo illustrates **intent**; production systems connect the same ideas to a real evaluator and enforcement point.

---

## 3. MCP (Model Context Protocol) — theory

### What MCP is (conceptually)

**MCP** is a way for an assistant to talk to **external capabilities** (tools, data, services) through a **standard protocol**, instead of ad-hoc scripts or manual copy-paste.

Think: **one pattern to plug in “things the model can use.”**

### Core ideas

- **Server** exposes **tools** (and sometimes resources/prompts) the client can call.  
- **Client** (the IDE / assistant host) connects to servers and routes model/tool use appropriately.  
- **Structured** — often better than unstructured scraped text for repeatable automation.

### Why teams care

- **Grounding:** Query real DB metadata, internal docs, ticket systems.  
- **Governance:** Control **which** servers exist in a workspace.  
- **Composability:** Swap a SQLite demo for Postgres; swap a mock docs URL for a real internal API catalog.

### Transports (this demo illustrates two patterns)

| Type | Mental model | Typical use |
|------|----------------|-------------|
| **STDIO** | Local process: host spawns a command, talks over stdin/stdout | CLI tools, local DB bridges, scripts |
| **Streamable HTTP** | Remote HTTP service that speaks MCP over the network | Internal APIs, hosted doc indexes, org-wide tools |

**This repo’s names:**

- **`sqlite_local` (STDIO):** Anything **on this machine** exposed via a small adapter process.  
- **`git_summary_local` (STDIO):** A local Git-aware utility server that turns push metadata into reviewable Markdown.  
- **`jira_project` (HTTP):** A remote Jira MCP connection that lets Codex read issue details directly.  
- **`internal_api_docs` (HTTP):** Anything **on the network** exposed as a long-lived MCP service.

### “Why not just use REST?”

- REST is fine; MCP aims at **standardizing how assistants discover and invoke capabilities** in a **tool-oriented** way across hosts.  
- An MCP server might still call REST **internally**.

### “Is MCP secure?”

- Security is **not automatic**: treat MCP servers like **plugins**—they can read data and cause side effects.  
- Mitigations: **allowlists**, auth headers (see mock `Authorization` in config), network boundaries, least privilege, auditing.

---

## 4. Skills (`.codex/SKILLS.md`) — theory

### What a “skill” is here

A **repeatable playbook**: steps + definition of done + output format. **Process as code** for the AI.

### Why it matters

- **Repeatability:** Same review every time.  
- **Teaching:** Onboards people to *how we work*.  
- **Measurable:** “Did we run the security checks?” is explicit.

### “Pre-Commit Code Review” (talk track)

1. **Scope** — what changed.  
2. **Security** — input validation, injection, authz, data leaks.  
3. **Style/quality** — strict types, errors, JSON contract.  
4. **Severity** — triage.  
5. **Gate** — approve vs request changes.

**Common question:** “Isn’t this just a checklist?”  
**Answer:** *Yes—and that’s the point. Checklists scale; ad-hoc chat doesn’t.*

---

## 5. The PHP API — technical talking points

`src/index.php` is intentionally small:

- **JSON API** — `Content-Type: application/json`.  
- **Query param** `user_id` — **input handling** (`filter_input`, `FILTER_VALIDATE_INT`).  
- **404** for unknown user — HTTP semantics.  
- **No database** — runs anywhere; MCP *could* supply DB-backed data in a real setup.

**Security angles:**

- Prefer **typed validation** over raw superglobals.  
- If you add SQL, use **parameterized queries**.  
- If you add auth, separate **authentication** vs **authorization**.

---

## 6. One coherent story (~30 seconds)

*We have a small PHP service the assistant can improve. Before it runs powerful commands, **rules** decide allow vs prompt vs forbid. When it needs facts, **MCP** connects it to local or remote **tools** instead of guessing. Jira MCP can turn a ticket number into grounded requirements. A Git-aware MCP tool can turn the upcoming push into a reviewable artifact. Before we commit, the **Pre-Commit Code Review** skill applies the same security and style bar every time.*

---

## 7. Tough Q&A — short answers

| Question | Answer |
|----------|--------|
| Does the rules file actually run in this repo? | In this demo repo it’s **illustrative**. In a real Codex/Cursor setup, the **host** enforces policy before execution. The **concept** is what you’re demonstrating. |
| What if the model ignores the rules? | The **client** should enforce policy **before** execution; the model isn’t the security boundary. |
| Why MCP if we already have plugins? | MCP pushes **interoperability** and a **common** tool surface for AI hosts—not an overnight replacement for every plugin. |
| What’s the risk of MCP? | Over-privileged servers and leaked tokens—**treat MCP like production integrations.** |
| How is this different from RAG? | RAG feeds **text** into context. MCP often exposes **actions** (tools) with structured schemas—they’re **complementary**. |

---

## 8. Minimum to memorize

1. **Allow / prompt / forbid** — one example each from `.codex/rules/default.rules`.  
2. **STDIO vs HTTP MCP** — one sentence each.  
3. **Skill** — repeatable workflow + severity + commit gate.  
4. **PHP demo** — JSON API, validated `user_id`, 404 path.
5. **Git summary demo** — hook writes a Markdown summary and intentionally blocks push until it is reviewed.
6. **Jira implementation demo** — ticket ID becomes requirements, file mapping, implementation, and verification.

---

## Related files in this project

| File | Role |
|------|------|
| `README.md` | How to run the demo and presenter script |
| `.codex/rules/default.rules` | Mock policy (allow / prompt / forbid) |
| `.codex/config.toml` | Mock MCP servers (STDIO + HTTP) |
| `.codex/SKILLS.md` | “Pre-Commit Code Review” workflow |
| `AGENTS.md` | Repo instructions for ticket-driven implementation behavior |
| `docs/JIRA_DEMO.md` | Presenter notes and prompts for the Jira flow |
| `tools/git_mcp_server.py` | Local MCP server for Git push summaries |
| `.githooks/pre-push` | Hook that enforces visible summary generation before push |
| `src/index.php` | Target PHP codebase for the assistant |
