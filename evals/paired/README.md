# Paired real-repo benchmarks

This layer measures end-to-end coding-agent behavior rather than routing-policy comprehension.

For every task, run the same runtime and model against two isolated copies of the same repository state:

- **vanilla** — the coding-agent CLI runs without ag-flow instructions.
- **ag-flow** — the same CLI receives the relevant ag-flow workflow skills as an explicit workflow policy.

The runner intentionally does **not** install or remove global skills. It keeps the experiment self-contained and reproducible by injecting the ag-flow policy only into the treatment prompt.

## What to measure

Primary metrics are runtime-agnostic:

- process success / crash
- wall-clock duration
- provider-reported input, output, and cached tokens when exposed
- structured tool events when exposed
- repository delta: changed files and diff size
- verification evidence reported by the agent

Do not claim token savings unless vanilla and ag-flow runs achieve comparable task outcomes.

## Task manifest

Start from `evals/paired/tasks.example.yaml` and create a local manifest. Each task needs a repository URL and a pinned base ref so both arms start from identical source state.

```yaml
version: 1
tasks:
  - id: direct-pagination
    repo: https://github.com/example/project.git
    base_ref: <commit-sha>
    prompt: Fix the pagination boundary bug described in issue #123. Run the smallest relevant verification.
    expected_route: direct
```

Use real tasks with deterministic acceptance criteria. Prefer pinned commits over moving branches.

## Run

```bash
python evals/paired/run_paired.py \
  --runtime codex \
  --tasks /path/to/tasks.yaml \
  --output evals/results/paired-codex.json
```

The runner clones each task twice into a temporary directory, executes vanilla and ag-flow arms, records the repository delta, and deletes the temporary workspace unless `--keep-workspaces` is set.

Optional model override:

```bash
python evals/paired/run_paired.py \
  --runtime claude \
  --model <model-id> \
  --tasks /path/to/tasks.yaml
```

## Interpretation

This harness deliberately does not auto-score semantic task correctness. Repository-specific tests, acceptance commands, or human review remain the source of truth for task success. The report preserves stdout-derived final messages, verification evidence, usage, latency, and git deltas so those outcomes can be compared without pretending a generic judge understands every repository.
