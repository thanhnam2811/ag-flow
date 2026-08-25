from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cli_common import parse_json_text, require_binary, run_command, usage_dict


def _extract_json_object(stdout: str) -> dict[str, Any]:
    """Parse Agy JSON output defensively.

    Agy headless output has had versions where strict JSON formatting was imperfect,
    so first try full JSON, then fall back to the last parseable JSON line.
    """
    try:
        value = json.loads(stdout)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise RuntimeError(f"Agy output did not contain a parseable JSON object: {stdout[:1000]}")


def _result_text(envelope: dict[str, Any]) -> str:
    for key in ("result", "response", "text", "output"):
        value = envelope.get(key)
        if isinstance(value, str) and value.strip():
            return value

    # Handle common nested response/content shapes without depending on one version.
    for container_key in ("message", "content"):
        container = envelope.get(container_key)
        if isinstance(container, dict):
            for key in ("text", "content", "result"):
                value = container.get(key)
                if isinstance(value, str) and value.strip():
                    return value
        elif isinstance(container, str) and container.strip():
            return container

    raise RuntimeError("Agy JSON output did not expose a recognized result text field")


def run(prompt: str, model: str | None, cwd: Path, timeout: int) -> tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]:
    binary = require_binary("agy")
    command = [binary, "-p", prompt, "--output-format", "json"]
    if model:
        command += ["--model", model]

    stdout, stderr, latency_ms = run_command(command, cwd, timeout)
    envelope = _extract_json_object(stdout)
    stats = envelope.get("stats") or envelope.get("usage") or {}
    usage = usage_dict(
        stats.get("input_tokens", stats.get("prompt_tokens", stats.get("promptTokenCount", 0))),
        stats.get("output_tokens", stats.get("completion_tokens", stats.get("candidatesTokenCount", 0))),
        stats.get("cached_tokens", stats.get("cache_read_input_tokens", 0)),
    )
    meta = {
        "session_id": envelope.get("session_id") or envelope.get("sessionId"),
        "stderr": stderr[-1000:] if stderr else "",
    }
    return parse_json_text(_result_text(envelope)), usage, latency_ms, meta
