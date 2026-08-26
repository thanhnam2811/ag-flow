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
