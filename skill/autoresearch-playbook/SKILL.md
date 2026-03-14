---
name: autoresearch-playbook
description: >
  Public reusable skill for running evidence-driven autoresearch loops with
  baseline discipline, acceptance gates, deep post-run analysis, durable state,
  and controlled SOTA intake.
---

# Autoresearch Playbook

Use this skill when the goal is to improve a system through repeated, measured research rounds rather than a one-shot experiment.

## Recommended durable files

```text
program.md
ledger.jsonl
CURRENT_STATUS.md
experiments/NNN/round-log.md
```

## Read order

1. `CURRENT_STATUS.md`
2. `program.md`
3. `ledger.jsonl`
4. relevant templates / constraints

## Required behaviors

- verify baseline before claiming progress
- keep changes attributable when possible
- perform deep analysis after each round
- gate major acceptance through a stronger confirmation path
- update durable files before ending the run
- treat external papers/repos as controlled intake, not automatic truth

## Per-round outputs

- one decision
- one ledger entry
- one round log
- one updated current status snapshot
- one recommended next step

## Stop conditions

- target reached
- plateau detected
- budget exhausted
- blocker requires human decision

## Companion docs

- `docs/methodology.md`
- `docs/acceptance-gates.md`
- `docs/experiment-ledger-spec.md`
- `docs/research-program-template.md`
