from __future__ import annotations
import json, os, re, subprocess
from dataclasses import dataclass
from typing import Any
try:
    from litellm import completion
except Exception:
    completion = None
@dataclass
class LLMResponse:
    text: str
    raw: dict[str, Any] | None = None
class LLMClient:
    def __init__(self, model: str, provider: str = 'litellm') -> None: self.model = model; self.provider = provider
    def generate(self, prompt: str, system: str | None = None, temperature: float = 0.2) -> LLMResponse:
        if self.provider == 'litellm' and completion is not None:
            msgs = ([{'role':'system','content':system}] if system else []) + [{'role':'user','content':prompt}]
            result = completion(model=self.model, messages=msgs, temperature=temperature)
            return LLMResponse(text=result.choices[0].message.content or '', raw=result.model_dump() if hasattr(result,'model_dump') else None)
        cli = os.getenv('AUTORESEARCH_LLM_CLI')
        if cli:
            out = subprocess.run([cli, prompt], check=True, capture_output=True, text=True)
            return LLMResponse(out.stdout.strip(), {'stderr': out.stderr})
        raise RuntimeError('No LLM backend available. Install litellm or set AUTORESEARCH_LLM_CLI.')
    def generate_json(self, prompt: str, system: str | None = None, temperature: float = 0.2) -> dict[str, Any]:
        text = self.generate(prompt, system, temperature).text.strip(); m = re.search(r'```(?:json)?\s*(\{.*\}|\[.*\])\s*```', text, re.S)
        return json.loads(m.group(1) if m else text)
