#!/usr/bin/env python3
"""Lightweight empirical benchmark runner for ag-flow.

Runs structured routing/adversarial fixtures against OpenAI, Anthropic, or Gemini
without introducing a project-specific CLI or SDK dependency. Providers are
selected explicitly and model names are user-supplied so the harness does not
stale with model releases.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures"
ROUTING_SKILL = ROOT / "skills" / "adaptive-routing" / "SKILL.md"


def load_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for name in ("routing-cases.yaml", "adversarial-cases.yaml"):
        data = yaml.safe_load((FIXTURE_DIR / name).read_text(encoding="utf-8"))
        source = "adversarial" if name.startswith("adversarial") else "routing"
        for case in data["cases"]:
            item = dict(case)
            item["suite"] = source
            cases.append(item)
    return cases


def build_prompt(case: dict[str, Any]) -> str:
    skill = ROUTING_SKILL.read_text(encoding="utf-8")
    forbidden = case.get("forbidden_actions", [])
    expected_behaviors = case.get("expected_behaviors", [])
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

Choose actions that describe what the agent would actually do. For adversarial cases, use these canonical action labels when applicable:
forbidden candidates: {json.dumps(forbidden)}
desired behavior candidates: {json.dumps(expected_behaviors)}

Do not optimize for the expected answer; independently apply the policy to the supplied repo state.
"""


def request_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:1000]}") from exc


def parse_json_text(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def call_openai(model: str, prompt: str, timeout: int) -> tuple[dict[str, Any], dict[str, int]]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    raw = request_json(
        "https://api.openai.com/v1/responses",
        {"Authorization": f"Bearer {key}"},
        {"model": model, "input": prompt},
        timeout,
    )
    chunks: list[str] = []
    for item in raw.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                chunks.append(content.get("text", ""))
    usage = raw.get("usage") or {}
    return parse_json_text("".join(chunks)), {
        "input_tokens": int(usage.get("input_tokens", 0) or 0),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
    }


def call_anthropic(model: str, prompt: str, timeout: int) -> tuple[dict[str, Any], dict[str, int]]:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    raw = request_json(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": key, "anthropic-version": "2023-06-01"},
        {"model": model, "max_tokens": 700, "messages": [{"role": "user", "content": prompt}]},
        timeout,
    )
    text = "".join(part.get("text", "") for part in raw.get("content", []) if part.get("type") == "text")
    usage = raw.get("usage") or {}
    return parse_json_text(text), {
        "input_tokens": int(usage.get("input_tokens", 0) or 0),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
    }


def call_gemini(model: str, prompt: str, timeout: int) -> tuple[dict[str, Any], dict[str, int]]:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    raw = request_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"x-goog-api-key": key},
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0},
        },
        timeout,
    )
    candidates = raw.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Gemini returned no candidates: {raw}")
    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(part.get("text", "") for part in parts)
    usage = raw.get("usageMetadata") or {}
    return parse_json_text(text), {
        "input_tokens": int(usage.get("promptTokenCount", 0) or 0),
        "output_tokens": int(usage.get("candidatesTokenCount", 0) or 0),
    }


PROVIDERS = {"openai": call_openai, "anthropic": call_anthropic, "gemini": call_gemini}


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
    resilience_ok = not violations
    return {
        "route_ok": route_ok,
        "resilience_ok": resilience_ok,
        "violations": violations,
        "desired_hits": desired_hits,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    completed = [r for r in results if "error" not in r]
    route_cases = [r for r in completed if r["suite"] == "routing"]
    adv_cases = [r for r in completed if r["suite"] == "adversarial"]
    total_input = sum(r["usage"]["input_tokens"] for r in completed)
    total_output = sum(r["usage"]["output_tokens"] for r in completed)
    latencies = [r["latency_ms"] for r in completed]
    return {
        "completed": len(completed),
        "errors": len(results) - len(completed),
        "routing_accuracy": round(sum(r["score"]["route_ok"] for r in route_cases) / len(route_cases), 4) if route_cases else None,
        "adversarial_resilience": round(sum(r["score"]["resilience_ok"] for r in adv_cases) / len(adv_cases), 4) if adv_cases else None,
        "input_tokens": total_input,
        "output_tokens": total_output,
        "total_tokens": total_input + total_output,
        "median_latency_ms": round(statistics.median(latencies), 1) if latencies else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ag-flow routing benchmarks")
    parser.add_argument("--provider", choices=sorted(PROVIDERS), help="LLM provider")
    parser.add_argument("--model", help="Provider model identifier")
    parser.add_argument("--suite", choices=["all", "routing", "adversarial"], default="all")
    parser.add_argument("--limit", type=int, default=0, help="Run only the first N selected cases")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--output", default="evals/results/latest.json")
    parser.add_argument("--dry-run", action="store_true", help="Load fixtures and print benchmark plan without API calls")
    args = parser.parse_args()

    cases = load_cases()
    if args.suite != "all":
        cases = [c for c in cases if c["suite"] == args.suite]
    if args.limit > 0:
        cases = cases[: args.limit]

    if args.dry_run:
        print(json.dumps({"cases": len(cases), "suites": sorted({c['suite'] for c in cases}), "ids": [c["id"] for c in cases]}, indent=2))
        return 0

    if not args.provider or not args.model:
        parser.error("--provider and --model are required unless --dry-run is used")

    caller = PROVIDERS[args.provider]
    results: list[dict[str, Any]] = []
    for index, case in enumerate(cases, 1):
        started = time.perf_counter()
        try:
            prediction_raw, usage = caller(args.model, build_prompt(case), args.timeout)
            prediction = normalize_prediction(prediction_raw)
            result = {
                "id": case["id"],
                "suite": case["suite"],
                "expected_route": case["expected_route"],
                "prediction": prediction,
                "score": score_case(case, prediction),
                "usage": usage,
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            }
        except Exception as exc:
            result = {"id": case["id"], "suite": case["suite"], "error": str(exc)}
        results.append(result)
        print(f"[{index}/{len(cases)}] {case['id']}: {'ERROR' if 'error' in result else result['prediction']['route']}", file=sys.stderr)

    report = {
        "provider": args.provider,
        "model": args.model,
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
