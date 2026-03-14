---
name: autoresearch-playbook
description: >
  Run an evidence-driven autoresearch loop for improving a model, system,
  retrieval stack, agent workflow, or benchmarked pipeline. Use when planning,
  executing, analyzing, and reporting iterative research rounds with strong
  baseline discipline, acceptance gates, resumable state, and controlled
  external research intake.
---

# Autoresearch Playbook Skill

Use this skill when the task is not “do one experiment”, but:

- define a research loop,
- run repeated experiment rounds,
- evaluate improvements against a stable baseline,
- maintain a durable experiment ledger,
- decide next steps from evidence,
- and keep progress resumable after interruptions.

## Core operating rules

1. **Baseline first**
   - Verify the baseline before claiming improvement.
   - If the baseline is unstable, stop and fix evaluation.

2. **One hypothesis per round when possible**
   - Keep diffs attributable.
   - Large mixed changes are allowed only when explicitly justified.

3. **Frozen eval path**
   - Keep the evaluation harness stable across rounds.
   - Change the harness only in clearly separated eval-maintenance work.

4. **Deep analysis required**
   - Do not stop at a headline metric.
   - Check slices, regressions, robustness, failure clusters, and cost/latency tradeoffs.

5. **Acceptance gates**
   - Fast local validation is not enough for major decisions.
   - Important gains should pass a stronger confirmation path.

6. **Durable state over transcript memory**
   - Keep `program.md`, `ledger.jsonl`, and `CURRENT_STATUS.md` up to date.
   - Assume the session can reset at any time.

7. **Controlled SOTA intake**
   - Scan new papers/repos continuously.
   - Only adopt ideas after explicit evaluation, not by novelty impulse.

## Recommended persistent worktree

```text
project-autoresearch/
├── program.md
├── ledger.jsonl
├── CURRENT_STATUS.md
├── experiments/
│   └── NNN/
│       ├── round-log.md
│       └── diff.patch
├── eval/
│   └── eval_harness.py
└── src/
```

## Read order on each invocation

1. `CURRENT_STATUS.md` — current state snapshot
2. `program.md` — goals, constraints, active hypotheses, queue
3. `ledger.jsonl` — historical experiment record
4. relevant templates / design constraints

## Loop skeleton

```text
while not stop_condition:
    read current status
    verify baseline if needed
    choose next experiment
    make controlled change
    run evaluation
    analyze deeply
    apply acceptance gate
    append ledger
    write round log
    update CURRENT_STATUS
```

## Stop conditions

Stop and report when any of the following happens:

- target reached
- plateau detected
- budget exhausted
- evaluation invalidated
- blocker requires human input

## Minimal outputs per round

Every round should produce:

- a decision (`accept`, `reject`, `explore`, or `blocked`)
- a ledger entry
- a round log
- an updated current status snapshot
- a proposed next step

## Use with this repo

See:
- `docs/methodology.md`
- `docs/acceptance-gates.md`
- `docs/experiment-ledger-spec.md`
- `docs/research-program-template.md`
- `research-loop/templates/round-log.md`
- `research-loop/templates/post-run-analysis.md`
