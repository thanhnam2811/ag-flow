from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"Required CLI '{name}' was not found in PATH")
    return path


def run_command(
    command: list[str],
    cwd: Path,
    timeout: int,
    input_text: str | None = None,
) -> tuple[str, str, float]:
    started = time.perf_counter()
    use_shell = sys.platform.startswith("win") and (
        command[0].lower().endswith((".cmd", ".bat")) or not command[0].lower().endswith(".exe")
    )
    proc = subprocess.run(
        command,
        cwd=str(cwd),
        input=input_text,
        stdin=subprocess.DEVNULL if input_text is None else None,
        text=True,
        capture_output=True,
        shell=use_shell,
        timeout=timeout,
        check=False,
    )
    latency_ms = round((time.perf_counter() - started) * 1000, 1)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise RuntimeError(f"CLI exited {proc.returncode}: {detail[:1500]}")
    return proc.stdout, proc.stderr, latency_ms


def parse_json_text(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(cleaned)


def parse_jsonl(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def usage_dict(input_tokens: int = 0, output_tokens: int = 0, cached_tokens: int = 0) -> dict[str, int]:
    return {
        "input_tokens": int(input_tokens or 0),
        "output_tokens": int(output_tokens or 0),
        "cached_tokens": int(cached_tokens or 0),
    }
