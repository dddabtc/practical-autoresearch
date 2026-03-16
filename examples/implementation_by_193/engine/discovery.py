from __future__ import annotations
import json, logging, re, shutil, subprocess
from pathlib import Path
from typing import Any
from .config import ResearchConfig
LOGGER = logging.getLogger(__name__)
BENCHMARK_HINTS = ('benchmark','eval','evaluate','pytest','score','accuracy','f1')
def _copy_or_clone(target: str, destination: Path) -> dict[str, Any]:
    if re.match(r'^(https?|git@)', target):
        if destination.exists() and any(destination.iterdir()): return {'mode':'reuse','source':target,'destination':str(destination)}
        subprocess.run(['git','clone',target,str(destination)], check=True); return {'mode':'clone','source':target,'destination':str(destination)}
    source = Path(target).expanduser().resolve()
    if not source.exists(): raise FileNotFoundError(f'Target path does not exist: {source}')
    if source == destination: return {'mode':'in_place','source':str(source),'destination':str(destination)}
    if destination.exists() and any(destination.iterdir()): shutil.rmtree(destination)
    shutil.copytree(source, destination, dirs_exist_ok=True); return {'mode':'copy','source':str(source),'destination':str(destination)}
def infer_eval_commands(root: Path) -> list[str]:
    c: list[str] = []
    # Direct eval/benchmark scripts
    for name in ('eval.py', 'evaluate.py', 'benchmark.py', 'run_eval.py', 'eval_harness.py'):
        if (root / name).exists():
            c.append(f'python3 {name}')
    # eval/ directory with main scripts
    if (root / 'eval').is_dir():
        for name in ('eval.py', 'run.py', 'main.py', 'evaluate.py'):
            if (root / 'eval' / name).exists():
                c.append(f'python3 eval/{name}')
    # pytest
    if (root / 'pytest.ini').exists() or (root / 'pyproject.toml').exists() or any(root.glob('tests/test*.py')):
        c.append('pytest -q')
    # npm scripts
    if (root / 'package.json').exists():
        try:
            scripts = json.loads((root / 'package.json').read_text()).get('scripts', {})
            for key in ('eval', 'benchmark', 'test'):
                if key in scripts:
                    c.append(f'npm run {key}')
        except json.JSONDecodeError:
            LOGGER.warning('Could not parse package.json')
    # Makefile targets
    if (root / 'Makefile').exists():
        text = (root / 'Makefile').read_text(errors='ignore')
        for target in ('eval', 'benchmark', 'test'):
            if re.search(rf'^{target}:', text, re.M):
                c.append(f'make {target}')
    return list(dict.fromkeys(c or ['python3 -m pytest -q']))
def run_discovery(config: ResearchConfig, target: str, goal: str) -> dict[str, Any]:
    copy = _copy_or_clone(target, config.project.source)
    files = [p for p in config.project.source.rglob('*') if p.is_file() and '.git' not in p.parts]
    hints = [str(p.relative_to(config.project.source)) for p in files if any(t in p.name.lower() for t in BENCHMARK_HINTS)][:25]
    evals = infer_eval_commands(config.project.source)
    config.project.program.write_text(f"# Research Program\n\n## Goal\n{goal}\n\n## Target\n{target}\n\n## Success metric\n- Primary metric: primary_metric from discovered evaluator\n- Acceptance threshold: baseline + {config.thresholds.strong_improvement_pp:.1f}pp on strong confirmation path\n\n## Current phase\ndiscovery\n\n## Experiment queue\n1. Run baseline repeatedly and measure variance\n2. Coarse sweep on a fast subset across major categories\n3. Fine-tune weak slices before full-scale confirmation\n\n## Acceptance gate\n- Local validation rule: +{config.thresholds.local_improvement_pp:.1f}pp on fast subset\n- Strong confirmation rule: +{config.thresholds.strong_improvement_pp:.1f}pp on strong path\n\n## Plateau rule\n- Stop or re-evaluate after {config.thresholds.plateau_consecutive_rejects} consecutive rejects\n\n## Discovery notes\n- File count: {len(files)}\n- Benchmark-like files: {', '.join(hints) or 'none found'}\n- Eval candidates: {', '.join(evals)}\n")
    return {'copy':copy,'inventory':{'file_count':len(files),'benchmark_like_files':hints,'eval_candidates':evals},'program':str(config.project.program)}
