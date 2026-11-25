# Failure analysis, fresh CADPrompt-200 run

Source: `cadprompt_fresh.jsonl` (DeepSeek flash, 200 items), re-executed by `scripts/failure_analysis.py`, joined with `cadprompt_fresh_poseinv.json`.
"cd" is the no-ICP chamfer, "pose" is the pose-invariant chamfer (`pose_inv.py`, min over 24 axis rotations); both are correct below 0.05.
Gate-fail = the gate rejected the final attempt (48 items). Wrong-pass = gate passed but no-ICP cd >= 0.05 (61 items).

| Group | Cause | Count | Example |
|---|---|---|---|
| gate-fail | Program did not run or no program (fillet BRep error, no solid on stack, list used as Workplane, format failure, missing STL) | 7 | 00986712 |
| gate-fail | Program runs, geometry correct (pose < 0.05); the model's own spec disagreed with the build (bbox tolerance, hole count, volume), so retries were wasted | 31 | 00521230 |
| gate-fail | Program runs, geometry wrong (pose >= 0.05), including 1e4 to 1e6 volume ratios from unit mix-ups | 10 | 00673733 |
| wrong-pass | Orientation or axis only: shape right, pose differs from the reference (pose < 0.05); 4 of these are also 1000x scale | 35 | 00001411 |
| wrong-pass | Regular polygon given a side length; ours used circumradius = side, reference passes the number as polygon(n, d), so about 2x too large | 4 | 00853706 |
| wrong-pass | Other dimension or feature errors (bbox axis off by 5% to 3x, missing feature); no single cause found | 22 | 00017291 |

Notes
- The 35 orientation-only items and the 31 spec-mismatch gate-fails cost nothing under the pose-invariant score; they matter for the strict no-ICP number and for retry cost.
- The polygon cause was read from three reference programs (00853706, 00997785, 00670441); 00689964 is counted by the same bbox signature, not by reading its reference.
- Prompts say "units" or meters; the system prompt says millimetres. The model sometimes converts (00998300 ran at 1000x). The pose score is scale-invariant, so this only shows in no-ICP.
- Fixes (now on by default, opt out with CAD_NO_FIX1/2/3; see README): CAD_FIX1 error-specific retry hints (7 crashes), CAD_FIX2 polygon and unit rules (4 + scale items), CAD_FIX3 one retry when a prompt number appears nowhere in the code. On the fresh run FIX3's check flagged 33 passing programs, of which only 5 were wrong, so expect little gain from it; that is why it is a flag.
