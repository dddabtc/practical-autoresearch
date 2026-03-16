from __future__ import annotations
import contextlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
try:
    import fcntl
except ImportError:
    fcntl = None
@dataclass
class LedgerEntry:
    id: str; timestamp: str; phase: str; hypothesis: str; change_summary: str
    diff_file: str | None = None; baseline: dict[str, Any] = field(default_factory=dict); result: dict[str, Any] = field(default_factory=dict)
    delta: dict[str, Any] = field(default_factory=dict); decision: str = 'pending_confirmation'; reason: str = ''
    runtime_sec: float | None = None; cost_usd: float | None = None; lane: str = 'manual'; status: str = 'completed'
    code_version: str | None = None; next_recommended_experiment: str | None = None; metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]: return asdict(self)
class Ledger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True); self.path.touch(exist_ok=True); self.lock_path = self.path.with_suffix(self.path.suffix + '.lock'); self.lock_path.touch(exist_ok=True)
    @contextlib.contextmanager
    def _lock(self) -> Iterator[None]:
        with self.lock_path.open('r+') as h:
            if fcntl is not None: fcntl.flock(h.fileno(), fcntl.LOCK_EX)
            try: yield
            finally:
                if fcntl is not None: fcntl.flock(h.fileno(), fcntl.LOCK_UN)
    def read_all(self) -> list[dict[str, Any]]:
        with self._lock(): return [json.loads(line) for line in self.path.read_text().splitlines() if line.strip()]
    def append(self, entry: LedgerEntry) -> None:
        with self._lock(), self.path.open('a') as h: h.write(json.dumps(entry.to_dict(), sort_keys=True) + '\n')
    def next_id(self) -> str:
        with self._lock(): return f"exp-{len([l for l in self.path.read_text().splitlines() if l.strip()]) + 1:03d}"
    def reserve(self, phase: str, hypothesis: str, lane: str = 'manual', metadata: dict[str, Any] | None = None) -> LedgerEntry:
        e = LedgerEntry(id=self.next_id(), timestamp=datetime.now(timezone.utc).isoformat(), phase=phase, hypothesis=hypothesis, change_summary='Reserved experiment slot', decision='pending_confirmation', reason='Reserved before execution per single-ledger principle', lane=lane, status='reserved', metadata=metadata or {})
        self.append(e); return e
    def recent_decisions(self, limit: int = 5) -> list[str]: return [e.get('decision', '') for e in [x for x in self.read_all() if x.get('status') == 'completed'][-limit:]]
