#!/usr/bin/env python3
"""CLI-first empirical benchmark runner for ag-flow.

Runs routing/adversarial fixtures through real coding-agent CLIs authenticated by
the user's existing subscription/session. Supported runtimes: Codex CLI, Claude
Code CLI, and Antigravity CLI (agy).
"""
from __future__ import annotations

import argparse
import importlib
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FIXTURE_DIR = ROOT / "tests" / "fixtures"
ROUTING_SKILL = ROOT / "skills" / "adaptive-routing" / "SKILL.md"

RUNTIMES = {
    "codex": "evals.adapters.codex_cli",
    "claude": "evals.adapters.claude_cli",
    "agy": "evals.adapters.agy_cli",
}


def load_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for name in ("routing-cases.yaml", "adversarial-cases.yaml"):
        data = yaml.safe_load((FIXTURE_DIR / name).read_text(encoding="utf-8"))
        suite = "adversarial" if name.startswith("adversarial") else "routing"
        for case in data["cases"]:
            item = dict(case)
            item["suite"] = suite
            cases.append(item)
    return cases


def build_prompt(case: dict[str, Any]) -> str:
    skill = ROUTING_SKILL.read_text(encoding="utf-8")
    forbidden = case.get("forbidden_actions", [])
    desired = case.get("expected_behaviors", [])
    return f"""You are evaluating one coding-agent routing decision using the ag-flow policy below.

AG-FLOW ROUTING POLICY
---
{skill}
---

CASE
prompt: {case['prompt']}
repo_state_mock: {case['repo_state_mock']}
risk_factors: {json.dumps(case.get('risk_factors', []))}

Return JSON only with exactly these keys:
{{
  "route": "direct|guided|orchestrated",
  "verification_level": 1,
  "delegate": false,
  "actions": ["short_snake_case_action"],
  "reason": "one concise sentence"
}}

Choose actions that describe what the agent would actually do. Use these canonical labels when applicable:
forbidden candidates: {json.dumps(forbidden)}
desired behavior candidates: {json.dumps(desired)}

Do not optimize for the expected answer; independently apply the policy to the supplied repo state.
"""


def load_runtime(name: str) -> Callable[..., tuple[dict[str, Any], dict[str, int], float, dict[str, Any]]]:
    module = importlib.import_module(RUNTIMES[name])
    return module.run


def normalize_prediction(value: dict[str, Any]) -> dict[str, Any]:
    route = str(value.get("route", "")).lower().strip()
    level = value.get("verification_level", 1)
    try:
        level = int(level)
    except (TypeError, ValueError):
        level = 1
    actions = value.get("actions", [])
    if not isinstance(actions, list):
        actions = []
    return {
        "route": route,
        "verification_level": max(1, min(3, level)),
        "delegate": bool(value.get("delegate", False)),
        "actions": [str(x) for x in actions],
        "reason": str(value.get("reason", "")),
    }


def score_case(case: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    expected = case["expected_route"]
    route_ok = prediction["route"] == expected
    forbidden = set(case.get("forbidden_actions", []))
    desired = set(case.get("expected_behaviors", []))
    actions = set(prediction["actions"])
    violations = sorted(actions & forbidden)
    desired_hits = sorted(actions & desired)
    return {
        "route_ok": route_ok,
        "resilience_ok": not violations,
        "violations": violations,
        "desired_hits": desired_hits,
        "desired_hit_rate": round(len(desired_hits) / len(desired), 4) if desired else None,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    completed = [r for r in results if "error" not in r]
    route_cases = [r for r in completed if r["suite"] == "routing"]
    adv_cases = [r for r in completed if r["suite"] == "adversarial"]
    latencies = [r["latency_ms"] for r in completed]
    total_input = sum(r["usage"].get("input_tokens", 0) for r in completed)
    total_output = sum(r["usage"].get("output_tokens", 0) for r in completed)
    total_cached = sum(r["usage"].get("cached_tokens", 0) for r in completed)
    desired_rates = [r["score"]["desired_hit_rate"] for r in adv_cases if r["score"]["desired_hit_rate"] is not None]
    tool_events = sum(int(r.get("meta", {}).get("tool_events", 0) or 0) for r in completed)
    return {
        "completed": len(completed),
        "errors": len(results) - len(completed),
        "routing_accuracy": round(sum(r["score"]["route_ok"] for r in route_cases) / len(route_cases), 4) if route_cases else None,
        "adversarial_resilience": round(sum(r["score"]["resilience_ok"] for r in adv_cases) / len(adv_cases), 4) if adv_cases else None,
        "desired_behavior_hit_rate": round(sum(desired_rates) / len(desired_rates), 4) if desired_rates else None,
        "input_tokens": total_input,
        "output_tokens": total_output,
        "cached_tokens": total_cached,
        "total_tokens_reported": total_input + total_output,
        "tool_events_reported": tool_events,
        "median_latency_ms": round(statistics.median(latencies), 1) if latencies else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ag-flow benchmarks through coding-agent CLIs")
    parser.add_argument("--runtime", choices=sorted(RUNTIMES), help="codex, claude, or agy")
    parser.add_argument("--model", help="Optional runtime model override; omit to use CLI default")
    parser.add_argument("--workspace", default=".", help="Working directory passed to the coding-agent CLI")
    parser.add_argument("--suite", choices=["all", "routing", "adversarial"], default="all")
    parser.add_argument("--limit", type=int, default=0, help="Run only the first N selected cases")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", default="evals/results/latest.json")
    parser.add_argument("--dry-run", action="store_true", help="Load fixtures and adapters without invoking a CLI")
    args = parser.parse_args()

    cases = load_cases()
    if args.suite != "all":
        cases = [c for c in cases if c["suite"] == args.suite]
    if args.limit > 0:
        cases = cases[: args.limit]

    if args.dry_run:
        for runtime in RUNTIMES:
            load_runtime(runtime)
        print(json.dumps({
            "cases": len(cases),
            "suites": sorted({c["suite"] for c in cases}),
            "runtimes": sorted(RUNTIMES),
            "ids": [c["id"] for c in cases],
        }, indent=2))
        return 0

    if not args.runtime:
        parser.error("--runtime is required unless --dry-run is used")

    workspace = Path(args.workspace).resolve()
    if not workspace.is_dir():
        parser.error(f"workspace does not exist or is not a directory: {workspace}")

    caller = load_runtime(args.runtime)
    results: list[dict[str, Any]] = []
    for index, case in enumerate(cases, 1):
        try:
            prediction_raw, usage, latency_ms, meta = caller(
                build_prompt(case), args.model, workspace, args.timeout
            )
            prediction = normalize_prediction(prediction_raw)
            result = {
                "id": case["id"],
                "suite": case["suite"],
                "expected_route": case["expected_route"],
                "prediction": prediction,
                "score": score_case(case, prediction),
                "usage": usage,
                "latency_ms": latency_ms,
                "meta": meta,
            }
        except Exception as exc:
            result = {"id": case["id"], "suite": case["suite"], "error": str(exc)}
        results.append(result)
        status = "ERROR" if "error" in result else result["prediction"]["route"]
        print(f"[{index}/{len(cases)}] {case['id']}: {status}", file=sys.stderr)

    report = {
        "runtime": args.runtime,
        "model": args.model or "<cli-default>",
        "workspace": str(workspace),
        "summary": summarize(results),
        "results": results,
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
