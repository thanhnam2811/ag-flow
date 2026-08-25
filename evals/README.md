# Empirical benchmarks

ag-flow benchmarks are **CLI-first**. They run through the coding-agent runtimes people actually use, authenticated by existing subscription/session login instead of requiring separate API keys.

Supported runtimes:

- Codex CLI (`codex`)
- Claude Code CLI (`claude`)
- Antigravity CLI (`agy`)

The harness stays model-agnostic: omit `--model` to use the CLI's configured default, or pass a runtime-supported model identifier explicitly.

## What it measures

The fixture benchmark records:

- **Routing accuracy** — exact match against `expected_route`.
- **Adversarial resilience** — whether canonical `forbidden_actions` are avoided.
- **Desired behavior hit rate** — canonical expected behaviors present in the action plan.
- **Provider-reported usage** — input/output/cached tokens when the CLI exposes them.
- **Tool events** — when the runtime exposes structured tool events.
- **Latency** — wall-clock time per case.

Usage fields are provider-native and are not assumed to be perfectly comparable across runtimes.

## Dry run

CI uses dry-run mode. It imports every adapter and loads all fixtures without launching any external agent:

```bash
python evals/run_benchmarks.py --dry-run
```

Filter the corpus:

```bash
python evals/run_benchmarks.py --dry-run --suite adversarial --limit 5
```

## Codex CLI

Authenticate Codex normally with your ChatGPT/Codex account, then run:

```bash
python evals/run_benchmarks.py \
  --runtime codex \
  --suite all
```

Optional model override:

```bash
python evals/run_benchmarks.py \
  --runtime codex \
  --model <codex-model-id>
```

The adapter uses `codex exec --ephemeral --json` in a read-only sandbox and extracts the final agent message plus `turn.completed` usage when available.

## Claude Code CLI

Authenticate Claude Code normally, then run:

```bash
python evals/run_benchmarks.py \
  --runtime claude
```

Optional model override:

```bash
python evals/run_benchmarks.py \
  --runtime claude \
  --model <claude-model-id>
```

The adapter uses headless print mode with JSON output and reads usage/turn metadata when exposed by the installed CLI version.

## Antigravity CLI (Agy)

Authenticate `agy` normally through Antigravity/Google Sign-In, then run:

```bash
python evals/run_benchmarks.py \
  --runtime agy
```

Optional model override if supported by your installed Agy version:

```bash
python evals/run_benchmarks.py \
  --runtime agy \
  --model <agy-model-id>
```

The adapter invokes Agy headlessly with `-p` and `--output-format json`. Parsing is defensive because some Agy releases have emitted imperfect strict-JSON output.

## Workspace

By default the agent runs with the current directory as its workspace. Override it with:

```bash
python evals/run_benchmarks.py \
  --runtime codex \
  --workspace /path/to/repo
```

The current fixture suite is a routing-policy benchmark, so it embeds the adaptive-routing policy in the prompt. The next empirical layer should use real repository tasks and compare paired runs in isolated worktrees.

## Paired real-repo benchmark

The meaningful end-to-end experiment is:

```text
same task + same repo + same runtime + same model

A: vanilla coding-agent CLI
B: coding-agent CLI with ag-flow installed/enabled
```

Compare task success, verification evidence, delegation/tool activity, wall time, provider-reported usage, and repository delta. Do not call request-token differences "token savings" until the paired runs have comparable task outcomes.

## Results

By default:

```text
evals/results/latest.json
```

Use `--output` for named snapshots. `evals/results/` is ignored by default so repeated local benchmarks do not pollute the repository.

## Scoring limitation

Adversarial resilience uses deterministic action-label matching. This is cheap and reproducible, but it is not a semantic judge. If a future evaluator adds an independent LLM judge, judge cost and model bias should be reported separately from the primary score.
