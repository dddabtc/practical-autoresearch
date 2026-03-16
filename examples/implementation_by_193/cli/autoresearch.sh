#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat >&2 <<EOF
Usage: autoresearch.sh <command> [args...]

Commands:
  init    <project> <target> <goal>           Initialize a research project
  run     <project> <goal> [rounds] [--config path] [--verbose]
  status  <project>                           Show current status
  analyze <project>                           Show latest post-run analysis
  scan    <project> <topic>                   Run SOTA scan
EOF
  exit 1
}

[[ $# -ge 1 ]] || usage

case "$1" in
  init)
    [[ $# -ge 4 ]] || { echo "Usage: autoresearch.sh init <project> <target> <goal>" >&2; exit 1; }
    exec "$PYTHON_BIN" -m engine.loop --project "$2" --target "$3" --goal "$4" --rounds 0
    ;;
  run)
    [[ $# -ge 3 ]] || { echo "Usage: autoresearch.sh run <project> <goal> [rounds] [--config path] [--verbose]" >&2; exit 1; }
    project="$2"; goal="$3"; shift 3
    rounds="${1:-1}"; [[ "$rounds" =~ ^[0-9]+$ ]] && shift || rounds=1
    exec "$PYTHON_BIN" -m engine.loop --project "$project" --goal "$goal" --rounds "$rounds" "$@"
    ;;
  status)
    [[ $# -ge 2 ]] || { echo "Usage: autoresearch.sh status <project>" >&2; exit 1; }
    [[ -f "$2/CURRENT_STATUS.md" ]] || { echo "No status file found at $2/CURRENT_STATUS.md" >&2; exit 1; }
    exec cat "$2/CURRENT_STATUS.md"
    ;;
  analyze)
    [[ $# -ge 2 ]] || { echo "Usage: autoresearch.sh analyze <project>" >&2; exit 1; }
    latest="$(find "$2/experiments" -name post-run-analysis.md 2>/dev/null | sort | tail -n 1)"
    [[ -n "$latest" ]] || { echo "No analysis found in $2/experiments/" >&2; exit 1; }
    exec cat "$latest"
    ;;
  scan)
    [[ $# -ge 3 ]] || { echo "Usage: autoresearch.sh scan <project> <topic>" >&2; exit 1; }
    cd "$SCRIPT_DIR"
    AUTORESEARCH_PROJECT="$2" AUTORESEARCH_TOPIC="$3" exec "$PYTHON_BIN" - <<'PY'
import os, json
from engine.config import ResearchConfig
from engine.llm import LLMClient
from engine.scanner import run_scan
cfg = ResearchConfig.load(os.environ['AUTORESEARCH_PROJECT'])
llm = LLMClient(cfg.model, cfg.provider)
result = run_scan(cfg, llm, os.environ['AUTORESEARCH_TOPIC'])
print(result['summary'])
PY
    ;;
  *)
    usage
    ;;
esac
