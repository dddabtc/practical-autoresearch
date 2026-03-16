from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .config import ResearchConfig

def write_round_log(config: ResearchConfig, experiment_id: str, content: dict[str, Any]) -> Path:
    d = config.project.experiments / experiment_id.replace('exp-', ''); d.mkdir(parents=True, exist_ok=True); p = d/'round-log.md'
    p.write_text(f"# Round {experiment_id}\n\n## Hypothesis\n{content.get('hypothesis','-')}\n\n## Change introduced\n{content.get('change_summary','-')}\n\n## Setup\n- Telescope stage: {content.get('stage','coarse')}\n\n## Results\n- Baseline: {content.get('baseline')}\n- Fast validation: {content.get('fast_result')}\n- Strong confirmation: {content.get('strong_result')}\n\n## Deep analysis\n{content.get('analysis_summary','-')}\n\n## Decision\n- Verdict: {content.get('decision','pending')}\n- Reason: {content.get('reason','-')}\n- Next: {content.get('next_step','-')}\n")
    return p

def write_post_run_analysis(config: ResearchConfig, experiment_id: str, analysis_text: str) -> Path:
    d = config.project.experiments / experiment_id.replace('exp-', ''); d.mkdir(parents=True, exist_ok=True); p = d/'post-run-analysis.md'; p.write_text(analysis_text); return p

def update_status(config: ResearchConfig, snapshot: dict[str, Any]) -> Path:
    config.project.status.write_text(f"# Current Status\n\n- Updated: {datetime.now(timezone.utc).isoformat()}\n- State: {snapshot.get('state','running')}\n- Goal: {snapshot.get('goal','-')}\n- Current phase: {snapshot.get('phase','-')}\n- Last experiment: {snapshot.get('last_experiment','-')}\n- Last decision: {snapshot.get('last_decision','-')}\n- Baseline: {snapshot.get('baseline','-')}\n- Best result: {snapshot.get('best_result','-')}\n- Plateau status: {snapshot.get('plateau','-')}\n- Next step: {snapshot.get('next_step','-')}\n")
    return config.project.status
