# optimist7: verifier + spec as moat, text-to-CAD (2026-10-17)

## Prior art
VERIFIED (search-result snippets only; no full-text read):
- CADCodeVerify (Alrashedy et al.), VLM visual feedback on CAD code, CADPrompt benchmark, ~7.3% PCD reduction on GPT-4: https://arxiv.org/abs/2410.05340
- CAD-Coder: CadQuery + CoT + Chamfer-distance GRPO reward (needs GT; training-time): https://arxiv.org/abs/2505.19713
- CAD-Judge: compiler-as-judge/review, resample on compile failure; semantic feedback listed as future work: https://arxiv.org/abs/2508.04002
- CADSmith: multi-agent CadQuery, outer loop checks OCC bbox/volume/validity + VLM judge (closest to us): https://arxiv.org/abs/2603.26512
- CADCrafter is IMAGE-to-CAD (DPO with code checker), not text: https://openaccess.thecvf.com/content/CVPR2025/papers/Chen_CADCrafter_Generating_Computer-Aided_Design_Models_from_Unconstrained_Images_CVPR_2025_paper.pdf
- Verifier-free consensus selection for CAD (NeurIPS 2026): https://neurips.cc/virtual/2026/172902
- ProCAD clarify-before-draw (asks user on under-specified dims): https://icml.cc/virtual/2026/poster/66672
- Pointer-CAD v2 "dimension-aware precision": https://arxiv.org/pdf/2606.29301
- Zoo Zookeeper: parametric B-Rep, engine-level inspect/debug tools; NO documented spec-vs-geometry check found: https://zoo.dev/docs/zoo-design-studio/text-to-cad
- Code-model abstention/deferral (not CAD): https://conf.researchr.org/details/icse-2026/icse-2026-nier/47/When-to-Answer-and-When-to-Defer-A-Decision-Framework-for-Reliable-Code-Predictions

## Genuinely unoccupied (INFERRED from absence in ~3 searches; CADSmith/Pointer-CAD v2 not read in full -- must check before claiming)
1. A kernel-measured, prompt-number-to-feature one-to-one certificate returned WITH the part (spec-conformance artifact), vs. internal loop signal.
2. Risk-coverage / abstention curves on CAD with a geometric verifier as the confidence score.
3. Local-draft -> cloud-fallback routed by a geometric certificate (cost/accuracy Pareto).
Occupied: VLM critic loops, bbox/volume checks, resampling on compile failure, consensus selection.

## 10x version (INFERRED/idealized)
"Warranty CAD": every part ships with a typed certificate: each spec number -> (feature, measured value, tol, PASS/MISS/AMBIGUOUS), signed with the kernel version. Router: local 30B drafts (7s, $0), cert PASS -> ship; MISS -> repair with the typed miss list (one shot) -> still MISS -> cloud -> still MISS -> abstain/ask (ProCAD-style). Product claim = "x% of parts auto-certified at y% precision", sold as a risk-coverage curve, not a model. Moat = typed spec parser + held-out verified-pair corpus (which also trains the local model).

## Honest state (VERIFIED from STATUS.md / results)
Current untyped cert: AUC .56 -> cannot route yet. GTcov=1 subset n=102: cov=1 84% vs 65% (p=.065, post hoc). Only 20 of 102 have cov<1 (7 wrong, 13 right): too few to power anything. Prior misses are often bare fractions (0.75, 0.0625) = likely mis-parsed numbers, not wrong geometry -> the "miss list" is noisy; typed matching must fix that first.

## Cheapest experiment (<=1h, ~$0.05): miss-list repair vs blind retry
Set: 20 items with GTcov=1 and cov<1 (results/cert_score.json, results/gt_cov.json). For each, one DeepSeek-flash call given original prompt + previous code + "these prompt numbers not found in your output: [miss]" (A), and one with generic "retry, previous code was likely wrong" (B, control). Re-run, recompute pose-inv CD<0.05 and cov. Metric: fixes among the 7 wrong, breaks among the 13 right, A vs B. Success = A fixes >=3/7 with <=1 break and beats B. Also free (no API): bucket the 20 misses into integer/decimal-length vs fraction-like to see how much is parser noise. n tiny -> only a go/no-go for building the typed cert, not a result.
Why this one: tests the repair loop and the miss-list's information content directly; the router needs a cert that discriminates, which we don't have, so routing/selective-prediction experiments would be premature (AUC .56 gives a flat risk-coverage curve by construction).
