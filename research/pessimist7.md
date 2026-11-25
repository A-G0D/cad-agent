# Pessimist 7 (cad) — A/B/C teardown
Search was snippet-level (WebSearch + abstract fetches); full texts NOT read.

## VERIFIED (from fetched pages)
- CADCodeVerify + CADPrompt (ICLR'25): VLM Q&A verification -> refinement loop; GPT-4 7.30% PCD reduction. https://arxiv.org/abs/2410.05340
- CAD-Judge: compiler-as-judge CD reward + compile-check/resample/agentic refine. https://arxiv.org/abs/2508.04002
- CAD-Coder: CD + format reward GRPO. https://arxiv.org/abs/2505.19713
- CADTests / CADTestBench (May 2026): executable tests of geometric/topological prompt requirements; "CADTests can guide generation, simple baselines outperform current methods". This IS direction A+B, published. https://arxiv.org/abs/2605.07807 (body not read; repo/HF dataset linked there)
- Verifier-free consensus selection (NeurIPS 2026): geometric consensus beats a SOTA method's verifier and random, CD -1..10%. Matches our vote.py result (medoid tiny gain). https://neurips.cc/virtual/2026/172902
- Zoo Zookeeper: agent with engine-level inspect/snapshot/debug tools, mass/volume props; no documented dimension certificate. https://zoo.dev/press/zoo-introduces-zookeeper
- CADialogue: search returned nothing; unverified.

## INFERRED
- "Independent verifier as moat" is not novel and not defensible: CADTests publishes the open, executable version. Moat claim dead unless we ship a better test suite, and our own cert has AUC .56.
- A: cert noise ceiling = prompt/GT inconsistency; the p=.065 subgroup is post hoc, subgroup chosen using GT (not available at deploy) -> selection bias; cannot be a deployable gate. Typed matching adds parser degrees of freedom -> forking-paths risk unless frozen before looking.
- B: repair loop fed by a cert with AUC .56 feeds noise; CADCodeVerify's gain is ~7% with a VLM; ceiling small. Also loop contaminates cert-as-independent-verifier (Goodhart: generator optimizes the checker).
- C: only direction with a measurable, non-label-dependent outcome (cost/latency/accuracy are real). Gate-ok already informative on DeepSeek (79.8 vs 48.1). Local 30B 76.7% vs 93.3% at n=30 (CI ~±15, not ±8 at those rates).
- Unmarketable: single-part CADPrompt accuracy; customers (Zoo, Leo) compete on integration, not certificates.

## Verdict
KILL B (dominated, circular). DEMOTE A to a 1-hour frozen test, not a project. SURVIVE C, run on n=200 with gate-ok as router.
Minimal decisive test: freeze typed-cert parser, run on existing 187 DeepSeek outputs, pre-register AUC>=0.65 (lower CI bound > .5) on the FULL set (no GT-based subgroup). Fail -> drop moat claim. In parallel: C on n=200, report routed accuracy vs DeepSeek-only at cost/latency, with bootstrap CIs.
