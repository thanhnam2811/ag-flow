# Work Package Contract

A work package is a bounded execution unit. It should contain enough context to execute safely without forwarding the full parent conversation.

```yaml
goal: <one concrete outcome>

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

return:
  - changed
  - verification
  - interface_facts
  - unresolved
```

## Good package properties

- one owner for every write surface
- little or no overlapping write ownership
- explicit interfaces between packages
- no hidden architecture decisions delegated accidentally
- acceptance criteria test behavior rather than implementation style
- enough repository facts to avoid repeated broad exploration

## Bad package smells

- "fix everything related to auth"
- multiple packages editing the same shared contract independently
- full repository dumps attached as context
- executor expected to infer product/architecture choices
- no verification path
- no escalation boundary

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
