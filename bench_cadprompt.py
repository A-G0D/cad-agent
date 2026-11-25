"""CADPrompt benchmark (CADCodeVerify, arXiv 2410.05340). usage: bench_cadprompt.py DATA_DIR [start] [n] [prompt_variant]
Metric: symmetric chamfer of 10k surface samples, each mesh centered + scaled to unit max-extent, NO ICP (stricter than paper); fail = 3*sqrt(3)."""
import sys, os, json, glob, numpy as np, trimesh
from scipy.spatial import cKDTree
from agent import design, Worker
FAIL = 3 * 3 ** .5
def norm(m):
    p = m.sample(10000); p = p - (m.bounds.sum(0) / 2); return p / (m.extents.max() or 1)
def chamfer(a, b):
    ta, tb = cKDTree(a), cKDTree(b); return float((tb.query(a)[0].mean() + ta.query(b)[0].mean()) / 2)
def score(gt_stl, pred_stl):
    g = trimesh.load(gt_stl); p = trimesh.load(pred_stl)
    return chamfer(norm(g), norm(p)), float(p.volume / g.volume) if g.volume else 0.0
if __name__ == "__main__":
    d, start, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0, int(sys.argv[3]) if len(sys.argv) > 3 else 200
    pf = sys.argv[4] if len(sys.argv) > 4 else "Natural_Language_Descriptions_Prompt_with_specific_measurements.txt"
    ws = [Worker() for _ in range(int(os.environ.get("NW", 2)))]; os.makedirs("results", exist_ok=True); rows = []
    for dd in sorted(glob.glob(d + "/CADPrompt/0*"))[start:start + n]:
        if os.environ.get('IDS') and os.path.basename(dd) not in open(os.environ['IDS']).read().split(): continue
        prompt = open(f"{dd}/{pf}").read().strip(); out = f"/tmp/cadp_{os.path.basename(dd)}"
        [os.path.exists(out+e) and os.remove(out+e) for e in (".stl", ".step")]; r = design(prompt, ws, out)  # stale outputs cleared above: a failed run must not be scored on a previous run's STL
        os.makedirs("results/outputs", exist_ok=True); open(f"results/outputs/{os.path.basename(dd)}.py", "w").write(r.get("code") or "")
        row = dict(id=os.path.basename(dd), ok=r["ok"], fb=r.get("fallback", False), sec=r.get("seconds"), tries=r.get("tries"), tok=sum(r["usage"]))
        try: row["cd"], row["volratio"] = score(dd + "/Ground_Truth.stl", out + ".stl")
        except Exception as e: row["cd"], row["volratio"] = FAIL, 0.0; row["err"] = str(e)[:80]
        rows.append(row); print(json.dumps(row), flush=True)
    cds = np.array([r["cd"] for r in rows]); print(f"n={len(rows)} compile={np.mean([r['cd']<FAIL for r in rows]):.3f} cd_median={np.median(cds):.3f} cd_mean={cds.mean():.3f} sec_median={np.median([r['sec'] or 0 for r in rows]):.2f}")
    json.dump(rows, open(f"results/cadprompt{os.environ.get('TAG','')}_{start}_{n}{'_rerun' if os.environ.get('IDS') else ''}.json", "w"))
