# Autoresearch Playbook

A public, reusable playbook for running **automatic research loops** on ML, AI, retrieval, agent, and systems problems.

This repo is inspired by the top-level logic of Karpathy's autoresearch framework:
- fast iteration
- explicit hypotheses
- strict measurement
- evidence-driven updates

But it adds a stronger operating layer for real-world research teams:

- baseline-first discipline
- deep post-round analysis
- explicit acceptance gates
- controlled SOTA intake
- file-based state for resumability
- templates for program, ledger, round logs, and progress reporting

## What this repo is

This is a **public methodology repo**, not a private benchmark dump and not a system-specific experiment log.

It is for people who want to run research loops that are:

- more structured than ad hoc experimentation,
- more reproducible than “agent vibe iteration”,
- more practical than a pure theory note,
- and more robust than a single overnight automation script.

## Core idea

A good autoresearch loop should behave like this:

1. Start from a trustworthy baseline.
2. Change one thing at a time when possible.
3. Measure with a fixed eval path.
4. Do deep analysis after every round.
5. Decide the next step from evidence, not intuition alone.
6. Continuously scan for newer papers/systems, but only adopt them through controlled evaluation.
7. Keep enough durable state that the loop can resume after interruption.

## What this playbook adds beyond a minimal autoresearch loop

### 1. Baseline is sacred
If the baseline is unstable, every downstream conclusion is suspect.

### 2. Deep analysis is mandatory
A round does not end at “metric up” or “metric down”.
It ends when you understand:
- what improved,
- what regressed,
- which slices moved,
- whether the gain is robust,
- and what the next best move is.

### 3. Acceptance gates matter
Fast local evaluation is useful, but major decisions should be gated by a slower, stronger, or more trustworthy confirmation path.

### 4. SOTA intake should be disciplined
New papers and repos should enter through controlled intake, not random adoption.

### 5. Research state should survive resets
A serious autoresearch loop should be resumable from files, not dependent on a transient chat transcript.

---

## Repository contents

```text
.
├── README.md
├── SKILL.md
├── docs/
│   ├── methodology.md
│   ├── acceptance-gates.md
│   ├── experiment-ledger-spec.md
│   └── research-program-template.md
├── research-loop/
│   └── templates/
│       ├── round-log.md
│       └── post-run-analysis.md
└── skill/
    ├── autoresearch-playbook/
    │   └── SKILL.md
    └── research_skill.md
```

## Recommended file layout for a real research loop

```text
my-autoresearch-worktree/
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
    └── ... your system under test ...
```

### Suggested responsibilities

- `program.md` — current goals, constraints, active hypotheses, experiment queue
- `ledger.jsonl` — append-only experiment history
- `CURRENT_STATUS.md` — latest resumable snapshot for humans/agents
- `experiments/NNN/` — per-round artifacts and notes
- `eval_harness.py` — fixed evaluation path, kept stable as long as possible
- `src/` — the system being improved

---

## Documentation map

- **Methodology**: [`docs/methodology.md`](docs/methodology.md)
- **Acceptance gates**: [`docs/acceptance-gates.md`](docs/acceptance-gates.md)
- **Ledger spec**: [`docs/experiment-ledger-spec.md`](docs/experiment-ledger-spec.md)
- **Research program template**: [`docs/research-program-template.md`](docs/research-program-template.md)
- **Round log template**: [`research-loop/templates/round-log.md`](research-loop/templates/round-log.md)
- **Post-run analysis template**: [`research-loop/templates/post-run-analysis.md`](research-loop/templates/post-run-analysis.md)
- **Reusable skill-style prompt**: [`SKILL.md`](SKILL.md)

---

## Who this is for

This playbook is useful if you are running iterative improvement loops on:

- retrieval systems
- memory systems
- agents and tool-use systems
- evaluation pipelines
- model-routing systems
- benchmark optimization programs
- production ML systems where regressions are expensive

---

## What this is not

- not a claim of implementation parity with Karpathy's repo
- not a benchmark leaderboard
- not a private experiment dump
- not tied to any one company, dataset, model provider, or hardware stack

---

## Practical stance

This repo is deliberately opinionated:

- small changes beat giant uncontrolled rewrites
- file-based durability beats transcript-only state
- stronger evaluation beats faster self-congratulation
- controlled external research intake beats novelty chasing
- public methodology should be reusable without private infrastructure

If you want a short description:

> **Autoresearch Playbook is a practical operating system for evidence-driven research loops.**
