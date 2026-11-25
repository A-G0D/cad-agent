"""Independent dimension certificate: every number in the prompt must match a geometric quantity measured from the output STL
(not from the LLM's own spec). usage: cert.py gen DATA START N  (DeepSeek, resumable, writes results/cert/ID.stl+json) | cert.py score DATA"""
import sys, os, re, json, glob, numpy as np, trimesh
NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")
def prompt_nums(t): return [float(x) for x in NUM.findall(t)]
def quantities(m):
    q = list(m.extents); q += [e / 2 for e in m.extents]
    f = m.facets  # coplanar face groups -> distances between parallel planes
    if len(f):
        n = np.array([m.facets_normal[i] for i in range(len(f))]); o = np.array([m.facets_origin[i] for i in range(len(f))])
        for i in range(len(f)):
            d = np.abs(np.einsum("ij,j->i", o - o[i], n[i])); par = np.abs(np.abs(n @ n[i]) - 1) < 1e-3; q += list(d[par & (d > 1e-6)])
    ed = m.face_adjacency_edges[m.face_adjacency_angles > 0.3]
    if len(ed):
        v = m.vertices; q += list(np.linalg.norm(v[ed[:, 0]] - v[ed[:, 1]], axis=1))
        for comp in trimesh.graph.connected_components(ed):  # sharp-edge components: bbox = circle diameter / feature size
            x = np.ptp(v[list(comp)], axis=0); q += list(x) + list(x / 2)
    for ax in range(3):  # sketch coordinates: |coord| from origin and spacing between coordinate values (positions, offsets)
        u = np.unique(m.vertices[:, ax].round(4))[:80]; q += list(np.abs(u)); q += [] if os.environ.get('STRICT') else list(np.abs(u[:, None] - u[None]).ravel())
    a = np.degrees(m.face_adjacency_angles); q += list(np.unique(a.round(1))) + ([] if os.environ.get('STRICT') else list(180 - np.unique(a.round(1))))
    return np.array(q)
def coverage(prompt, m, tol=float(os.environ.get('TOL', 0.015))):
    ns = prompt_nums(prompt); 
    if not ns: return 1.0, []
    q = quantities(m); miss = [n for n in ns if not (np.abs(q - n) <= tol * max(n, 1e-9) + 1e-4).any()]
    return 1 - len(miss) / len(ns), miss
if __name__ == "__main__":
    mode, d = sys.argv[1], sys.argv[2]; PF = "Natural_Language_Descriptions_Prompt_with_specific_measurements.txt"
    dirs = sorted(glob.glob(d + "/CADPrompt/0*")); os.makedirs("results/cert", exist_ok=True)
    if mode == "gen":
        from agent import design, Worker
        a, n = int(sys.argv[3]), int(sys.argv[4]); ws = [Worker(), Worker()]
        for dd in dirs[a:a + n]:
            i = os.path.basename(dd); o = f"results/cert/{i}"
            if os.path.exists(o + ".json"): continue
            r = design(open(f"{dd}/{PF}").read().strip(), ws, o)
            json.dump({k: r[k] for k in ("ok", "seconds", "tries") if k in r} | {"fb": r.get("fallback", False), "stl": os.path.exists(o + ".stl")}, open(o + ".json", "w")); print(i, r["ok"], flush=True)
    else:
        from bench_cadprompt import norm, chamfer, FAIL
        from pose_inv import R
        out = {}
        for dd in dirs:
            i = os.path.basename(dd); o = f"results/cert/{i}"
            if not os.path.exists(o + ".stl"): continue
            m = trimesh.load(o + ".stl"); G = norm(trimesh.load(dd + "/Ground_Truth.stl")); P = norm(m)
            cd = min(chamfer(G, P @ M.T) for M in R); cov, miss = coverage(open(f"{dd}/{PF}").read(), m)
            out[i] = dict(cd=cd, cov=cov, miss=miss, ok=json.load(open(o + ".json"))["ok"])
        json.dump(out, open("results/cert_score.json", "w")); print(len(out))
