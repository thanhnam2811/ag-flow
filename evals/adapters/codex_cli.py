from __future__ import annotations

from pathlib import Path
from typing import Any

from .cli_common import parse_json_text, parse_jsonl, require_binary, run_command, usage_dict


def run(prompt: str, model: str | None, cwd: Path, timeout: int) -> tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]:
    binary = require_binary("codex")
    command = [
        binary,
        "exec",
        "--ephemeral",
        "--json",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
    ]
    if model:
        command += ["--model", model]
    command.append("-")

    stdout, stderr, latency_ms = run_command(command, cwd, timeout, input_text=prompt)
    events = parse_jsonl(stdout)
    final_text = ""
    usage = usage_dict()
    tool_events = 0

    for event in events:
        event_type = event.get("type")
        if event_type == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                final_text = str(item.get("text", final_text))
            elif item.get("type") in {"command_execution", "tool_call", "mcp_tool_call"}:
                tool_events += 1
        elif event_type == "turn.completed":
            raw_usage = event.get("usage") or {}
            usage = usage_dict(
                raw_usage.get("input_tokens", 0),
                raw_usage.get("output_tokens", 0),
                raw_usage.get("cached_input_tokens", raw_usage.get("cached_tokens", 0)),
            )

    if not final_text:
        raise RuntimeError("Codex JSONL did not contain a final agent_message")

    prediction = parse_json_text(final_text)
    meta = {"tool_events": tool_events, "stderr": stderr[-1000:] if stderr else ""}
    return prediction, usage, latency_ms, meta
