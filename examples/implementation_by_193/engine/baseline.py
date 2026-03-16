from __future__ import annotations
import json, statistics, subprocess, time, os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .config import ResearchConfig
from .ledger import Ledger, LedgerEntry
from .reporter import update_status
def _parse_metrics(stdout: str) -> dict[str, Any]:
    s = stdout.strip()
    try:
        data = json.loads(s)
        if isinstance(data, dict): return data
    except json.JSONDecodeError:
        pass
    for line in s.splitlines()[::-1]:
        if 'primary_metric' in line: return {'primary_metric': float(line.split(':',1)[1].strip()), 'slices': {}, 'secondary_metrics': {}}
    raise ValueError('Evaluator output did not contain JSON or primary_metric')
def run_evaluator(command: str, cwd: Path, max_items: int | None = None) -> dict[str, Any]:
    env = dict(os.environ)
    if max_items is not None: env['AUTORESEARCH_MAX_ITEMS'] = str(max_items)
    start = time.time(); done = subprocess.run(command, shell=True, cwd=str(cwd), capture_output=True, text=True, env=env); runtime = time.time() - start
    if done.returncode != 0: raise RuntimeError(f'Evaluator failed ({done.returncode}): {done.stderr.strip() or done.stdout.strip()}')
    metrics = _parse_metrics(done.stdout); metrics['runtime_sec'] = runtime; return metrics
def verify_baseline(config: ResearchConfig, command: str) -> dict[str, Any]:
    results = [run_evaluator(command, config.project.source, None if config.scale_items <= 0 else config.scale_items) for _ in range(config.baseline_runs)]
    primary = [float(x['primary_metric']) for x in results]; mean = statistics.fmean(primary); variance_pp = (max(primary)-min(primary))*100.0 if len(primary)>1 else 0.0; stable = variance_pp <= config.thresholds.max_variance_pp
    summary = {'primary_metric': mean, 'runs': results, 'variance_pp': variance_pp, 'stable': stable, 'slices': results[-1].get('slices', {}), 'secondary_metrics': results[-1].get('secondary_metrics', {})}
    ledger = Ledger(config.project.ledger); ledger.append(LedgerEntry(id=ledger.next_id(), timestamp=datetime.now(timezone.utc).isoformat(), phase='baseline', hypothesis='Establish trustworthy baseline', change_summary=f'Ran baseline {config.baseline_runs} times with {command}', result=summary, delta={'primary_metric_pp':0.0}, decision='accept' if stable else 'blocked', reason='Baseline stable' if stable else 'Baseline unstable; fix evaluation first', runtime_sec=sum(x['runtime_sec'] for x in results)))
    update_status(config, {'state':'baseline-complete' if stable else 'baseline-unstable','goal':'Establish stable baseline','phase':'baseline','last_experiment':'baseline','last_decision':'accept' if stable else 'blocked','baseline':summary,'best_result':summary,'plateau':'none','next_step':'Design first coarse experiment' if stable else 'Fix evaluator instability'})
    return summary
