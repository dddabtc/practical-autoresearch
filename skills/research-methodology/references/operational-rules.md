# Operational Rules (D1–D15)

Detailed rules for running a disciplined research loop. These complement the core principles in SKILL.md.

## D1: Reproducibility

Baseline must reproduce within ±1pp before experiments begin. If baseline drifts, stop and fix before continuing.

## D2–D4: Reserved

Reserved for future operational rules.

## D5: Dev Loop

Use a fast development subset (e.g., 20-30% of full dataset) for iterating. Reserve the full dataset for the acceptance gate. All LLM calls use a configured model from a single config source.

## D6: Single Ledger

One single ledger file (e.g., `ledger.jsonl`) is the **ONLY** authority for experiment numbers.

- NO split or secondary ledger files allowed under any circumstances.
- Every experiment MUST write a ledger entry (`verdict=RUNNING`) BEFORE starting execution.
- Every experiment MUST commit after completion, abort, or kill.
- Old experiments MUST be marked (`KILLED`/`ABORTED`) before being superseded.
- All agents (main, cron, subagent) read and write the SAME ledger.

**Why:** Multi-agent systems with shared state need a single source of truth. Without it, agents independently evolve their own view of reality → divergent numbering, zombie processes, conflicting status reports.

## D7: Non-Blocking Main Session

Never block the main session with long-running operations. Use subagents, tmux, or screen for anything over ~60 seconds.

## D8: Incremental Validation

Large runs MUST be split into segments with decision points between each.

**Pattern:**
1. Run segment A (smallest, fastest) → analyze results.
2. **Decision point:** metrics OK → continue. Metrics bad → stop, diagnose, fix.
3. Run segment B → analyze.
4. **Decision point:** consistent with A → continue. Diverged → investigate.
5. Repeat until all segments pass or a fix is needed.

**Why:** A full blind run that fails at 60% wastes the remaining 40%. Each segment provides actionable signal. Fixing after 15 minutes is cheaper than after 3 hours.

## D9: Single Source of Truth for Models

Use a single config file for model selection. No hardcoded model names scattered across scripts.

## D10: Mandatory Post-Round Analysis

5 questions after EVERY experiment before starting the next:

1. Did the primary metric improve?
2. Which slices improved or regressed?
3. What changed in the failure distribution?
4. How strong is the signal? (sample size, confidence interval)
5. What is the best next move? (cite evidence from Q1-4)

**Rule:** No "next step by vibe." Every directional update must cite observed data.

## D11: Run Logging

Every experiment MUST write a persistent log file.

**What to log:**
- At startup: timestamp, hypothesis, config/parameters.
- Per item: item number, result, score.
- Progress checkpoint: every N items — cumulative stats so far.
- At completion: summary stats, total runtime, final verdict.

**Rules:**
- Use `flush=True` / unbuffered output so `tail -f` works in real time.
- The log file is the PRIMARY record. Agent announces may never arrive if the session dies.
- If the experiment crashes, the log is your post-mortem.

## D12: Sub-Experiment Naming

`NNN.M` naming for sub-experiments (e.g., 005.1, 005.2, 005.3).

- Main experiment number = hypothesis direction.
- Sub-experiment number = specific implementation variant.
- Each sub-experiment is independently scored.
- Main experiment verdict based on the BEST sub-experiment result.
- Human sets the main hypothesis; agent can auto-generate variant designs.

**When to use:** Multiple prompt variants, parameter settings, or implementation approaches for one idea.
**When NOT to use:** Fundamentally different hypotheses (use separate experiment numbers) or sequential refinements (use separate rounds).

## D13: SOTA Awareness

SOTA scans must specifically search for:

- How SOTA systems handle **adversarial/unanswerable inputs**.
- **Hallucination guard** / faithfulness checking methods.
- **Abstention mechanisms** ("I don't know" strategies).
- **Grounding verification** (checking outputs against retrieved evidence).

Standard scans focus on accuracy but miss the equally important problem of knowing when NOT to produce an answer.

## D14: Data Quality Audit (Pre-Experiment Gate)

Before any experiment that depends on a data pipeline, MUST audit:

1. **Schema check:** All expected tables/columns present and populated?
2. **Sample inspection:** Pull 10 random records, manually verify correctness.
3. **Format consistency:** Dates (ISO 8601?), entity names (normalized?), type labels (controlled vocabulary?).
4. **Coverage check:** What % of source data made it through the pipeline?
5. **Link integrity:** Can you trace from structured record → source → original text?

**Rule:** No downstream experiment may begin until the data quality audit passes. This is a gate, not a suggestion.

## D15: Failure Case Sampling (Post-REJECT Mandatory)

After every REJECT, before designing the next experiment, sample 5-10 failures and classify:

1. **Retrieval miss** — correct answer exists but wasn't retrieved.
2. **Retrieval noise** — correct answer retrieved but buried.
3. **Generation error** — correct context retrieved, model generated wrong answer.
4. **Data gap** — information doesn't exist in stored data.
5. **Grounding failure** — system hallucinated instead of abstaining.

Record the distribution in the round-log. This tells you WHERE to focus.

**Rule:** No next-experiment design after a REJECT without a failure case sample and error-type distribution.
