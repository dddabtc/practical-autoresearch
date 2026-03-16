# Automatic Research Methodology

## 0) Overall Logic

This methodology aligns with the high-level logic of autoresearch:

- iterate quickly,
- measure strictly,
- make hypotheses explicit,
- and update direction from evidence.

The extension here is operational discipline:

- baseline-first thinking,
- telescope method for efficient search,
- direction over early results,
- deep post-round analysis,
- controlled SOTA intake,
- acceptance gates,
- LLM-first design,
- and durable state for resumability.

---

## 1) Baseline Must Be Trustworthy

Before optimization begins:

- lock the task definition,
- lock the dataset/split/version,
- verify reproducibility,
- document failure modes,
- and confirm baseline stability across reruns.

**Rule:** if the baseline is unreliable, downstream conclusions are unreliable.

---

## 2) Telescope Method: Coarse → Fine-Tune → Scale

Like using a telescope: coarse adjustment finds the star field, fine adjustment resolves the target, then you observe.

1. **Coarse Sweep** — Scan all functions/categories at once with a small sample. Goal: find where the signal IS and where it IS NOT.
   - Example: Run a handful of test items across all categories → discover which categories show improvement and which show zero effect.
2. **Fine-Tune** — Zoom into the weak spot with the narrowest possible test to diagnose root cause.
   - Example: Take 3-5 failures from the weak category → test alternative approaches → confirm which component is the bottleneck.
3. **Scale** — Only after all basic functions are good enough. Scaling amplifies signal, it does not create it.
   - If broken at n=3, still broken at n=500.

**Critical rule:** Do NOT skip fine-tuning by jumping from coarse to scale.

---

## 3) Direction Over Results

Theoretically right direction matters more than early test numbers — until evidence proves the theory wrong.

- A low score with right direction can be improved (implementation fix).
- A high score with wrong direction is a dead end.
- When a sound approach tests poorly, ask: is the THEORY wrong, or is the IMPLEMENTATION incomplete?
- Only abandon when the theory itself is disproven.

**Guideline:** If an approach addresses a real failure mode but underperforms the current best, refine it — the theory may be right while the implementation is incomplete. But if N experiments consistently show the theory doesn't hold, abandon it.

---

## 4) Every Round Must End in Analysis

Each round should answer at least five questions:

1. Did the primary metric improve?
2. Which slices improved or regressed?
3. What changed in the failure distribution?
4. How strong is the signal?
5. What is the best next move?

**Rule:** no "next step by vibe". Every directional update should cite evidence.

---

## 5) Keep Changes Attributable

When possible:

- one hypothesis per round,
- one focused code/config change,
- one stable evaluation path,
- one clear decision.

This keeps the loop interpretable and makes rollback easy.

---

## 6) Separate Fast Validation from Strong Confirmation

Use at least two quality layers when stakes are meaningful:

- **fast validation path** — cheaper, faster, more frequent
- **strong confirmation path** — slower, more trustworthy, used before major acceptance

This prevents local overfitting to a weak internal judge.

**Warning:** A large metric improvement can come from fixing the evaluation judge, not from actual system improvement. Always distinguish judge calibration from true gains.

---

## 7) LLM-First Design

Don't build what AI will do 10x better tomorrow. When a heuristic/rule-based method shows no results in testing, try the LLM path before diagnosing further.

- Always leave an LLM entry point even when building a heuristic version.
- Heuristics are speed optimizations, not architecture.
- Use a `USE_LLM_PRIMARY` flag pattern for easy toggling.
- Build for the future capability curve: if tomorrow's model is 10x better, your system should benefit with zero code changes.

**Proven pattern:** A rule-based extraction method scored 0pp improvement while an LLM-based approach on the same task scored +16pp. The heuristic was simply too dumb for the task's complexity.

---

## 8) Small Sample Warning

n<30 category-level conclusions are unreliable.

- A "+8pp" category improvement can be a single flipped item in n=12 (noise).
- Always report sample size alongside percentages.
- Use n≥30 for category-level decisions, n≥100 for overall conclusions.

---

## 9) Continuous SOTA Scanning, Controlled Adoption

In every round or every few rounds:

- scan new papers,
- scan relevant repos,
- scan benchmark reports,
- identify promising ideas,
- deep-dive only when the expected value is high.

Specifically search for:

- adversarial/unanswerable defense strategies,
- hallucination guard / faithfulness checking,
- abstention mechanisms,
- grounding verification.

**Rule:** novelty enters through controlled evaluation, not blind adoption.

---

## 10) Cross-Benchmark Validation

When improvements are developed on one benchmark:

1. Smoke test on ALL benchmarks (telescope step 1).
2. POC on all (telescope step 2).
3. Full scale on all (telescope step 3).

Never assume improvements transfer without validation.

---

## 11) Durable Files Beat Transient Session Memory

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

## 12) Suggested Operating Rhythm

### Per experiment round
- verify baseline when needed
- run one controlled change (single variable)
- record metrics
- perform deep 5-question analysis
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

## 13) Typical Failure Modes

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

### Small-sample mirage
Large percentage improvements on tiny subsets turn out to be noise.

### Premature abandonment
Approaches with sound theory abandoned due to poor early implementation, before the theory itself is disproven.

---

## 14) Multi-agent Coordination: Single Ledger Principle

When multiple agents run experiments concurrently:

- One single ledger file is the **ONLY** authority for experiment numbers.
- **NO** split or secondary ledger files allowed.
- Every experiment MUST write a ledger entry BEFORE starting execution.
- Every experiment MUST commit after completion, abort, or kill.
- Old experiments MUST be marked before being superseded.
- All agents read and write the SAME ledger.

**Why:** Without a single source of truth, agents independently evolve their own view of reality → divergent numbering, zombie processes, conflicting status reports.

---

## 15) Incremental Validation

Large benchmark runs must be split into segments with **decision points** between each.

1. Run segment A (smallest, fastest) → analyze results
2. Decision point: metrics OK → continue. Metrics bad → stop, diagnose, fix.
3. Run segment B → analyze.
4. Decision point: consistent with A → continue. Diverged → investigate.
5. Repeat until all segments pass or a fix is needed.

**Rule:** Never launch a full run without first validating on a fast subset.

---

## 16) Mandatory Experiment Logging

Every experiment MUST write a persistent log file.

- At startup: timestamp, hypothesis, config/parameters.
- Per item: item number, result, score.
- Progress checkpoint: every N items — cumulative stats.
- At completion: summary stats, total runtime, final verdict.
- Use unbuffered output so `tail -f` works in real time.
- The log file is the PRIMARY record; session transcripts may be lost.

---

## 17) Sub-experiment Structure

Experiments may have sub-experiments when testing variants of the same hypothesis.

- Naming: `NNN.M` (e.g., 005.1, 005.2, 005.3).
- Each sub-experiment is independently scored.
- Main experiment verdict based on the best sub-experiment result.
- Use for: multiple prompt variants, parameter settings, implementation approaches.
- Do NOT use for: fundamentally different hypotheses or sequential refinements.

---

## 18) Data Quality Audit: Pre-experiment Gate

Before any experiment that depends on a data pipeline, MUST audit:

1. Schema check: all expected tables/columns present and populated?
2. Sample inspection: pull 10 random records, manually verify.
3. Format consistency: dates, entity names, type labels.
4. Coverage check: what % of source data made it through?
5. Link integrity: can you trace from structured record → source → original text?

**Rule:** No downstream experiment may begin until audit passes. This is a gate, not a suggestion.

---

## 19) Failure Case Sampling: Post-REJECT Mandatory

After every REJECT, sample 5-10 failures and classify:

1. **Retrieval miss** — correct answer exists but wasn't retrieved.
2. **Retrieval noise** — correct answer retrieved but buried.
3. **Generation error** — correct context retrieved, model answered wrong.
4. **Data gap** — information doesn't exist in stored data.
5. **Grounding failure** — system hallucinated instead of abstaining.

Record the distribution. This tells you WHERE in the pipeline to focus.

**Rule:** No next-experiment design after a REJECT without failure sampling.

---

## 20) Acceptance Gate

- No experiment accepted without external re-evaluation confirmation.
- Internal evaluation is a hypothesis; external confirmation is evidence.
- Every 3 experiments or 2+ consecutive failures → mandatory SOTA scan.
- Plateau protocol: 2+ consecutive failures → stop → SOTA scan → re-open assumptions → inspect eval → resume.

---

## 21) Practical Summary

A good autoresearch loop is not just:

> generate experiment → run eval → repeat

It is:

> establish truth → telescope into signal → test carefully → analyze deeply → update direction → preserve state → repeat

---

_This document is living. Update it as new principles are learned._


## Dual Validation (Design Spec ↔ External Research)

When your project has a design specification, treat it as equal-weight evidence alongside external research. Analyze both in the same framework to find convergence or divergence.

- Design spec = hypothesis from first principles
- External research (SOTA papers, prior art) = independent evidence
- **Convergence** (both agree) → strong signal, move fast
- **Only one source** → gather more evidence before committing
- **Conflict** → investigate which is wrong

Put both in the SAME analysis framework. Side-by-side analysis reveals convergence faster than treating them sequentially. Don't treat external research as the sole source of direction while ignoring your own design, or vice versa.
