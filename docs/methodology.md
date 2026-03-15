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

## 11. Incremental Validation (D8)

Large benchmark runs must be split into segments with **decision points** between each.

**Pattern:**
1. Run segment A (smallest, fastest) → analyze results
2. **Decision point:** metrics OK? → continue to segment B. Metrics bad? → stop, diagnose, fix
3. Run segment B → analyze results  
4. **Decision point:** consistent with A? → continue to C. Diverged? → investigate
5. Repeat until all segments pass or a fix is needed

**Why:**
- A full blind run that fails at 60% wastes the remaining 40% of compute time
- Each segment provides actionable signal: which question types fail, which conversations are harder
- Fixing a problem after 15 minutes is cheaper than after 3 hours
- Splitting doesn't add total time (segments sum to full run) but adds decision opportunities

**Rule:** Never launch a full benchmark run without first validating on a fast subset. If the subset passes, expand incrementally.

## 12. Mandatory Experiment Logging (D11)

Every experiment **MUST** write a log file for monitoring and post-mortem analysis.

**Log file:** `experiments/NNN/run.log`

**What to log:**
- **At startup:** timestamp, hypothesis, config/parameters
- **Per item:** item number, result, score
- **Progress checkpoint:** every N items (e.g., every 10) — cumulative stats so far
- **At completion:** summary stats, total runtime, final verdict

**Implementation rules:**
- Use `flush=True` / unbuffered output so `tail -f run.log` works in real time
- Never rely on agent announce alone — the log file is the **primary record**
- If the experiment crashes, the log file is your post-mortem; session transcripts may be lost

**Why:**
Experiments 008–010 showed that without persistent logging, crashed or long-running experiments
leave no trace. The agent's announce message may never arrive if the session dies. A log file
on disk is the only reliable record of what happened.

## 13. Sub-experiment Structure (D12)

Experiments may have **sub-experiments** when testing variants of the same hypothesis.

**Naming convention:** `NNN.M` (e.g., 010.1, 010.2, 010.3)
- Main experiment number = hypothesis direction
- Sub-experiment number = specific implementation variant

**Rules:**
- Each sub-experiment is independently scored with its own metrics
- Main experiment verdict is based on the **best sub-experiment result**
- Human sets the main hypothesis; LLM can auto-generate variant designs (hybrid approach)
- Sub-experiments share the same `experiments/NNN/` directory with clearly labeled outputs
- Each sub-experiment should have its own log: `experiments/NNN/run_NNN.M.log`

**When to use:**
- Testing multiple prompt variants for the same strategy
- Comparing parameter settings (e.g., different chunk sizes, thresholds)
- A/B testing implementation approaches for one idea

**When NOT to use:**
- Fundamentally different hypotheses → use separate experiment numbers
- Sequential refinements where each builds on the last → use separate rounds

## 14. SOTA Scan: Adversarial & Unanswerable Defense (D13)

When performing SOTA scans (per Section 5), **specifically search for**:

- How SOTA systems handle **adversarial/unanswerable questions**
- **RAG hallucination guard** / faithfulness checking methods
- **Abstention mechanisms** ("I don't know" strategies, refusal calibration)
- **Grounding verification** approaches (checking answers against retrieved evidence)

**Why:**
Experiments 008–010 revealed that adversarial and unanswerable questions are a major
failure category. Standard SOTA scans focus on accuracy improvement but miss the
equally important problem of knowing when NOT to answer. Systems that always produce
an answer score worse on benchmarks that penalize hallucinated responses to
unanswerable questions.
