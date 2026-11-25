#!/bin/zsh
# Sequential benchmark of all backends, 2 workers each, low priority (RAM/CPU limits: one job at a time).
cd "$(dirname "$0")"; PY=${CAD_PY:-python3}
run(){ n=$1; shift; env "$@" CAD_TIMEOUT=120 nice -n 15 $PY eval.py 2 > results/$n.log 2>&1; }
run deepseek-v41-flash CAD_MODEL=deepseek-flash
run deepseek-v4-pro CAD_MODEL=deepseek-v4-pro
run haiku-5-5 CAD_CLI=claude-haiku-5-5
run sonnet-5-5 CAD_CLI=claude-sonnet-5-5
run opus-5-5 CAD_CLI=claude-opus-5-5
