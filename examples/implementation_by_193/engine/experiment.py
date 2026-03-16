from __future__ import annotations
import subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from .analysis import analyze_round
from .baseline import run_evaluator
from .config import ResearchConfig
from .gate import evaluate_gate
from .ledger import Ledger, LedgerEntry
from .llm import LLMClient
from .reporter import update_status, write_post_run_analysis, write_round_log
SYSTEM = 'You are a research engineer. Propose small, attributable changes that improve benchmark results without breaking the evaluator.'
def _git(command: list[str], cwd: Path) -> str:
    done = subprocess.run(['git', *command], cwd=str(cwd), capture_output=True, text=True)
    if done.returncode != 0: raise RuntimeError(done.stderr.strip() or done.stdout.strip())
    return done.stdout.strip()
def _current_stage(ledger: Ledger) -> str:
    completed = [e for e in ledger.read_all() if e.get('phase') == 'experiment' and e.get('status') == 'completed']
    return 'coarse' if len(completed) < 1 else 'fine-tune' if len(completed) < 3 else 'scale'
def _design_experiment(llm: LLMClient, goal: str, program_text: str, ledger_entries: list[dict], stage: str) -> dict:
    prompt = dedent(f'''Design the next autoresearch experiment.
Goal: {goal}
Stage: {stage}
Program:\n{program_text}
Recent ledger entries:\n{ledger_entries[-5:]}
Return JSON with keys hypothesis, change_summary, patch, next_step_if_reject.
The patch must be a unified diff that can be applied with git apply.
''')
    return llm.generate_json(prompt, system=SYSTEM)
def run_experiment(config: ResearchConfig, llm: LLMClient, goal: str, baseline: dict, evaluator_command: str) -> dict:
    ledger = Ledger(config.project.ledger); stage = _current_stage(ledger); program_text = config.project.program.read_text() if config.project.program.exists() else ''
    plan = _design_experiment(llm, goal, program_text, ledger.read_all(), stage); reservation = ledger.reserve('experiment', plan['hypothesis'], metadata={'stage':stage})
    d = config.project.experiments / reservation.id.replace('exp-',''); d.mkdir(parents=True, exist_ok=True); diff_path = d/'diff.patch'; diff_path.write_text(plan['patch'])
    start = time.time()
    try:
        subprocess.run(['git','apply','--whitespace=fix',str(diff_path)], cwd=str(config.project.source), check=True)
        fast = run_evaluator(evaluator_command, config.project.source, config.fast_items); strong = None
        if stage == 'scale' or float(fast.get('primary_metric',0.0)) >= float(baseline.get('primary_metric',0.0)): strong = run_evaluator(evaluator_command, config.project.source, None if config.scale_items <= 0 else config.scale_items)
        gate = evaluate_gate(baseline, fast, strong, config.thresholds)
        analysis = analyze_round(config, llm, {'baseline':baseline,'fast_result':fast,'strong_result':strong,'hypothesis':plan['hypothesis'],'decision':gate.decision,'failure_summary':'populate with evaluator-specific failures when available'})
        write_post_run_analysis(config, reservation.id, analysis); write_round_log(config, reservation.id, {'hypothesis':plan['hypothesis'],'change_summary':plan['change_summary'],'baseline':baseline,'fast_result':fast,'strong_result':strong,'analysis_summary':analysis,'decision':gate.decision,'reason':gate.reason,'next_step':plan.get('next_step_if_reject','Continue telescope progression'),'stage':stage})
        runtime = time.time() - start; commit_hash = None
        if (config.project.source/'.git').exists():
            _git(['add','-A'], config.project.source)
            if _git(['status','--short'], config.project.source): _git(['commit','-m',f"{reservation.id}: {plan['change_summary'][:60]}"], config.project.source)
            commit_hash = _git(['rev-parse','--short','HEAD'], config.project.source)
        entry = LedgerEntry(id=reservation.id, timestamp=datetime.now(timezone.utc).isoformat(), phase='experiment', hypothesis=plan['hypothesis'], change_summary=plan['change_summary'], diff_file=str(diff_path.relative_to(config.project.root)), baseline=baseline, result={'fast':fast,'strong':strong}, delta={'primary_metric_pp': (float((strong or fast).get('primary_metric',0.0)) - float(baseline.get('primary_metric',0.0))) * 100.0}, decision=gate.decision, reason=gate.reason, runtime_sec=runtime, code_version=commit_hash, next_recommended_experiment=plan.get('next_step_if_reject'), metadata={'stage':stage})
        ledger.append(entry); update_status(config, {'state':'running','goal':goal,'phase':'experiment','last_experiment':reservation.id,'last_decision':gate.decision,'baseline':baseline,'best_result':strong or fast,'plateau':'watch' if gate.decision == 'reject' else 'clear','next_step':plan.get('next_step_if_reject','Continue to next telescope stage')})
        return {'entry': entry.to_dict(), 'analysis': analysis}
    except Exception as exc:
        ledger.append(LedgerEntry(id=reservation.id, timestamp=datetime.now(timezone.utc).isoformat(), phase='experiment', hypothesis=plan.get('hypothesis','unknown'), change_summary=plan.get('change_summary','failed before completion'), diff_file=str(diff_path.relative_to(config.project.root)) if diff_path.exists() else None, baseline=baseline, decision='blocked', reason=str(exc), runtime_sec=time.time()-start, metadata={'stage':stage}))
        raise
