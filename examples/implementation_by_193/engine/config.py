from __future__ import annotations
import json, logging, os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
LOGGER = logging.getLogger(__name__)
@dataclass
class ProjectPaths:
    root: Path
    source: Path
    experiments: Path
    eval_dir: Path
    program: Path
    status: Path
    ledger: Path
    logs: Path
    scanner: Path
    @classmethod
    def from_root(cls, root: str | Path) -> 'ProjectPaths':
        p = Path(root).expanduser().resolve()
        return cls(p, p/'src', p/'experiments', p/'eval', p/'program.md', p/'CURRENT_STATUS.md', p/'ledger.jsonl', p/'logs', p/'scanner')
    def ensure(self) -> None:
        for d in (self.root, self.source, self.experiments, self.eval_dir, self.logs, self.scanner): d.mkdir(parents=True, exist_ok=True)
        self.status.touch(exist_ok=True)
        self.ledger.touch(exist_ok=True)
@dataclass
class Thresholds:
    local_improvement_pp: float = 1.0
    strong_improvement_pp: float = 1.0
    critical_slice_regression_pp: float = -1.0
    max_variance_pp: float = 2.0
    plateau_consecutive_rejects: int = 2
    mandatory_scan_interval: int = 3
@dataclass
class Budget:
    max_rounds: int = 12
    max_runtime_minutes: int = 240
    max_cost_usd: float = 50.0
@dataclass
class ResearchConfig:
    project: ProjectPaths
    model: str = field(default_factory=lambda: os.getenv('AUTORESEARCH_MODEL', 'gpt-4o-mini'))
    provider: str = field(default_factory=lambda: os.getenv('AUTORESEARCH_PROVIDER', 'litellm'))
    thresholds: Thresholds = field(default_factory=Thresholds)
    budget: Budget = field(default_factory=Budget)
    baseline_runs: int = 3
    fast_items: int = 25
    scale_items: int = 0
    verbose: bool = False
    @classmethod
    def load(cls, project_root: str | Path, config_file: str | Path | None = None, verbose: bool = False) -> 'ResearchConfig':
        project = ProjectPaths.from_root(project_root); project.ensure(); payload: dict[str, Any] = {}
        if config_file and Path(config_file).exists(): payload = json.loads(Path(config_file).read_text())
        return cls(project=project, model=payload.get('model', os.getenv('AUTORESEARCH_MODEL', 'gpt-4o-mini')), provider=payload.get('provider', os.getenv('AUTORESEARCH_PROVIDER', 'litellm')), thresholds=Thresholds(**payload.get('thresholds', {})), budget=Budget(**payload.get('budget', {})), baseline_runs=int(payload.get('baseline_runs', 3)), fast_items=int(payload.get('fast_items', 25)), scale_items=int(payload.get('scale_items', 0)), verbose=verbose)
def setup_logging(verbose: bool = False) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
