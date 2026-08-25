from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cli_common import parse_json_text, require_binary, run_command, usage_dict


def run(prompt: str, model: str | None, cwd: Path, timeout: int) -> tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]:
    binary = require_binary("claude")
    command = [binary, "-p", prompt, "--output-format", "json"]
    if model:
        command += ["--model", model]

    stdout, stderr, latency_ms = run_command(command, cwd, timeout)
    try:
        envelope = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Claude CLI returned invalid JSON: {stdout[:1000]}") from exc

    result_text = envelope.get("result")
    if not isinstance(result_text, str):
        # Some versions may return content-like structures. Keep the fallback narrow.
        content = envelope.get("content")
        if isinstance(content, str):
            result_text = content
        else:
            raise RuntimeError("Claude JSON output did not contain a string result")

    raw_usage = envelope.get("usage") or {}
    usage = usage_dict(
        raw_usage.get("input_tokens", 0),
        raw_usage.get("output_tokens", 0),
        raw_usage.get("cache_read_input_tokens", raw_usage.get("cached_input_tokens", 0)),
    )
    meta = {
        "num_turns": int(envelope.get("num_turns", 0) or 0),
        "duration_ms": envelope.get("duration_ms"),
        "stderr": stderr[-1000:] if stderr else "",
    }
    return parse_json_text(result_text), usage, latency_ms, meta
