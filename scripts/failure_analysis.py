"""Classify gate-fails and wrong-passes of a CADPrompt run from saved programs. No API calls.
usage: failure_analysis.py CADPROMPT_DIR rows.jsonl poseinv.json > failures.json   (then see results/failure_analysis.md)"""
import sys, json, re, numpy as np, trimesh
from agent import Worker
D, rows_f, pi_f = sys.argv[1:4]
rows = [json.loads(l) for l in open(rows_f) if l.startswith('{"id"')]; pi = json.load(open(pi_f)); w = Worker(); out = []
for r in rows:
    i = r["id"]; p = pi.get(i, 5.196); wrong = r["ok"] and (r["cd"] >= .05)
    if r["ok"] and not wrong: continue
    code = open(f"results/outputs/{i}.py").read(); m = w.run(code) if code.strip() else {"ok": False, "error": "no program"}
    g = trimesh.load(f"{D}/{i}/Ground_Truth.stl"); gb = np.sort(g.extents)
    d = dict(id=i, kind="wrong_pass" if wrong else "gate_fail", cd=r["cd"], pose=p, volratio=r.get("volratio"), fb=r["fb"], err=m.get("error"))
    if m.get("ok"):
        mb = np.sort(m["bbox"]); d["bbox_ratio"] = (mb / gb).round(3).tolist(); d["holes"] = m["holes"]; d["solids"] = m["solids"]; d["valid"] = m["valid"]
    d["code_hint"] = [k for k in ("fillet", "chamfer", "shell", "revolve", "loft", "sweep", "polyline", "workplane(\"XZ\")", "workplane(\"YZ\")", "Workplane(\"XZ\")", "Workplane(\"YZ\")") if k in code]
    out.append(d)
json.dump(out, sys.stdout, indent=0)
