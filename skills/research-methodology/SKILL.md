---
name: research-methodology
description: Research methodology for experiment design, research planning, methodology compliance, post-round analysis, telescope method, evidence-driven decisions, acceptance gates, LLM-first design, single-variable experiments, failure case sampling, cross-benchmark validation, and SOTA scanning. Use when planning experiments, reviewing results, diagnosing failures, or making directional research decisions.
---

# Research Methodology

Core principles for empirical research. These are universal — they apply to any iterative experiment loop, not just one project.

## 1. Telescope Method (Coarse → Fine-Tune → Scale)

Like a telescope: coarse adjustment finds the star field, fine adjustment resolves the target, then you observe.

1. **Coarse Sweep** — Scan all functions/categories at once with a small sample. Goal: find where the signal IS and where it IS NOT.
   - Example: 9 questions across 3 categories → discovered Category A at 0pp improvement, Category B at +8pp.
2. **Fine-Tune** — Zoom into the weak spot with the NARROWEST possible test to diagnose root cause.
   - Example: 3 failed items from Category A → tested heuristic vs LLM approach → confirmed heuristic was the bottleneck.
3. **Scale** — Only after ALL basic functions are good enough. Scaling amplifies signal, it does not create it.
   - If broken at n=3, still broken at n=500.

**Critical rule:** Do NOT skip fine-tuning by jumping from coarse to scale.

## 2. Direction Over Results

Theoretically right direction matters more than early test numbers — until evidence proves the theory wrong.

- A low score with right direction can be improved (implementation fix).
- A high score with wrong direction is a dead end.
- When a sound approach tests poorly, ask: is the THEORY wrong, or is the IMPLEMENTATION incomplete?
- Only abandon when the theory itself is disproven.

**Guideline:** If an approach scores below the current best but the theory is sound and it addresses a different failure mode, keep refining. If N experiments show the theory itself doesn't hold at scale, abandon it.

## 3. Evidence-Driven Decision Making

Every directional decision must cite evidence, never vibes.

- No next step by vibe — cite data from the current experiment.
- If 2+ consecutive failures → stop brute-force → re-open assumptions → inspect evaluation.
- Post-round 5-question analysis is **MANDATORY** (see D10 in `references/operational-rules.md`).

### Mandatory 5-Question Post-Round Analysis

After EVERY experiment, before designing the next:

1. Did the primary metric improve?
2. Which slices improved or regressed?
3. What changed in the failure distribution?
4. How strong is the signal? (sample size, confidence)
5. What is the best next move? (cite evidence from Q1-4)

## 4. LLM-First Design Principle

Don't build what AI will do 10x better tomorrow. When a heuristic/regex method shows no results in testing, try the LLM path before diagnosing further.

- Always leave an LLM entry point (`*_llm()`) even when building a heuristic version.
- Heuristics are speed optimizations, not architecture.
- `USE_LLM_PRIMARY` flag pattern: easy toggle between LLM and fast path.
- If tomorrow's model is 10x better, your system should benefit with zero code changes.

**Proven pattern:** Heuristic extraction scored 0pp improvement → LLM extraction scored +16.7pp. The heuristic was just too dumb for the task.

## 5. Single-Variable Experiments

Change ONE thing at a time.

- If you change two things, you cannot attribute the result.
- Control everything else.
- Use sub-experiment `NNN.M` naming for variants within a theme (see D12).

## 6. Small Sample Warning

n<30 category-level conclusions are unreliable.

- A "+8pp" improvement can turn out to be 1 flipped question in n=12 (noise).
- Always report sample size alongside percentages.
- Use n≥30 for category-level decisions, n≥100 for overall conclusions.

## 7. Cross-Benchmark Validation

When improvements are developed on one benchmark:

1. Smoke test on ALL benchmarks (telescope step 1).
2. POC on all (telescope step 2).
3. Full scale on all (telescope step 3).

Never assume improvements transfer without validation.

## 8. Acceptance Gate

- No experiment ACCEPT'd without external re-evaluation confirmation showing improvement over the external baseline.
- Internal evaluation is a hypothesis; external confirmation is evidence.
- **SOTA Intake:** Every 3 experiments or 2+ consecutive REJECT → mandatory SOTA scan.
- **Plateau Protocol:** 2+ consecutive REJECT → stop → SOTA scan → re-open assumptions → inspect eval → resume.

## 9. Failure Case Sampling (Post-REJECT Mandatory)

After every REJECT, before designing the next experiment, **sample 5-10 failure cases** and classify the error type:

1. **Retrieval miss** — correct answer exists but wasn't retrieved (recall problem).
2. **Retrieval noise** — correct answer retrieved but buried (ranking problem).
3. **Generation error** — correct context retrieved, model generated wrong answer.
4. **Data gap** — information needed doesn't exist in stored data (pipeline problem).
5. **Grounding failure** — system hallucinated instead of abstaining.

Record the distribution. This tells you WHERE in the pipeline to focus, instead of guessing.

## 10. Dual-Lane System (Multi-Agent)

- **Auto lane** (cron/subagent): Mechanical experiments, cannot final ACCEPT (only PENDING_REVIEW).
- **Manual lane** (main session): Direction, architecture, final decisions.
- Same ledger, `lane` field distinguishes.
- Auto lane checks for manual RUNNING before starting.

## Key Findings (Permanent Reference)

These are hard-won lessons that apply broadly:

- **Embedding similarity ≠ temporal ordering.** Embedding search returns most-discussed items, not chronologically first. Use keyword/date-filtered search for temporal queries.
- **Judge calibration ≠ retrieval quality.** A large metric improvement can come entirely from fixing the evaluation judge, not from actual retrieval improvement. Always distinguish.
- **Write-side data quality is the real bottleneck.** If upstream data is garbage, no downstream query approach can fix it. Audit data before experimenting on retrieval.
- **Prompt-level fixes can be massive.** A simple prompt change (e.g., injecting dates) can yield +30pp with zero retrieval changes. Don't over-engineer retrieval when a prompt fix suffices.
- **Iterative retrieval for aggregation.** For "list all X" queries: search → identify gaps → follow-up search → merge → synthesize. Single-pass retrieval misses items.

## Operational Rules

Detailed operational rules (D1-D15) covering reproducibility, dev loops, logging, sub-experiments, data quality audits, and more are in `references/operational-rules.md`.
