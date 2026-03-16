---
name: autoresearch
description: >
  Activate when the user asks to research a repo, optimize a benchmark,
  improve an evaluation score, or run an autoresearch loop. Use this skill for
  durable, evidence-driven experiment programs with discovery, baseline
  verification, iterative experiments, acceptance gates, and resumable state.
---

# AutoResearch Skill

Use this when the task is about repeated benchmark-driven experimentation, not a one-off patch.

## Triggers
- "research this repo"
- "improve benchmark"
- "optimize this eval"
- "autoresearch"

## Workflow
1. Discovery: create/select a research worktree, clone/copy the target, inventory evaluator candidates, write `program.md`.
2. Baseline: run the evaluator repeatedly and record stability in `ledger.jsonl`.
3. Experiment loop: reserve a ledger id, design one focused experiment, run fast validation first, then strong confirmation, then write logs and commit code.
4. Reporting: update `CURRENT_STATUS.md`, write round logs, and report the next move.

## Telescope method
Always progress coarse sweep -> fine-tune -> scale. Never skip fast-subset validation.
