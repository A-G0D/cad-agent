"""Local-draft -> DeepSeek fallback routing on CADPrompt. usage: route.py LOCAL_ROWS_GLOB LOCAL_POSEINV.json   (correct = pose-inv CD<0.05)
Policies: local only | DeepSeek only | gate-routed (local ok -> keep, else DeepSeek). Bootstrap 95% CI over items. Cost = DeepSeek calls fraction."""
import sys, json, glob, numpy as np
rows = {r["id"]: r for f in sorted(glob.glob(sys.argv[1])) for r in json.load(open(f))}
loc = json.load(open(sys.argv[2])); ds = json.load(open("results/cadprompt_poseinv.json"))
dsr = {r["id"]: r for r in json.load(open("results/cadprompt_merged.json"))}
ids = [i for i in rows if i in loc and i in ds]
L = np.array([loc[i] < .05 for i in ids]); D = np.array([ds[i] < .05 for i in ids]); ok = np.array([rows[i]["ok"] for i in ids])
ls = np.array([rows[i]["sec"] or 0 for i in ids]); dsec = np.array([dsr[i]["sec"] or 0 for i in ids])
R = np.where(ok, L, D); rs = ls + np.where(ok, 0, dsec); cloud = 1 - ok.mean()
rng = np.random.default_rng(0); B = [rng.integers(0, len(ids), len(ids)) for _ in range(2000)]
ci = lambda v: "%.3f [%.3f,%.3f]" % (v.mean(), *np.percentile([v[b].mean() for b in B], [2.5, 97.5]))
print(f"n={len(ids)}\nlocal only   acc {ci(L)}  p50 {np.median(ls):.1f}s\nDeepSeek only acc {ci(D)} p50 {np.median(dsec):.1f}s\ngate-routed  acc {ci(R)} cloud-call frac {cloud:.2f} p50 {np.median(rs):.1f}s p90 {np.percentile(rs,90):.1f}s")
print(f"gate-ok local: n={ok.sum()} acc {L[ok].mean():.2f} | gate-fail local acc {L[~ok].mean():.2f} (DS on those {D[~ok].mean():.2f})")
