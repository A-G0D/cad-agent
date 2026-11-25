"""Shape-space voting experiment on the pose-inv tail: K extra temp-0.8 candidates/item; baseline vs medoid vs oracle (pose-invariant chamfer).
usage: vote.py DATA [K]  (needs agent.py env + trimesh/scipy)"""
import sys, json, glob, os, threading, numpy as np, trimesh
from agent import attempt, Worker
from pose_inv import R
from bench_cadprompt import norm, chamfer
D = sys.argv[1] + "/CADPrompt/"; TAG = os.environ.get("TAG", ""); K = int(sys.argv[2]) if len(sys.argv) > 2 else 4
pi = json.load(open("results/cadprompt_poseinv.json")); mg = {r["id"]: r for r in json.load(open("results/cadprompt_merged.json"))}
tail = [i for i, v in pi.items() if 0.05 <= v < 5]
pf = "Natural_Language_Descriptions_Prompt_with_specific_measurements.txt"
def pcd(a, b): return min(chamfer(a, b @ M.T) for M in R)
def sample(i, ws):
    prompt = open(D + i + "/" + pf).read().strip(); outs = [None] * len(ws)
    def go(k):
        r = attempt(prompt, ws[k], float(os.environ.get("TEMP", 0.8)))
        c = r.get("code") if r["ok"] else r.get("ran")
        if c and ws[k].run(c, f"/tmp/vote{TAG}_{i}_{k}").get("ok"): outs[k] = f"/tmp/vote{TAG}_{i}_{k}.stl"
    ts = [threading.Thread(target=go, args=(k,)) for k in range(len(ws))]; [t.start() for t in ts]; [t.join() for t in ts]
    return [o for o in outs if o]
if __name__ == "__main__":
    ws = [Worker() for _ in range(K)]; rows = []
    for i in tail:
        G = norm(trimesh.load(D + i + "/Ground_Truth.stl")); fs = sample(i, ws)
        base = f"/tmp/cadp_{i}.stl"
        if os.path.exists(base): fs = [base] + fs
        P = [norm(trimesh.load(f)) for f in fs]
        if len(P) < 2: continue
        n = len(P); M = np.zeros((n, n))
        for a in range(n):
            for b in range(a + 1, n): M[a, b] = M[b, a] = pcd(P[a], P[b])
        med = int(M.sum(1).argmin()); cds = [pcd(G, p) for p in P]
        rows.append(dict(id=i, n=n, base=pi[i], base_rep=cds[0] if os.path.exists(base) else None, medoid=cds[med], oracle=min(cds), mean=float(np.mean(cds)), spread=float(M.sum() / (n * (n - 1)))))
        print(json.dumps(rows[-1]), flush=True)
    json.dump(rows, open(f"results/vote{TAG}.json", "w"))
    b, m, o = (np.array([r[k] for r in rows]) for k in ("base", "medoid", "oracle"))
    print(f"n={len(rows)} median base {np.median(b):.4f} medoid {np.median(m):.4f} oracle {np.median(o):.4f}; fixed(<0.02) base {(b<.02).sum()} medoid {(m<.02).sum()} oracle {(o<.02).sum()}; medoid worse>0.01: {(m>b+.01).sum()}")
