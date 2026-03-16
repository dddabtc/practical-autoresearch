# AutoResearch

An autonomous research engine that turns a one-sentence request into a durable, evidence-driven experiment loop. Built on the [practical-autoresearch](https://github.com/dddabtc/practical-autoresearch) methodology.

> "Research this repo and improve the benchmark to 90%"

The system handles everything: discovery → baseline → experiment loop → analysis → reporting.

## Architecture

```
User request
    │
    ▼
┌─────────────┐
│  Discovery   │  Clone repo, find eval harness, write program.md
└──────┬──────┘
       ▼
┌─────────────┐
│  Baseline    │  Run eval N times, verify stability, record to ledger
└──────┬──────┘
       ▼
┌─────────────────────────────────────────┐
│  Experiment Loop (telescope method)      │
│                                          │
│  1. LLM designs next experiment          │
│  2. Apply code change (unified diff)     │
│  3. Fast validation (small subset)       │
│  4. Strong confirmation (full run)       │
│  5. Deep 5-question analysis             │
│  6. Acceptance gate (accept/reject/explore) │
│  7. Append ledger, commit, update status │
│  8. Plateau? → SOTA scan                 │
│  9. Target reached? → Stop               │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Reporting   │  CURRENT_STATUS.md, round logs, notifications
└─────────────┘
```

## Quick Start

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Initialize a research project (discovery + baseline, 0 experiment rounds)
python -m engine.loop \
  --project /tmp/my-research \
  --target https://github.com/org/repo.git \
  --goal "Improve benchmark to 90%" \
  --rounds 0

# Run experiment rounds
python -m engine.loop \
  --project /tmp/my-research \
  --goal "Improve benchmark to 90%" \
  --rounds 5

# Check status
cat /tmp/my-research/CURRENT_STATUS.md

# Or use the CLI wrapper
bash cli/autoresearch.sh init /tmp/my-research https://github.com/org/repo.git "Improve benchmark to 90%"
bash cli/autoresearch.sh run /tmp/my-research "Improve benchmark to 90%" 5
bash cli/autoresearch.sh status /tmp/my-research
bash cli/autoresearch.sh analyze /tmp/my-research
bash cli/autoresearch.sh scan /tmp/my-research "retrieval optimization techniques"
```

## OpenClaw Integration

Install as an OpenClaw skill:

```bash
ln -s /path/to/autoresearch ~/.openclaw/workspace/.agents/skills/autoresearch
```

Then just tell your agent: "research this repo and improve the benchmark to 90%"

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTORESEARCH_MODEL` | `gpt-4o-mini` | LLM model for experiment design and analysis |
| `AUTORESEARCH_PROVIDER` | `litellm` | LLM provider (`litellm` or set `AUTORESEARCH_LLM_CLI`) |
| `AUTORESEARCH_LLM_CLI` | _(none)_ | Custom CLI command for LLM calls |

### Project Config File

Create `config.json` in your project root:

```json
{
  "model": "claude-sonnet-4-20250514",
  "provider": "litellm",
  "baseline_runs": 3,
  "fast_items": 25,
  "scale_items": 0,
  "thresholds": {
    "local_improvement_pp": 1.0,
    "strong_improvement_pp": 1.0,
    "critical_slice_regression_pp": -1.0,
    "max_variance_pp": 2.0,
    "plateau_consecutive_rejects": 2,
    "mandatory_scan_interval": 3
  },
  "budget": {
    "max_rounds": 12,
    "max_runtime_minutes": 240,
    "max_cost_usd": 50.0
  }
}
```

### Evaluator Contract

Your eval harness must output JSON to stdout:

```json
{
  "primary_metric": 0.742,
  "slices": {
    "category_a": 0.81,
    "category_b": 0.69
  },
  "secondary_metrics": {
    "latency_ms": 420,
    "cost_usd": 0.11
  }
}
```

The engine passes `AUTORESEARCH_MAX_ITEMS` as an environment variable for fast-subset validation.

## Project Worktree

Each research project maintains durable state:

```
project/
├── program.md              # Goals, constraints, hypotheses, queue
├── ledger.jsonl            # Append-only experiment history (file-locked)
├── CURRENT_STATUS.md       # Resumable snapshot
├── experiments/
│   └── NNN/
│       ├── round-log.md
│       ├── post-run-analysis.md
│       └── diff.patch
├── eval/                   # Evaluation harness
├── scanner/                # SOTA scan results
├── logs/                   # Runtime logs
└── src/                    # Working copy of target code
```

## Key Design Principles

From [practical-autoresearch](https://github.com/dddabtc/practical-autoresearch):

1. **Baseline first** — if the baseline is unreliable, all conclusions are suspect
2. **Telescope method** — coarse sweep → fine-tune → scale (never skip steps)
3. **One hypothesis per round** — keep changes attributable
4. **Deep analysis required** — 5-question post-run analysis, not just headline metrics
5. **Acceptance gates** — fast validation + strong confirmation before accepting
6. **Durable state** — files beat session memory; survives restarts and handoffs
7. **LLM-first** — use LLM for experiment design, not just parameter sweeps
8. **Single ledger principle** — one append-only ledger, file-locked for multi-agent safety

## License

MIT
