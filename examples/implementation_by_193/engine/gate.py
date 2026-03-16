from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .config import Thresholds
@dataclass
class GateDecision:
    decision: str; reason: str; needs_confirmation: bool

def evaluate_gate(baseline: dict[str, Any], fast_result: dict[str, Any], strong_result: dict[str, Any] | None, thresholds: Thresholds) -> GateDecision:
    b = float(baseline.get('primary_metric', 0.0)); f = float(fast_result.get('primary_metric', 0.0)); local_pp = (f - b) * 100.0
    if local_pp < thresholds.local_improvement_pp: return GateDecision('reject', f'Fast validation delta {local_pp:.2f}pp below threshold', False)
    for name, value in fast_result.get('slices', {}).items():
        if name in baseline.get('slices', {}):
            delta_pp = (float(value) - float(baseline['slices'][name])) * 100.0
            if delta_pp < thresholds.critical_slice_regression_pp: return GateDecision('reject', f'Critical slice {name} regressed by {delta_pp:.2f}pp', False)
    if strong_result is None: return GateDecision('explore', 'Fast path passed but strong confirmation missing', True)
    strong_pp = (float(strong_result.get('primary_metric', 0.0)) - b) * 100.0
    if strong_pp >= thresholds.strong_improvement_pp: return GateDecision('accept', f'Strong confirmation delta {strong_pp:.2f}pp passed', False)
    if strong_pp > 0: return GateDecision('explore', f'Strong confirmation positive but weak at {strong_pp:.2f}pp', False)
    return GateDecision('reject', f'Strong confirmation failed with {strong_pp:.2f}pp', False)
