# Research Program Template

Use this as the durable control document for an autoresearch loop.

```markdown
# Research Program

## Goal
[What are we trying to improve?]

## Success metric
- Primary metric:
- Acceptance threshold:
- Secondary metrics / guardrails:

## Constraints
- Allowed files to modify:
- Forbidden files / frozen eval path:
- Latency / cost ceilings:
- Safety / compliance / design invariants:

## Baseline
- Current baseline value:
- Dataset/version:
- Seed/config:
- Known instability / noise band:
- Known failure modes:

## Current hypothesis
[One sentence]

## Current phase
[Calibration / Retrieval / Ranking / Write-path / System integration / Validation / etc.]

## Experiment queue
1. [Highest priority]
2. [Next]
3. [Next]

## Known dead ends
- 
- 

## Acceptance gate
- Local validation rule:
- Strong confirmation rule:
- Critical slice regression rule:

## Plateau rule
- Stop or re-evaluate after:

## Budget
- Time budget:
- Compute budget:
- API / infra budget:

## Reporting cadence
- Per round:
- Daily:
- Plateau / target reached:

## Resume instructions
If the loop is interrupted:
1. Read `CURRENT_STATUS.md`
2. Read `ledger.jsonl`
3. Resume from the highest-priority unfinished experiment
```

---

## Suggested companion files

- `CURRENT_STATUS.md`
- `ledger.jsonl`
- `experiments/NNN/round-log.md`
- `research-loop/templates/post-run-analysis.md`

This file should stay compact, current, and decision-oriented.
