# Smoke Test Record

Tested on: 2026-03-16, macOS (arm64), Python 3.9, op193 (192.168.1.193)

## 1. Compile Check
```
$ python3 -m compileall engine/
Listing 'engine/'...
Compiling 'engine/loop.py'...
Compiling 'engine/scanner.py'...
✅ All modules compiled successfully
```

## 2. CLI Help
```
$ python3 -m engine.loop --help
usage: loop.py [-h] --project PROJECT [--target TARGET] --goal GOAL
               [--rounds ROUNDS] [--config CONFIG] [--verbose]
✅ CLI argument parsing works
```

## 3. Discovery (mock project with eval.py)
```
$ python3 -c "from engine.discovery import ..."
{
  "copy": {"mode": "in_place", ...},
  "inventory": {
    "file_count": 1,
    "benchmark_like_files": ["eval.py"],
    "eval_candidates": ["python3 eval.py"]
  }
}
✅ Discovery correctly detected eval.py and recommended "python3 eval.py"
```

## 4. Baseline Verification (3 runs)
```
$ python3 -m engine.loop --project /tmp/autoresearch-poc --target /tmp/autoresearch-poc/src --goal "Improve benchmark to 90%" --rounds 0 --verbose
{
  "baseline": {
    "primary_metric": 0.7434,
    "variance_pp": 0.0,
    "stable": true,
    "slices": {"category_a": 0.8134, "category_b": 0.6934}
  },
  "rounds_completed": 0,
  "target_reached": false
}
✅ Baseline stable (3 runs, 0.0pp variance), correctly written to ledger.jsonl
```

## 5. State Files Verification
- program.md ✅ — goals, eval candidates, acceptance gates populated
- CURRENT_STATUS.md ✅ — state=baseline-complete, next_step="Design first coarse experiment"
- ledger.jsonl ✅ — exp-001 baseline entry with full metrics, decision=accept

## Mock Evaluator Used
```python
#!/usr/bin/env python3
import json, os, random
random.seed(42)
max_items = int(os.environ.get('AUTORESEARCH_MAX_ITEMS', '100'))
score = 0.742 + random.uniform(-0.005, 0.005)
print(json.dumps({
    "primary_metric": round(score, 4),
    "slices": {"category_a": round(score + 0.07, 4), "category_b": round(score - 0.05, 4)},
    "secondary_metrics": {"latency_ms": 420, "items_evaluated": max_items}
}))
```

## Issues Found & Fixed During Testing
1. `python` not found on macOS — fixed discovery to use `python3`
2. Discovery didn't detect `eval.py` — added direct eval script detection
3. Loop didn't check target achievement — added `_target_reached()` with goal parsing
4. Loop didn't update baseline after accept — added baseline progression
5. Loop didn't abort on unstable baseline — added early return
