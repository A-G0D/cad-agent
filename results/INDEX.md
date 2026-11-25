# Results index

Each README number and the file it comes from.

| README number | File |
|---|---|
| CADPrompt-200, DeepSeek flash: compile 95.5%, gate ok 86.5%, median 3.83 s | `cadprompt_merged.json` (first pass `cadprompt_0_200.json` merged with the failure rerun `cadprompt_0_200_rerun.json`; logs `logs/cadprompt_full.log`, `logs/cadprompt_rerun_fail.log`) |
| Three-run table: pose-invariant 157 / 161 / 162 of 200, strict 110 / 117 / 121, gate pass 152 / 147 / 147, median 4.77 / 3.51 / 3.68 s | `cadprompt_fresh.jsonl` + `_poseinv.json`, `cadprompt_fix23.*`, `cadprompt_fix123.*`; programs of the last run in `outputs/<id>.py` |
| Cost per run $0.23 / $0.15 / $0.13 (total $0.80 incl. screens) | `spend.log` (balance before/after each run); `screen_fix*.jsonl` are the 74-item screens |
| Earlier run pose-invariant 151/200 | `cadprompt_poseinv.json` |
| Qwen3-30B-A3B 106/200 | `q3_30b_poseinv_all.json`, chunks `cadprompt_q3_30b_*.json`, `logs/q3_30b_full.log` |
| Qwen3-4B (not fine-tuned) 17/30 | `cadprompt_q3_4b_0_30.json`, `q3_4b_poseinv.json`, `logs/q3_4b.log` |
| 44-case suite per model | `deepseek-v41-flash.log`, `deepseek-v4-pro.log`, `haiku-5-5.log`, `sonnet-5-5.log`, `opus-5-5.log` (suite A + B, last lines) |
| Suite B on DeepSeek, 13/15 | `logs/hard.log` |
| Gate vs certificate AUC .542 | `cert_score.json`, `gt_cov.json`, `cert/` |
| `vote*.json` | majority-vote experiment, not cited in the README |
