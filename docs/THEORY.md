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

**One-liner:** *We’re not demoing “the model is smart”—we’re demoing **governed automation**: code + policy + tool access + a repeatable process.*

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

### This repo’s three rules (how to explain each)

1. **`allow` + git read commands**  
   - **Idea:** Low risk, high value for understanding the repo.  
   - **Common question:** “Why not allow all git?”  
   - **Answer:** Read-only is different from `git push --force` or rewriting history—you’d add more rules for higher-risk git operations.

2. **`prompt` + Composer**  
   - **Idea:** Dependency changes affect lockfiles, supply chain, and runtime; worth a human gate.  
   - **Common question:** “Why prompt and not forbid?”  
   - **Answer:** Updates are *often* necessary; we don’t block—we **confirm** because impact is high.

3. **`forbidden` + destructive ops**  
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

*We have a small PHP service the assistant can improve. Before it runs powerful commands, **rules** decide allow vs prompt vs forbid. When it needs facts, **MCP** connects it to local or remote **tools** instead of guessing. Before we commit, the **Pre-Commit Code Review** skill applies the same security and style bar every time.*

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

---

## Related files in this project

| File | Role |
|------|------|
| `README.md` | How to run the demo and presenter script |
| `.codex/rules/default.rules` | Mock policy (allow / prompt / forbid) |
| `.codex/config.toml` | Mock MCP servers (STDIO + HTTP) |
| `.codex/SKILLS.md` | “Pre-Commit Code Review” workflow |
| `src/index.php` | Target PHP codebase for the assistant |
