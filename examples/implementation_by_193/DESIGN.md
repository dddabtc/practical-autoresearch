# AutoResearch System - Design Document

## Overview
An OpenClaw skill that turns a one-sentence research request into a fully autonomous research loop.
User says: "research this repo and improve the benchmark to 90%"
System does everything else.

## User Experience
1. User gives a research target (repo URL, essay, paper) + goal (e.g. "improve benchmark to 90%")
2. System auto-discovers: codebase structure, benchmarks, eval harness, baseline
3. System runs iterative experiment loops following practical-autoresearch methodology
4. User gets Telegram notifications at key decision points
5. System stops when target reached, plateau detected, or budget exhausted

## Architecture

### Entry Point: OpenClaw Skill
- SKILL.md triggers on research/benchmark/improve/optimize requests
- Reads target, establishes worktree, kicks off the loop

### Phase 1: Discovery
- Clone/read the target repo or essay
- Identify: what is being measured, how (eval harness), current baseline
- If no eval harness exists, create one
- Write program.md with goals, constraints, baseline

### Phase 2: Baseline Verification
- Run eval harness, record baseline metrics
- Verify stability (run 2-3 times, check variance)
- Write baseline to ledger.jsonl
- Update CURRENT_STATUS.md

### Phase 3: Experiment Loop (auto lane)
For each round:
  a. Read CURRENT_STATUS.md + ledger.jsonl + program.md
  b. LLM designs next experiment (hypothesis + code change)
  c. Telescope method: coarse sweep first, then fine-tune
  d. Spawn coding agent to implement the change
  e. Run eval harness
  f. Deep 5-question analysis (LLM-driven)
  g. Acceptance gate: accept/reject/explore
  h. Append ledger, write round-log, update status
  i. If plateau (2+ consecutive rejects): SOTA scan, re-open assumptions
  j. Check stop conditions (target reached / budget / plateau)

### Phase 4: Reporting
- Per round: Telegram summary (metric delta, decision, next step)
- On target reached: full report with all accepted changes
- On plateau: notify user with analysis, ask for direction

## File Structure (per research project)
```
~/.openclaw/workspace/research/<project-name>/
├── program.md              # goals, constraints, hypotheses, queue
├── ledger.jsonl            # append-only experiment history
├── CURRENT_STATUS.md       # resumable snapshot
├── experiments/
│   └── NNN/
│       ├── round-log.md    # detailed per-round narrative
│       ├── post-run-analysis.md
│       └── diff.patch      # code changes
├── eval/
│   └── eval_harness.py     # evaluation script (discovered or created)
└── src/                    # working copy of target code
```

## Key Design Decisions
1. LLM-driven experiment design (not just parameter sweeps)
2. Coding agent for code changes (spawn claude/codex)
3. All state in files + git (survives restarts)
4. Telescope method built into loop logic
5. Dual validation: fast local + strong confirmation
6. Auto SOTA scan on plateau
7. Single ledger principle for multi-agent coordination

## Technology
- Python 3 for engine (loop, analysis, ledger, gate logic)
- OpenClaw skill for entry point
- OpenClaw cron for auto lane scheduling
- Coding agents (claude/codex) for code modifications
- Web search for SOTA scanning
- Git for state management

## Stop Conditions
- Target metric reached
- Budget exhausted (time or compute)
- Plateau: 3+ consecutive rejects with no new direction
- User intervention requested
