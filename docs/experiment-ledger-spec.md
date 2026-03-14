# Experiment Ledger Specification

The ledger is the durable memory of an autoresearch loop.

Use an append-only format such as `ledger.jsonl` so every experiment round leaves behind a compact, machine-readable record.

---

## 1) Why keep a ledger

A good ledger makes it possible to:

- resume after interruption,
- audit decisions,
- inspect historical gradients,
- compare branches of exploration,
- detect plateaus,
- and explain why the next experiment was chosen.

---

## 2) Minimal fields

Each entry should include at least:

- experiment ID
- timestamp
- hypothesis
- change summary
- metrics
- decision
- reason
- runtime / cost

---

## 3) Recommended JSONL schema

```jsonc
{
  "id": "exp-001",
  "timestamp": "2026-03-14T04:00:00Z",
  "phase": "retrieval",
  "hypothesis": "Adding shortlist pre-filtering reduces candidate noise",
  "change_summary": "Pre-filtered candidate set before final ranking",
  "diff_file": "experiments/001/diff.patch",
  "baseline": {
    "primary_metric": 0.742,
    "slices": {
      "slice_a": 0.81,
      "slice_b": 0.69
    }
  },
  "result": {
    "primary_metric": 0.758,
    "slices": {
      "slice_a": 0.83,
      "slice_b": 0.71
    },
    "secondary_metrics": {
      "latency_ms": 420,
      "cost_usd": 0.11
    }
  },
  "delta": {
    "primary_metric_pp": 1.6
  },
  "decision": "accept",
  "reason": "Primary metric improved, critical slices held, confirmation path agreed",
  "runtime_sec": 210,
  "cost_usd": 0.11
}
```

---

## 4) Decision vocabulary

Recommended values:

- `accept`
- `reject`
- `explore`
- `blocked`
- `pending_confirmation`

Keep the vocabulary small and stable.

---

## 5) Optional but useful fields

You may also include:

- experiment axis coordinates
- seed / config hash
- dataset version
- evaluator version
- code version / commit hash
- confidence level
- failure taxonomy summary
- next recommended experiment

---

## 6) Ledger writing rules

1. Append only — do not silently rewrite history.
2. Use one entry per completed round.
3. If a round is interrupted, either:
   - write a `blocked` / `interrupted` style entry, or
   - rerun from scratch and only record the completed run.
4. Keep reasons concise but interpretable.
5. Prefer stable field names over cleverness.

---

## 7) Relationship to other files

- `ledger.jsonl` → structured history
- `CURRENT_STATUS.md` → latest human-readable snapshot
- `program.md` → goals and future queue
- `experiments/NNN/round-log.md` → full per-round narrative detail

The ledger should be enough for quick resumption and quantitative review.
