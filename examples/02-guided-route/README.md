# Canonical Example: Guided Route

## Scenario

Refactor a cache layer inside one service so callers use a new cache interface. The change spans several files, but remains inside one subsystem and has no useful parallel write boundaries.

## Routing decision

```yaml
scope: subsystem
uncertainty: medium
risk: medium
parallelizable: false
route: guided
```

The main agent should explore enough of the cache subsystem to understand ownership and dependencies, then plan and execute sequentially.

## Exploration brief

```text
Relevant files:
- cache interface
- cache implementation
- service callers
- focused tests

Key constraints:
- cache key format must remain stable
- callers must not bypass the interface
- no external API changes
```

## Plan

1. Stabilize the new cache interface.
2. Update the implementation.
3. Migrate subsystem callers.
4. Update focused tests.
5. Run type checking and targeted tests.

## Verification

Expected verification depth: **Level 2**.

```text
Changed:
- cache interface updated
- implementation migrated
- callers use the new interface

Verification:
- subsystem unit tests passed
- type check passed

Delegation:
- none; overlapping sequential dependencies made delegation low-value
```

## Why this stays Guided

The task benefits from explicit discovery and planning, but the work is tightly coupled through one subsystem. Spawning multiple executors would create coordination overhead without clean ownership boundaries.
