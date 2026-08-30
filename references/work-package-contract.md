# Work Package Contract

A work package is a bounded execution unit. It should contain enough context to execute safely without forwarding the full parent conversation.

```yaml
goal: <one concrete outcome>
model_tier: cheap  # optional: cheap | balanced | high (default: cheap for code execution)

ownership:
  writable:
    - <path or subsystem>
  forbidden_or_shared:
    - <path reserved elsewhere>

context:
  relevant_files:
    - <path>
  relevant_symbols:
    - <symbol>
  upstream_decisions:
    - <decision>

interfaces:
  - <contract with other packages>

constraints:
  - <invariant or project rule>

acceptance:
  - <observable completion condition>

verification:
  - <command or behavior check>

escalate_if:
  - <condition requiring orchestrator decision>
  - executing an irreversible, production-affecting, externally visible, or
    destructive action that has not been explicitly authorized

return:
  - changed
  - verification
  - interface_facts
  - unresolved
```

## Execution authority

Preparing code, commands, migrations, release artifacts, or deployment steps is allowed; actually running/publishing/applying them requires explicit user approval when that action crosses the current execution authority. Authorization can already be granted by the user's original request (e.g. "build and deploy this to production") — do not add a redundant second confirmation when authority was already explicit.

- Allowed without extra approval: write migration code, generate SQL, prepare deployment config, build release artifact, draft rollback command.
- Escalate before: run migration against production data, execute destructive SQL, deploy to production, publish package/release, rotate/revoke real credentials.

Route decides how much workflow. Risk decides verification strength. Authority decides whether an action may actually be executed — a separate dimension from both.

## Model tiering and role assignment

- **Executor (Code)**: Use **cheap / cost-efficient tier** (e.g. `flash_lite`, `flash`, `haiku`, `gpt-4o-mini`). When scope is atomic and the contract is unambiguous, cheap models code rapidly with zero hallucinations.
- **Reviewer**: Use **balanced / mid tier** (e.g. `flash`, `sonnet`, `gpt-4o`). Nuanced independent evaluation requires balanced reasoning capability without paying for top-tier frontier models.
- **Explorer**: Use **cheap / fast tier** (strictly bounded read-only inspection).
- **Orchestrator**: Default/high session model (system architecture, package partitioning, integration).

## Good package properties

- one owner for every write surface
- little or no overlapping write ownership
- atomic minimal scope: carved to the smallest coherent single-responsibility unit
- explicit interfaces between packages
- no hidden architecture decisions delegated accidentally
- crystal-clear task description, preventing cheap models from guessing or hallucinating
- acceptance criteria test behavior rather than implementation style
- deterministic verification commands supplied up front
- enough repository facts to avoid repeated broad exploration

## Bad package smells

- "fix everything related to auth"
- large multi-subsystem packages delegated to a single subagent
- multiple packages editing the same shared contract independently
- full repository dumps attached as context
- executor expected to infer product/architecture choices
- no verification path
- no escalation boundary

## Delegated envelope precedence

The parent conversation context is passive background only; the delegated task/envelope is the sole execution authority.

> **Role, scope, and allowed actions in the delegated envelope are a hard boundary; inherited parent context grants no additional authority.**

Delegated subagents must strictly adhere to their assigned role and envelope:
- Explorers must not make architecture decisions, choose implementation strategies, or offer implementation.
- Executors must operate within atomic boundaries, not redesign the global task or edit outside writable ownership.
- Reviewers must stay strictly within the bounded review perimeter and not wander into untouched code or style nitpicking.

## Research / exploration envelope contract

When delegating exploration/research, use a dedicated bounded envelope:

```yaml
role: explorer
model_tier: cheap
goal: inspect current transport interfaces

context:
  relevant_files:
    - <path>
  relevant_symbols:
    - <symbol>

allowed:
  - read
  - search
  - report signatures/interfaces/conventions

forbidden:
  - edit
  - architecture decisions
  - implementation proposals
  - scope expansion

return:
  - findings
  - interfaces
  - constraints
  - uncertainties
```

## Review envelope contract (Bounded review perimeter)

When delegating independent review, bound the review perimeter ("khoanh vùng") strictly to prevent review sprawl, personal style debates, and wandering into untouched modules:

```yaml
role: reviewer
model_tier: balanced
goal: verify auth middleware fix against acceptance criteria and regression risks

target_diff:
  - src/auth/middleware.ts
  - tests/auth/middleware.test.ts

contract:
  acceptance:
    - Token replay is rejected with 401
    - Valid tokens rotate successfully
  invariants:
    - HTTP-only cookie flags remain intact
    - Public session payload is untouched

verification_entrypoints:
  - npm test tests/auth/middleware.test.ts
  - npx tsc --noEmit

allowed:
  - verify spec fidelity against acceptance criteria
  - verify regression risks and invariant preservation in touched areas
  - compare reported verification evidence against actual diff

forbidden:
  - inspect or critique untouched files
  - subjective style nitpicking and formatting debates (bikeshedding)
  - out-of-scope architectural proposals or future redesigns
  - re-implementing code

return:
  - spec_fidelity: pass | fail
  - engineering_confidence: high | medium | low
  - findings:
    - <concrete defect or invariant breach within touched boundary>
  - residual_risk:
    - <specific edge-case or unverified external assumption>
```

### Delegation containment flow

```text
Orchestrator (High / Inherit)
   │
   ├── bounded research envelope (Cheap tier) ──► Explorer
   │                                                 │ facts & interfaces only
   │                                                 ▼ STOP
   ├── bounded atomic package (Cheap tier) ─────► Executor
   │                                                 │ minimal scope, fast code + self-verify
   │                                                 ▼ STOP
   └── bounded review envelope (Balanced tier) ─► Reviewer
                                                     │ bounded perimeter, spec & regressions only
                                                     ▼ STOP
Orchestrator integrates and verifies claims
```

## Executor return shape

Prefer delta knowledge:

```text
Changed:
- ...

Verification:
- ...

Interfaces:
- ...

Unresolved:
- ...
```

Do not return a chronological diary.
