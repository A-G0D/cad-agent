"""Offline kernel benchmark: replay the CADPrompt reference CadQuery programs (no model) through kernel.metrics().
usage: bench_kernel.py CADPROMPT_DIR [kernel.py path] [passes]   Prints median ms per part for metrics(), best of N passes (parts are rebuilt each pass)."""
import sys, glob, re, time, importlib.util, statistics as st
import cadquery as cq
d = sys.argv[1]; kp = sys.argv[2] if len(sys.argv) > 2 else "kernel.py"; passes = int(sys.argv[3]) if len(sys.argv) > 3 else 7
spec = importlib.util.spec_from_file_location("k", kp); k = importlib.util.module_from_spec(spec); spec.loader.exec_module(k)
parts = []
for f in sorted(glob.glob(d + "/0*/Python_Code.py")):
    g = {"cq": cq}
    try: exec(re.sub(r".*exporters.*", "", open(f).read()) + "\nresult = part\n", g)
    except Exception: continue  # some reference programs don't run on current CadQuery
    parts.append(g["result"])
best = []
for _ in range(passes):
    ts = []
    for r in parts:
        t = time.perf_counter(); k.metrics(r); ts.append(time.perf_counter() - t)
    best.append(st.median(ts) * 1e3)
print(f"parts={len(parts)} metrics_ms_median_best_of_{passes}={min(best):.2f}")
