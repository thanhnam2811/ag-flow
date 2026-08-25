from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cli_common import parse_json_text, require_binary, run_command, usage_dict


def _try_result_text(envelope: dict[str, Any]) -> str | None:
    for key in ("result", "response", "text", "output"):
        value = envelope.get(key)
        if isinstance(value, str) and value.strip():
            return value

    for container_key in ("message", "content"):
        container = envelope.get(container_key)
        if isinstance(container, dict):
            for key in ("text", "content", "result"):
                value = container.get(key)
                if isinstance(value, str) and value.strip():
                    return value
        elif isinstance(container, str) and container.strip():
            return container
    return None


def _extract_envelope(stdout: str) -> tuple[str, dict[str, Any], str | None]:
    try:
        val = json.loads(stdout)
        if isinstance(val, dict):
            text = _try_result_text(val)
            if text:
                stats = val.get("stats") or val.get("usage") or {}
                return text, stats, val.get("session_id") or val.get("sessionId")
    except Exception:
        pass

    parsed_objects: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            val = json.loads(line)
            if isinstance(val, dict):
                parsed_objects.append(val)
        except Exception:
            continue

    for obj in reversed(parsed_objects):
        text = _try_result_text(obj)
        if text:
            stats = obj.get("stats") or obj.get("usage") or {}
            if not stats:
                for o in reversed(parsed_objects):
                    if o.get("stats") or o.get("usage"):
                        stats = o.get("stats") or o.get("usage") or {}
                        break
            return text, stats, obj.get("session_id") or obj.get("sessionId")

    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{") and "route" in line:
            return line, {}, None

    raise RuntimeError(f"Agy output did not contain a recognized result text: {stdout[:1000]}")


def _invoke(prompt: str, model: str | None, cwd: Path, timeout: int) -> tuple[str, dict[str, int], float, dict[str, Any]]:
    binary = require_binary("agy")
    command = [binary, "-p", prompt, "--output-format", "json"]
    if model:
        command += ["--model", model]

    stdout, stderr, latency_ms = run_command(command, cwd, timeout)
    result_text, stats, session_id = _extract_envelope(stdout)
    usage = usage_dict(
        stats.get("input_tokens", stats.get("prompt_tokens", stats.get("promptTokenCount", 0))),
        stats.get("output_tokens", stats.get("completion_tokens", stats.get("candidatesTokenCount", 0))),
        stats.get("cached_tokens", stats.get("cache_read_input_tokens", 0)),
    )
    meta = {
        "session_id": session_id,
        "stderr": stderr[-1000:] if stderr else "",
    }
    return result_text, usage, latency_ms, meta


def run(prompt: str, model: str | None, cwd: Path, timeout: int) -> tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]:
    result_text, usage, latency_ms, meta = _invoke(prompt, model, cwd, timeout)
    return parse_json_text(result_text), usage, latency_ms, meta


def run_task(prompt: str, model: str | None, cwd: Path, timeout: int) -> tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]:
    result_text, usage, latency_ms, meta = _invoke(prompt, model, cwd, timeout)
    return {"final_message": result_text}, usage, latency_ms, meta
