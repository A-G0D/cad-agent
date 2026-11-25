#!/bin/bash
# needs CADDATA=<dir containing CADPrompt/> and mlx-lm. resumable: skips chunks whose result json exists; each chunk <20min under heavy lock
cd "$(dirname "$0")"
for s in 30 80 130 180; do n=50; [ $s = 180 ] && n=20
  f=results/cadprompt_q3_30b_${s}_${n}.json; [ -f $f ] && continue
  until CAD_LOCAL=mlx-community/Qwen3-30B-A3B-Instruct-2507-4bit NW=1 TAG=_q3_30b python3 bench_cadprompt.py "$CADDATA" $s $n >> results/logs/q3_30b_full.log 2>&1; do [ $? = 75 ] || break; done
done
echo DONE >> results/logs/q3_30b_full.log
