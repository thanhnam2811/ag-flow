# Changelog

All notable changes to ag-flow will be documented in this file.

The project follows Semantic Versioning once tagged releases begin.

## [Unreleased]

### Added

- Adaptive per-task routing
- Bounded codebase exploration
- Dependency-aware implementation planning
- Work-package dispatch and execution contracts
- Risk-aware verification
- Systematic debugging workflow
- Session handoff workflow
- Routing and adversarial test cases
- Project contribution and security documentation
- Draft 2020-12 JSON Schema for bounded Work Packages
- Canonical schema-validated Work Package example
- Lightweight repository validator for Agent Skill frontmatter, relative Markdown links, schema validity, examples, and structured fixtures
- GitHub Actions validation on pushes to `main` and pull requests
- Three canonical route case studies: Direct, Guided, and Orchestrated
- Machine-readable YAML fixtures for all 25 routing cases and 12 adversarial cases
- Fixture validation for required fields, route enums, list types, versions, and unique IDs
- CLI-first empirical benchmark harness using existing subscription/session authentication
- Runtime adapters for Codex CLI, Claude Code CLI, and Antigravity CLI (`agy`)
- Routing accuracy, adversarial resilience, desired-behavior, provider-native usage, tool-event, and latency metrics
- Network-free benchmark dry-run and CI compilation checks for all CLI adapters
- Benchmark methodology documenting current limitations and the need for paired real-repository baselines before claiming token savings
- Paired real-repository benchmark harness for vanilla CLI vs ag-flow treatment runs
- Isolated pinned-revision clones, repository-delta metrics, and reusable paired task manifests
- Real-task execution mode for Codex, Claude Code, and Agy adapters
- `agf-spec-clarify` skill for gated requirement-ambiguity resolution, distinct from routing and implementation uncertainty
- Behavior-change test gate in `agf-exec-package`/`agf-verify-confidence` (write/identify a failing test before implementing when a harness exists and it lowers regression risk); deliberately not promoted to a standalone TDD skill until the paired real-repo benchmark shows it changes outcomes
- 6 adversarial fixtures guarding the new skill-budget behavior: trivial-task skill ceiling, read-only discovery not needing clarification, requirement ambiguity not fixable by exploration, high risk not implying dispatch, no-subagent not changing route, and at most one routing question
- Simplicity gate in `agf-plan-impl`/`agf-exec-package`/`agf-verify-confidence`, and output-discipline wording rules in `agf-session-handoff` — primitives borrowed in spirit (not name or persistence mode) from the Ponytail and Caveman skills
- README guidance for guaranteeing routing runs every session by adding a one-line bootstrap instruction to the consuming project's `CLAUDE.md`/`AGENTS.md`, since skill descriptions are matched, not force-loaded

### Fixed

- Stale pre-rename skill paths in `evals/run_benchmarks.py` and `evals/paired/run_paired.py` that made every real-CLI benchmark case fail with `FileNotFoundError` after the `agf-*` rename
- Bounded retry in the Agy adapter (`evals/adapters/agy_cli.py`) for the CLI's intrinsic `CANCELED`/empty-response flakiness (~20-25% of calls), independent of concurrency
- Paired benchmark treatment prompt only loaded 6 of the 9 current skills, silently dropping `agf-spec-clarify`, `agf-debug-systematic`, and `agf-session-handoff` from the arm under test
- Paired benchmark `repo_delta()` undercounted `lines_added` because `git diff --numstat HEAD` ignores untracked files; now intent-to-adds (`git add -N`) before diffing
- Agy adapter retried every parse failure, including deterministic ones retrying can never fix; narrowed to only the recognized transient CANCELED/empty-response case
- `agf-route-adaptive`'s description said "use for non-trivial coding work," contradicting its own adversarial fixture (`adv-013`), which expects it to run and route Direct even for trivial changes; skill-matching engines can only see the description, so this actively discouraged routing the cases most likely to need a fast, cheap route

### Changed

- Replaced the default OpenAI/Anthropic/Gemini API benchmark path with real coding-agent CLI runtimes
- Kept model identifiers runtime-supplied instead of hard-coding model releases
- Frozen routing calibration after policy-conformance benchmarking; end-to-end efficiency claims now belong to paired real-repo evaluation
- **Breaking:** renamed every skill to the `agf-<domain>-<name>` convention to stay collision-safe when installed alongside other skill packs (e.g. Superpowers) that ship skills with the same short names. Directories keep only the new names; consumers pinned to old paths must update.

  | Old | New |
  | --- | --- |
  | `adaptive-routing` | `agf-route-adaptive` |
  | `codebase-exploration` | `agf-explore-code` |
  | `implementation-planning` | `agf-plan-impl` |
  | `session-handoff` | `agf-session-handoff` |
  | `systematic-debugging` | `agf-debug-systematic` |
  | `verification` | `agf-verify-confidence` |
  | `work-package-dispatch` | `agf-dispatch-package` |
  | `work-package-execution` | `agf-exec-package` |

## [0.1.0] - 2026-08-25

### Added

- Initial public core workflow for agent-agnostic coding orchestration
- Portable semantic roles: Orchestrator, Explorer, Executor, Reviewer
- Skills CLI installation support for Claude Code, Codex, and other compatible agents
