#!/usr/bin/env python3
"""Minimal stdio MCP server for Git summary demos."""

from __future__ import annotations

import json
import traceback
from pathlib import Path

from git_summary import DEFAULT_OUTPUT, GitSummaryError, parse_push_line, render_summary, write_summary


SERVER_INFO = {
    "name": "git_summary_local",
    "version": "0.1.0",
}


TOOLS = [
    {
        "name": "summarize_push",
        "description": "Generate a Markdown summary for a git push pre-push line.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "push_line": {"type": "string"},
            },
            "required": ["push_line"],
        },
    },
    {
        "name": "write_push_summary",
        "description": "Generate and write a push summary Markdown file inside the repo.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "push_line": {"type": "string"},
                "output_path": {"type": "string"},
            },
            "required": ["push_line"],
        },
    },
]


def read_message() -> dict | None:
    try:
        line = input()
    except EOFError:
        return None
    if not line.strip():
        return None
    return json.loads(line)


def send_message(payload: dict) -> None:
    print(json.dumps(payload), flush=True)


def ok_response(request_id: object, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id: object, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def content_text(text: str) -> list[dict]:
    return [{"type": "text", "text": text}]


def handle_call_tool(params: dict) -> dict:
    name = params.get("name")
    arguments = params.get("arguments", {})
    push_line = arguments.get("push_line", "")

    if name == "summarize_push":
        context = parse_push_line(push_line)
        return {"content": content_text(render_summary(context))}

    if name == "write_push_summary":
        context = parse_push_line(push_line)
        output_path = Path(arguments.get("output_path", DEFAULT_OUTPUT))
        path = write_summary(output_path, render_summary(context))
        return {"content": content_text(f"Wrote push summary to {path}")}

    raise GitSummaryError(f"Unknown tool: {name}")


def handle_request(message: dict) -> dict | None:
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params", {})

    if method == "initialize":
        return ok_response(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "serverInfo": SERVER_INFO,
                "capabilities": {"tools": {}},
            },
        )

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return ok_response(request_id, {"tools": TOOLS})

    if method == "tools/call":
        return ok_response(request_id, handle_call_tool(params))

    return error_response(request_id, -32601, f"Method not found: {method}")


def main() -> int:
    while True:
        message = read_message()
        if message is None:
            continue

        try:
            response = handle_request(message)
        except GitSummaryError as exc:
            response = error_response(message.get("id"), -32000, str(exc))
        except Exception:
            response = error_response(message.get("id"), -32603, traceback.format_exc(limit=2))

        if response is not None:
            send_message(response)


if __name__ == "__main__":
    raise SystemExit(main())
