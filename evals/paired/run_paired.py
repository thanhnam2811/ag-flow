#!/usr/bin/env python3
"""Paired vanilla-vs-ag-flow benchmark runner for real repositories."""
from __future__ import annotations

import argparse
import importlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RUNTIMES = {
    "codex": "evals.adapters.codex_cli",
    "claude": "evals.adapters.claude_cli",
    "agy": "evals.adapters.agy_cli",
}

SKILL_PATHS = [
    ROOT / "skills" / "agf-route-adaptive" / "SKILL.md",
    ROOT / "skills" / "agf-explore-code" / "SKILL.md",
    ROOT / "skills" / "agf-plan-impl" / "SKILL.md",
    ROOT / "skills" / "agf-spec-clarify" / "SKILL.md",
    ROOT / "skills" / "agf-dispatch-package" / "SKILL.md",
    ROOT / "skills" / "agf-exec-package" / "SKILL.md",
    ROOT / "skills" / "agf-verify-confidence" / "SKILL.md",
    ROOT / "skills" / "agf-debug-systematic" / "SKILL.md",
    ROOT / "skills" / "agf-session-handoff" / "SKILL.md",
]


def load_runtime(name: str) -> Callable[..., tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]]:
    return importlib.import_module(RUNTIMES[name]).run_task


def load_tasks(path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("tasks"), list):
        raise ValueError("task manifest must contain version: 1 and a tasks list")
    required = {"id", "repo", "base_ref", "prompt"}
    tasks: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in data["tasks"]:
        if not isinstance(raw, dict) or not required.issubset(raw):
            raise ValueError(f"invalid task entry; required fields: {sorted(required)}")
        task_id = str(raw["id"])
        if task_id in seen:
            raise ValueError(f"duplicate task id: {task_id}")
        seen.add(task_id)
        tasks.append(dict(raw))
    return tasks


def ag_flow_policy() -> str:
    sections = []
    for path in SKILL_PATHS:
        sections.append(f"## {path.parent.name}\n\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(sections)


def treatment_prompt(task_prompt: str) -> str:
    return f"""Complete the repository task below. Apply the ag-flow workflow policy that follows.

TASK
---
{task_prompt}
---

AG-FLOW POLICY
---
{ag_flow_policy()}
---

Work in the repository, make the requested changes, and run appropriate verification. Keep delegation proportional to actual independence and risk.
"""


def vanilla_prompt(task_prompt: str) -> str:
    return f"""Complete this repository task. Work in the repository, make the requested changes, and run appropriate verification.

TASK
---
{task_prompt}
---
"""


def git(*args: str, cwd: Path | None = None) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=str(cwd) if cwd else None, text=True,
        capture_output=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {(proc.stderr or proc.stdout).strip()[:1500]}")
    return proc.stdout.strip()


def clone_arm(repo: str, base_ref: str, destination: Path) -> None:
    git("clone", "--quiet", repo, str(destination))
    git("checkout", "--quiet", base_ref, cwd=destination)
    git("reset", "--hard", "HEAD", cwd=destination)
    git("clean", "-fdx", cwd=destination)


def repo_delta(cwd: Path) -> dict[str, Any]:
    status = git("status", "--porcelain=v1", cwd=cwd)
    changed_files = [line[3:] for line in status.splitlines() if len(line) >= 4]
    # Intent-to-add so `git diff HEAD` counts new (untracked) files' content,
    # not just modifications to already-tracked files.
    git("add", "-N", "--", ".", cwd=cwd)
    diff_numstat = git("diff", "--numstat", "HEAD", cwd=cwd)
    added = deleted = 0
    for line in diff_numstat.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            if parts[0].isdigit():
                added += int(parts[0])
            if parts[1].isdigit():
                deleted += int(parts[1])
    return {
        "changed_files": changed_files,
        "changed_file_count": len(changed_files),
        "lines_added": added,
        "lines_deleted": deleted,
    }


def run_arm(
    caller: Callable[..., tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]],
    prompt: str,
    model: str | None,
    cwd: Path,
    timeout: int,
) -> dict[str, Any]:
    try:
        result, usage, latency_ms, meta = caller(prompt, model, cwd, timeout)
        return {
            "completed": True,
            "result": result,
            "usage": usage,
            "latency_ms": latency_ms,
            "meta": meta,
            "delta": repo_delta(cwd),
        }
    except Exception as exc:
        return {
            "completed": False,
            "error": str(exc),
            "delta": repo_delta(cwd),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run paired vanilla-vs-ag-flow real-repo benchmarks")
    parser.add_argument("--runtime", choices=sorted(RUNTIMES), help="codex, claude, or agy")
    parser.add_argument("--model", help="Optional runtime model override")
    parser.add_argument("--tasks", type=Path, default=ROOT / "evals" / "paired" / "tasks.example.yaml")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--output", default="evals/results/paired-latest.json")
    parser.add_argument("--keep-workspaces", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tasks = load_tasks(args.tasks.resolve())
    if args.limit > 0:
        tasks = tasks[:args.limit]

    if args.dry_run:
        for runtime in RUNTIMES:
            module = importlib.import_module(RUNTIMES[runtime])
            if not hasattr(module, "run_task"):
                raise RuntimeError(f"{runtime} adapter does not expose run_task")
        print(json.dumps({"tasks": len(tasks), "runtimes": sorted(RUNTIMES), "ids": [t["id"] for t in tasks]}, indent=2))
        return 0

    if not args.runtime:
        parser.error("--runtime is required unless --dry-run is used")

    caller = load_runtime(args.runtime)
    temp_root = Path(tempfile.mkdtemp(prefix="ag-flow-paired-"))
    report_tasks: list[dict[str, Any]] = []
    try:
        for index, task in enumerate(tasks, start=1):
            task_root = temp_root / str(task["id"])
            vanilla_dir = task_root / "vanilla"
            agflow_dir = task_root / "ag-flow"
            print(f"[{index}/{len(tasks)}] {task['id']}: cloning", file=sys.stderr)
            clone_arm(str(task["repo"]), str(task["base_ref"]), vanilla_dir)
            clone_arm(str(task["repo"]), str(task["base_ref"]), agflow_dir)

            print(f"[{index}/{len(tasks)}] {task['id']}: vanilla", file=sys.stderr)
            vanilla = run_arm(caller, vanilla_prompt(str(task["prompt"])), args.model, vanilla_dir, args.timeout)
            print(f"[{index}/{len(tasks)}] {task['id']}: ag-flow", file=sys.stderr)
            agflow = run_arm(caller, treatment_prompt(str(task["prompt"])), args.model, agflow_dir, args.timeout)

            report_tasks.append({
                "id": task["id"],
                "repo": task["repo"],
                "base_ref": task["base_ref"],
                "expected_route": task.get("expected_route"),
                "vanilla": vanilla,
                "ag_flow": agflow,
            })

        report = {
            "runtime": args.runtime,
            "model": args.model or "<cli-default>",
            "protocol": "paired-real-repo-v1",
            "tasks": report_tasks,
        }
        output = ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({
            "tasks": len(report_tasks),
            "vanilla_completed": sum(bool(t["vanilla"].get("completed")) for t in report_tasks),
            "ag_flow_completed": sum(bool(t["ag_flow"].get("completed")) for t in report_tasks),
            "output": str(output),
        }, indent=2))
        return 0
    finally:
        if args.keep_workspaces:
            print(f"workspaces kept at: {temp_root}", file=sys.stderr)
        else:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
