# Automatic Research Methodology

## 0) Overall logic

This playbook aligns with the high-level logic of autoresearch:

- iterate quickly,
- measure strictly,
- make hypotheses explicit,
- and update direction from evidence.

The extension here is operational discipline:

- baseline-first thinking,
- deep post-round analysis,
- controlled SOTA intake,
- acceptance gates,
- and durable state for resumability.

---

## 1) Baseline must be trustworthy

Before optimization begins:

- lock the task definition,
- lock the dataset/split/version,
- verify reproducibility,
- document failure modes,
- and confirm baseline stability across reruns.

**Rule:** if the baseline is unreliable, downstream conclusions are unreliable.

---

## 2) Every round must end in analysis, not just execution

Each round should answer at least five questions:

1. Did the primary metric improve?
2. Which slices improved or regressed?
3. What changed in the failure distribution?
4. How strong is the signal?
5. What is the best next move?

**Rule:** no “next step by vibe”. Every directional update should cite evidence.

---

## 3) Keep changes attributable

When possible:

- one hypothesis per round,
- one focused code/config change,
- one stable evaluation path,
- one clear decision.

This keeps the loop interpretable and makes rollback easy.

---

## 4) Separate fast validation from strong confirmation

Use at least two quality layers when stakes are meaningful:

- **fast validation path** — cheaper, faster, more frequent
- **strong confirmation path** — slower, more trustworthy, used before major acceptance

This prevents local overfitting to a weak internal judge.

---

## 5) Continuous SOTA scanning, but controlled adoption

In every round or every few rounds:

- scan new papers,
- scan relevant repos,
- scan benchmark reports,
- identify promising ideas,
- deep-dive only when the expected value is high.

**Rule:** novelty enters through controlled evaluation, not blind adoption.

---

## 6) Durable files beat transient session memory

A serious autoresearch loop should survive:

- chat resets,
- process restarts,
- machine reboots,
- human handoff,
- long-running experiment gaps.

Recommended durable files:

- `program.md`
- `ledger.jsonl`
- `CURRENT_STATUS.md`
- `experiments/NNN/round-log.md`

**Rule:** if a new session cannot resume the work from files alone, the loop is under-documented.

---

## 7) Suggested operating rhythm

### Per experiment round
- verify baseline when needed
- run one controlled change
- record metrics
- perform deep analysis
- write decision and next step

### Per day
- summarize what was learned
- re-rank backlog
- scan external developments
- decide whether current line still has gradient

### On plateau
- stop brute-force looping
- re-open assumptions
- inspect eval validity
- widen search space or redesign the problem decomposition

---

## 8) Typical failure modes

### Baseline drift
What looked like improvement was only a changed baseline.

### Multi-variable confusion
Too many simultaneous changes prevent attribution.

### Weak-judge overfitting
The system learns how to satisfy a cheap proxy but not the true objective.

### Shallow reporting
Headline metric improves, but important slices regress.

### Transcript-only state
The research loop becomes unrecoverable after interruption.

### Novelty chasing
External ideas are adopted before being tested against local constraints.

---

## 9) Practical summary

A good autoresearch loop is not just:

> generate experiment → run eval → repeat

It is:

> establish truth → test carefully → analyze deeply → update direction → preserve state → repeat

That is the core purpose of this repo.

---

## 10) Multi-agent coordination: single ledger principle (D6)

### Problem

When multiple agents (main session, cron monitors, subagents) run experiments
concurrently, a subagent may create a separate ledger file or a secondary tracking
mechanism. This causes experiment numbering to diverge — one agent thinks Exp-006
is running while another reports Exp-007. Zombie processes run undetected because
no single view of truth exists.

### Rule

- One single ledger file (`ledger.jsonl`) is the **ONLY** authority for experiment numbers.
- **NO** split or secondary ledger files allowed under any circumstances.
- Every experiment **MUST** write a ledger entry (`verdict=RUNNING`) **BEFORE** starting execution.
- Every experiment **MUST** git commit + push after completion, abort, or kill.
- Old experiments **MUST** be marked in the ledger (`KILLED`/`ABORTED`) before being superseded.
- All agents (main, cron, subagent) read and write the **same** ledger file.

### Why this matters

Multi-agent systems with shared state need a single source of truth. Without it,
agents independently evolve their own view of reality, leading to:

- **Divergent numbering** — different agents assign different experiment IDs
- **Zombie processes** — old experiments run undetected because no agent owns their lifecycle
- **Incorrect status reports** — the human receives conflicting information about what is running

This is a general principle for any autonomous research system that uses multiple
concurrent agents or scheduled monitors.
