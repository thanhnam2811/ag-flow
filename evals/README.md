# Empirical benchmarks

The benchmark harness turns ag-flow's structured fixtures into repeatable model evaluations without coupling the repository to one SDK, model family, or hosted eval platform.

## What it measures

The initial harness records:

- **Routing accuracy** — exact match against `expected_route` for routing fixtures.
- **Adversarial resilience** — whether the model avoids canonical `forbidden_actions` in adversarial fixtures.
- **Desired behavior hits** — which canonical `expected_behaviors` appear in the model's action plan.
- **Token usage** — input/output usage when the provider returns token metadata.
- **Latency** — wall-clock request latency per case.

These metrics are intentionally separate. A route can be correct while verification depth or delegation behavior is poor.

## Dry run

Dry run makes no network requests and requires no API key:

```bash
python evals/run_benchmarks.py --dry-run
```

Filter by suite or limit cases:

```bash
python evals/run_benchmarks.py --dry-run --suite adversarial --limit 5
```

## OpenAI

Set an API key, then supply the model you want to measure:

```bash
export OPENAI_API_KEY=...
python evals/run_benchmarks.py \
  --provider openai \
  --model gpt-5.6-luna
```

The adapter uses the Responses API. Model identifiers are not hard-coded by ag-flow.

## Anthropic

```bash
export ANTHROPIC_API_KEY=...
python evals/run_benchmarks.py \
  --provider anthropic \
  --model <anthropic-model-id>
```

## Gemini

```bash
export GEMINI_API_KEY=...
python evals/run_benchmarks.py \
  --provider gemini \
  --model gemini-3.7-flash
```

## Results

By default the runner writes:

```text
evals/results/latest.json
```

Use `--output` to keep named benchmark snapshots outside the ignored results directory when publishing a curated result.

Each case stores the normalized decision, score, provider usage, and latency. The summary aggregates routing accuracy, adversarial resilience, total tokens, and median latency.

## Important limitation

Adversarial resilience currently uses deterministic action-label matching. That makes the score reproducible and cheap, but it is not a semantic judge. A later benchmark revision may add an optional independent judge, provided the extra judge cost and bias are reported separately rather than hidden inside the headline score.

Likewise, token counts are provider-reported request usage. They do **not** yet prove end-to-end coding-task token savings versus a full-context baseline. That comparison requires paired real-repository runs and belongs in a later benchmark layer.
