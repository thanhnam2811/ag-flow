# Security Policy

## Supported versions

ag-flow is currently pre-1.0. Security and workflow-safety fixes are applied to the latest version on the default branch.

## Reporting a vulnerability

Please do not open a public issue for a vulnerability that could enable destructive agent behavior, unsafe command execution, credential exposure, or repository compromise.

Instead, use GitHub's private vulnerability reporting for this repository when available. Include:

- affected skill or workflow
- minimal reproduction steps
- expected versus actual behavior
- impact and any known mitigations

For non-sensitive workflow bugs, use the public issue tracker.

## Scope

Security-sensitive behavior includes, but is not limited to:

- unsafe handling of secrets or credentials
- destructive commands without appropriate safeguards
- bypassing project-native safety instructions
- delegated agents exceeding assigned file ownership
- false verification claims that could mask unsafe changes
