from __future__ import annotations
import argparse, json, logging
from .baseline import verify_baseline
from .config import ResearchConfig, setup_logging
from .discovery import run_discovery
from .experiment import run_experiment
from .ledger import Ledger
from .llm import LLMClient
from .reporter import update_status
from .scanner import run_scan
LOGGER = logging.getLogger(__name__)
def detect_evaluator(config: ResearchConfig) -> str:
    text = config.project.program.read_text() if config.project.program.exists() else ''
    for line in text.splitlines():
        if line.strip().startswith('- Eval candidates:'): return line.split(':',1)[1].strip().split(',')[0].strip()
    return 'pytest -q'
def should_scan(ledger: Ledger, config: ResearchConfig) -> bool:
    if len(ledger.recent_decisions(config.thresholds.mandatory_scan_interval)) >= config.thresholds.mandatory_scan_interval: return True
    rejects = 0
    for d in reversed(ledger.recent_decisions(10)):
        if d == 'reject': rejects += 1
        else: break
    return rejects >= config.thresholds.plateau_consecutive_rejects
def _target_reached(result: dict, goal: str) -> bool:
    """Check if the experiment result meets the goal target (e.g. '90%' → 0.90)."""
    import re
    m = re.search(r'(\d+(?:\.\d+)?)\s*%', goal)
    if not m:
        return False
    target = float(m.group(1)) / 100.0
    best = result.get('entry', {}).get('result', {})
    strong = best.get('strong') or best.get('fast') or {}
    return float(strong.get('primary_metric', 0.0)) >= target


def run_loop(config: ResearchConfig, target: str | None, goal: str, rounds: int) -> dict:
    llm = LLMClient(config.model, config.provider)
    ledger = Ledger(config.project.ledger)

    if target:
        run_discovery(config, target, goal)

    evaluator = detect_evaluator(config)
    baseline = verify_baseline(config, evaluator)
    outcome: dict = {'baseline': baseline, 'rounds_completed': 0, 'target_reached': False}

    if not baseline.get('stable', False):
        LOGGER.warning('Baseline unstable — aborting loop until evaluator is fixed')
        outcome['aborted'] = 'unstable_baseline'
        return outcome

    for i in range(rounds):
        LOGGER.info('=== Round %d/%d ===', i + 1, rounds)
        result = run_experiment(config, llm, goal, baseline, evaluator)
        outcome['last_round'] = result
        outcome['rounds_completed'] = i + 1

        if result['entry']['decision'] == 'accept':
            # Update baseline to the new accepted result for subsequent rounds
            best = result['entry'].get('result', {})
            accepted_metrics = best.get('strong') or best.get('fast') or {}
            if accepted_metrics.get('primary_metric'):
                baseline = {**baseline, 'primary_metric': float(accepted_metrics['primary_metric'])}

            if _target_reached(result, goal):
                outcome['target_reached'] = True
                update_status(config, {
                    'state': 'target-reached', 'goal': goal, 'phase': 'complete',
                    'last_experiment': result['entry']['id'],
                    'last_decision': 'accept',
                    'baseline': baseline, 'best_result': accepted_metrics,
                    'plateau': 'clear', 'next_step': 'Target reached. Review and ship.'
                })
                LOGGER.info('Target reached!')
                break
            else:
                update_status(config, {
                    'state': 'target-progress', 'goal': goal, 'phase': 'experiment',
                    'last_experiment': result['entry']['id'],
                    'last_decision': 'accept',
                    'baseline': baseline, 'best_result': accepted_metrics,
                    'plateau': 'clear', 'next_step': 'Continue improving toward target'
                })

        if should_scan(ledger, config):
            LOGGER.info('Plateau detected — running SOTA scan')
            outcome['scan'] = run_scan(config, llm, f'{goal} benchmark optimization techniques')

    return outcome
def main() -> None:
    p = argparse.ArgumentParser(description='Run AutoResearch loop'); p.add_argument('--project', required=True); p.add_argument('--target'); p.add_argument('--goal', required=True); p.add_argument('--rounds', type=int, default=1); p.add_argument('--config'); p.add_argument('--verbose', action='store_true'); a = p.parse_args()
    setup_logging(a.verbose); cfg = ResearchConfig.load(a.project, a.config, verbose=a.verbose); print(json.dumps(run_loop(cfg, a.target, a.goal, a.rounds), indent=2, default=str))
if __name__ == '__main__': main()
