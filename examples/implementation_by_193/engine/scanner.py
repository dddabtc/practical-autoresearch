from __future__ import annotations
import json, logging, subprocess
from typing import Any
from .config import ResearchConfig
from .llm import LLMClient

LOGGER = logging.getLogger(__name__)


def _web_search(query: str, count: int = 5) -> list[dict[str, str]]:
    """Try multiple search backends: brave-search CLI, ddgr, or fallback to LLM."""
    # Try brave-search via openclaw's web_search pattern (subprocess)
    for cmd in ['brave-search', 'ddgr']:
        try:
            if cmd == 'ddgr':
                result = subprocess.run(
                    ['ddgr', '--json', '-n', str(count), query],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    items = json.loads(result.stdout)
                    return [{'title': i.get('title', ''), 'url': i.get('url', ''), 'snippet': i.get('abstract', '')} for i in items[:count]]
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            continue
    LOGGER.info('No web search CLI available; SOTA scan will rely on LLM knowledge only')
    return []


def run_scan(config: ResearchConfig, llm: LLMClient, topic: str) -> dict[str, Any]:
    """Scan for SOTA techniques relevant to the current research plateau."""
    findings = _web_search(f'{topic} state of the art techniques 2025 2026')

    prompt = f"""You are a research scout. The autoresearch loop has hit a plateau.

Topic: {topic}

Web search findings:
{json.dumps(findings, indent=2) if findings else '(no web results available — use your training knowledge)'}

Provide:
1. 3-5 promising techniques or papers that could help
2. For each: title, key idea, expected impact, implementation difficulty
3. A ranked recommendation of which to try first

Format as markdown."""

    try:
        summary = llm.generate(prompt, system='You are a research scout specializing in finding relevant SOTA techniques.').text
    except Exception as exc:
        summary = f'# Scan summary\n\nLLM analysis unavailable: {exc}\n\nRaw findings:\n{json.dumps(findings, indent=2)}'

    scan_path = config.project.scanner / 'latest-scan.md'
    scan_path.write_text(summary)
    LOGGER.info('SOTA scan written to %s', scan_path)
    return {'topic': topic, 'findings': findings, 'summary': summary}
