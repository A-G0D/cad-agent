"""v2 (post-hoc fix of decimal-truncation bug found by refuter; v1 AUC .446 was invalid). Typed one-to-one certificate (pre-registered AUC>=0.65 lower-CI>0.5 on all 187 DeepSeek outputs). usage: cert_typed.py
import os
radius/diameter numbers must match circle-ish sharp-edge components (bbox/2, bbox); length words must match extents/plane gaps/edge lengths; each measured value used once."""
import re, json, glob, numpy as np, trimesh
from cert import quantities
KW = re.compile(r"(radius|diameter|height|length|width|depth|thickness|dimensions?|measur\w*)\b((?:[^.;]|(?<=\d)\.(?=\d)){0,60})", re.I)
NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")
def typed_nums(t):
    out = []
    for m in KW.finditer(t):
        k = m.group(1).lower(); k = "r" if k == "radius" else "d" if k == "diameter" else "l"
        s = m.group(2); ns = NUM.findall(s)
        if k == "l" and m.group(1).lower() not in ("dimensions", "dimension") and not m.group(1).lower().startswith("measur"): ns = ns[:1]
        elif k != "l": ns = ns[:1]
        out += [(k, float(x)) for x in ns]
    return out
def measured(m):
    lin = list(quantities(m)); circ = []
    ed = m.face_adjacency_edges[m.face_adjacency_angles > 0.3]
    for comp in (trimesh.graph.connected_components(ed) if len(ed) else []):
        x = np.sort(np.ptp(m.vertices[list(comp)], axis=0))[::-1]
        if x[0] > 1e-6 and abs(x[0] - x[1]) < .03 * x[0]: circ.append(x[0])
    return lin, circ
def cov(t, m, tol=.015):
    tn = typed_nums(t)
    if not tn: return None, 0
    lin, circ = measured(m); lin = list(lin); circ = list(circ); hit = 0
    for k, n in tn:
        pool = {"l": lin, "d": circ, "r": circ}[k]; val = {"l": n, "d": n, "r": 2 * n}[k]
        j = next((i for i, q in enumerate(pool) if abs(q - val) <= tol * max(val, 1e-9) + 1e-4), None)
        if j is not None: hit += 1; pool.pop(j)
    return hit / len(tn), len(tn)
if __name__ == "__main__":
    from scipy.stats import rankdata
    def roc_auc_score(y, x): r = rankdata(x); n1 = y.sum(); return (r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
    PF = "Natural_Language_Descriptions_Prompt_with_specific_measurements.txt"; sc = json.load(open("results/cert_score.json")); res = {}
    for i, v in sc.items():
        t = open(f"{os.environ.get("CADPROMPT_DIR","CADPrompt")}/{i}/{PF}").read()
        c, n = cov(t, trimesh.load(f"results/cert/{i}.stl")); res[i] = (c, n, v["cd"])
    ids = [i for i in res if res[i][0] is not None]; y = np.array([res[i][2] < .05 for i in ids]); x = np.array([res[i][0] for i in ids])
    rng = np.random.default_rng(0); b = []
    for _ in range(2000):
        s = rng.integers(0, len(ids), len(ids))
        if 0 < y[s].sum() < len(s): b.append(roc_auc_score(y[s], x[s]))
    print(f"typed items {len(ids)}/{len(res)} acc {y.mean():.2f} AUC {roc_auc_score(y, x):.3f} CI95 {np.percentile(b,2.5):.3f}-{np.percentile(b,97.5):.3f} cov=1 acc {y[x>=1].mean():.2f} (n={int((x>=1).sum())}) cov<1 acc {y[x<1].mean():.2f} (n={int((x<1).sum())}) mean cov {x.mean():.2f}")
