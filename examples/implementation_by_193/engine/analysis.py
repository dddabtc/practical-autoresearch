from __future__ import annotations
from textwrap import dedent
from typing import Any
from .config import ResearchConfig
from .llm import LLMClient
SYSTEM = 'You are a rigorous research analyst. Be evidence-driven and explicit about uncertainty.'
def analyze_round(config: ResearchConfig, llm: LLMClient, context: dict[str, Any]) -> str:
    prompt = dedent(f'''Perform a deep five-question post-run analysis.
Baseline: {context.get('baseline')}
Fast result: {context.get('fast_result')}
Strong result: {context.get('strong_result')}
Hypothesis: {context.get('hypothesis')}
Decision: {context.get('decision')}
Failure summary: {context.get('failure_summary','Unknown')}

Answer:
1. Did the primary metric improve?
2. Which slices improved or regressed?
3. What changed in the failure distribution?
4. How strong is the signal?
5. What is the best next move?
''')
    try: return llm.generate(prompt, system=SYSTEM).text
    except Exception as exc: return f'# Post-Run Analysis\n\nLLM analysis unavailable: {exc}\n'
