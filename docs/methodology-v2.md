# Research Methodology — Atlas Memory Project

A comprehensive methodology guide distilled from hands-on research experience (2026-03-13 to present). These principles are universal — they apply to any empirical research, not just this project.

## Core Principles

### 1. Telescope Method (粗调→精调→Scaling)
Like using a telescope: coarse adjustment finds the star field, fine adjustment resolves the specific star, then you observe and record.

**Steps:**
1. **Coarse Sweep** — Scan all functions at once with a small sample. Goal: find where the signal IS and where it IS NOT.
   - Example: 9 questions across 3 paths → discovered preference 0pp, multi-session +8pp
2. **Fine-Tune** — Zoom into the weak spot with the NARROWEST possible test to diagnose root cause.
   - Example: 3 failed preference questions → regex vs Gemini → root cause confirmed
3. **Scale** — Only after ALL basic functions are good enough. Scaling amplifies signal, it does not create it.
   - If broken at n=3, still broken at n=500

**Critical rule:** Do NOT skip fine-tuning by jumping from coarse to scale.

### 2. Direction Over Results
Theoretically right direction matters more than early test numbers — until evidence proves the theory wrong.

- A low score with right direction can be improved (implementation fix)
- A high score with wrong direction is a dead end
- When a sound approach tests poorly, ask: is the THEORY wrong, or is the IMPLEMENTATION incomplete?
- Only abandon when the theory itself is disproven

**Example:** Fusion scored 67% (below date-inject 75%), but theory was correct — they solve different failure types. Keep refining, don't abandon.
**Counter-example:** KG fusion scored well on small entity pools but 9 experiments proved theory wrong for large pools. Correctly abandoned.

### 3. Evidence-Driven Decision Making
Every directional decision must cite evidence, never vibes.

- No next step by vibe — cite data from the current experiment
- If 2+ consecutive failures → stop brute-force → re-open assumptions → inspect evaluation
- Post-round 5-question analysis is MANDATORY (see below)

### 4. LLM-First Design Principle
Don't build what AI will do 10x better tomorrow. When a heuristic/regex method shows no results in testing, try the LLM path before diagnosing further.

- Always leave an LLM entry point (`*_llm()`) even when building regex/heuristic
- Regex is speed optimization, not architecture
- `USE_LLM_PRIMARY` flag pattern: easy toggle between LLM and fast path

**Example:** Preference regex: 0pp → Gemini: +16.7pp. The heuristic was just too dumb.

### 5. Single-Variable Experiments
Change ONE thing at a time.

- If you change two things, you cannot attribute the result
- Control everything else
- Use sub-experiment `NNN.M` naming for variants within a theme

### 6. Small Sample Warning
n<30 category-level conclusions are unreliable.

- Phase 3.5 showed "+8.3pp" on multi-session — turned out to be 1 question in n=12 (noise)
- Always report sample size alongside percentages
- Use n≥30 for category-level decisions, n≥100 for overall conclusions

## Operational Rules (D1-D15)

### D1: Reproducibility
Baseline must reproduce within ±1pp before experiments begin.

### D2: Reserved

### D3: Reserved

### D4: Reserved

### D5: Dev Loop
Dev loop uses conv-30 only (105 QA). Full 502 QA reserved for acceptance gate. All LLM calls use configured model from config.json.

### D6: Single Ledger
`autoresearch/ledger.jsonl` is the ONLY authoritative source for experiment numbers. NO split ledgers.

### D7: Non-Blocking Main Session
Never block main session — mandatory hard rule. Use subagents, tmux, screen for long tasks.

### D8: Incremental Validation
Split tests by conversation/category, with decision points between each. Run small → analyze → decide → next segment.

### D9: Single Source of Truth for Models
`autoresearch/config.json` is single source of truth for model selection.

### D10: Mandatory Post-Round Analysis
5 questions after EVERY experiment before next:
1. Did the primary metric improve?
2. Which slices improved or regressed?
3. What changed in the failure distribution?
4. How strong is the signal?
5. What is the best next move? (cite evidence from Q1-4)

### D11: Run Logging
Every experiment writes `run.log` with per-question detail, progress every 10 items, flush=True.

### D12: Sub-Experiment Naming
`NNN.M` naming for sub-experiments. Independent scoring, hybrid human+LLM design.

### D13: SOTA Awareness
SOTA scan must include adversarial/unanswerable defense, hallucination guard, abstention.

### D14: Data Quality Audit
Pre-experiment gate for data pipeline experiments. Audit before you build.

### D15: Failure Case Sampling
Post-REJECT mandatory. Sample 5-10 failures, classify error type before designing next experiment.

## Acceptance Gate
- No experiment ACCEPT'd without external re-judge (gpt-4o-mini) confirmation showing ≥+1pp over external baseline
- SOTA Intake: Every 3 experiments or 2+ consecutive REJECT → mandatory SOTA scan
- Plateau Protocol: 2+ consecutive REJECT → stop → SOTA scan → re-open assumptions → inspect eval → resume

## Dual-Lane System
- **Auto lane** (cron): Mechanical experiments, cannot final ACCEPT (only PENDING_REVIEW)
- **Manual lane** (main session): Direction, architecture, final decisions
- Same ledger, `lane` field distinguishes
- Auto lane checks for manual RUNNING before starting

## Cross-Benchmark Validation
When improvements are developed on one benchmark:
1. Smoke test on BOTH benchmarks (telescope step 1)
2. POC on both (telescope step 2)
3. Full scale on both (telescope step 3)
Never assume improvements transfer without validation.

## Key Findings (Permanent)
- **Embedding fatal flaw for temporal:** Returns most-discussed, not first-occurrence. Keyword search needed for temporal ordering.
- **Judge calibration ≠ retrieval quality:** Exp-012 +15.4pp was judge fix, not retrieval improvement.
- **Write-side data quality is the real bottleneck:** KG data too poor for structured queries.
- **Prompt-level fixes can be huge:** Temporal date-inject = +33pp with zero retrieval change.
- **Iterative retrieval for aggregation:** Search → identify gaps → follow-up → merge → synthesize.

---

_This document is living. Update it as new principles are learned._
_Last updated: 2026-03-16_
