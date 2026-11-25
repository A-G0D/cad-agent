"""Headless render of CADPrompt parts to PNG (matplotlib Agg, no window). Needs cadquery, trimesh, numpy, matplotlib.
usage: render_parts.py CADPROMPT_DIR OUT_DIR id1 id2 ...                  reference programs only (writes OUT_DIR/<id>.png, prompts.json)
       render_parts.py --compare CADPROMPT_DIR PROGRAMS_DIR OUT_DIR id1 ...  prompt | reference | ours, writes OUT_DIR/compare_<id>.png
       (PROGRAMS_DIR/<id>.py is model output ending in `result = <Workplane>`)"""
import sys, re, os, json, textwrap, numpy as np, trimesh, cadquery as cq
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def mesh(wp, stl):
    cq.exporters.export(wp, stl); m = trimesh.load(stl); os.remove(stl)
    m.apply_translation(-m.bounds.mean(0)); m.apply_scale(1 / m.extents.max()); return m

def draw(ax, m):
    v, f = trimesh.remesh.subdivide_to_size(m.vertices, m.faces, .04); m = trimesh.Trimesh(v, f).smooth_shaded; vn = m.vertex_normals[m.faces].mean(1); vn /= np.linalg.norm(vn, axis=1, keepdims=True) + 1e-12
    sh = np.clip(vn @ np.array([.4, -.5, .75]), 0, 1) * .65 + .3; fc = np.c_[sh, sh, sh * 1.05].clip(0, 1)
    ax.add_collection3d(Poly3DCollection(m.vertices[m.faces], facecolors=fc, edgecolors=fc, linewidths=.3))
    ax.set_xlim(-.5, .5); ax.set_ylim(-.5, .5); ax.set_zlim(-.5, .5); ax.set_box_aspect((1, 1, 1), zoom=1.35); ax.view_init(25, -55); ax.set_axis_off()

def ref(D, i):
    g = {"cq": cq}; exec(re.sub(r".*exporters.*", "", open(f"{D}/{i}/Python_Code.py").read()) + "\nresult = part\n", g); return g["result"]

def ours(P, i):
    g = {"cq": cq, "__name__": "prog"}; exec(open(f"{P}/{i}.py").read(), g); return g["result"]

def aligned(D, P, O, i):  # same best-of-24 rotation the pose-invariant scorer picks; both meshes share centre and scale
    from pose_inv import R; from bench_cadprompt import norm, chamfer
    cq.exporters.export(ours(P, i), f"{O}/_{i}.stl"); b = trimesh.load(f"{O}/_{i}.stl"); os.remove(f"{O}/_{i}.stl")
    g = trimesh.load(f"{D}/{i}/Ground_Truth.stl"); np.random.seed(0); G, Q = norm(g), norm(b)
    M = min(R, key=lambda M: chamfer(G, Q @ M.T))
    for m in (g, b): m.apply_translation(-m.bounds.mean(0))
    b.vertices = b.vertices @ M.T; sc = 1 / g.extents.max()
    for m in (g, b): m.apply_scale(sc)
    return [g, b]

def prompt(D, i): return open(f"{D}/{i}/Natural_Language_Descriptions_Prompt_with_specific_measurements.txt").read().strip()

if sys.argv[1] == "--compare":
    D, P, O, ids = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]; os.makedirs(O, exist_ok=True)
    for i in ids:
        fig = plt.figure(figsize=(7.4, 3.0), dpi=150); gs = fig.add_gridspec(1, 3, width_ratios=[.75, 1, 1], wspace=0, left=0, right=1, top=.93, bottom=0)
        ax = fig.add_subplot(gs[0]); ax.axis("off"); t = textwrap.fill(prompt(D, i).replace("Write Python code using CADQuery to ", ""), 36)
        ax.text(0, 1, t[:1500] + (" ..." if len(t) > 1500 else ""), va="top", fontsize=5.3, family="monospace"); ax.set_title(f"prompt {i}", fontsize=8, loc="left")
        meshes = aligned(D, P, O, i)
        for k, name in enumerate(["reference", "ours (best-matching orientation, as scored)"]):
            a = fig.add_subplot(gs[k + 1], projection="3d"); draw(a, meshes[k]); a.set_title(name, fontsize=8)
        fig.savefig(f"{O}/compare_{i}.png", bbox_inches="tight", pad_inches=.03); plt.close(fig)
        from PIL import Image, ImageChops; im = Image.open(f"{O}/compare_{i}.png").convert("RGB"); im.crop(ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()).save(f"{O}/compare_{i}.png")
else:
    D, O, ids = sys.argv[1], sys.argv[2], sys.argv[3:]; os.makedirs(O, exist_ok=True); cards = []
    for i in ids:
        fig = plt.figure(figsize=(3, 3), dpi=110); draw(fig.add_subplot(projection="3d"), mesh(ref(D, i), f"{O}/{i}.stl"))
        fig.savefig(f"{O}/{i}.png", bbox_inches="tight", pad_inches=0); plt.close(fig)
        cards.append({"id": i, "png": f"{i}.png", "prompt": prompt(D, i)})
    json.dump(cards, open(f"{O}/prompts.json", "w"), indent=1)
