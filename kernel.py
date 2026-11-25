# Persistent CadQuery worker: JSON lines in/out. Pre-imports cq once (1.25s) so each exec costs ~10ms.
import sys, json, math, traceback, time
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface

def metrics(r):
    sol = r.val() if isinstance(r, cq.Workplane) else r
    shapes = r.vals() if isinstance(r, cq.Workplane) else [r]
    comp = cq.Compound.makeCompound(shapes) if len(shapes) > 1 else sol
    bb = comp.BoundingBox()
    holes = {}
    faces = comp.Faces()  # wrapping faces costs ~3 ms; do it once
    for f in faces:
        if f.geomType() != "CYLINDER": continue
        c = f.Center()  # hole = cylinder whose axis point lies outside material
        cyl = BRepAdaptor_Surface(f.wrapped).Cylinder()  # CadQuery 2.8 _geomAdaptor() can return a trimmed surface without .Cylinder()
        r_, loc, axis = cyl.Radius(), cyl.Location(), cyl.Axis().Direction()
        ap = cq.Vector(loc.X(), loc.Y(), loc.Z())
        ad = cq.Vector(axis.X(), axis.Y(), axis.Z())
        # project face center onto axis for a point on the axis
        sp = f.positionAt(0.5, 0.5); n = f.normalAt(sp)
        t = (sp - ap).dot(ad); p = ap + ad * t
        outside = n.dot(p - sp) > 0  # normal points toward axis => concave => hole
        if outside:
            k = round(2 * r_, 2); holes.setdefault(k, set()).add((round(ap.x, 1), round(ap.y, 1), round(ap.z, 1), round(abs(ad.x), 1), round(abs(ad.y), 1), round(abs(ad.z), 1)))
    return {"ok": True, "valid": bool(comp.isValid()), "solids": len(comp.Solids()), "volume": round(comp.Volume(), 3),
            "bbox": [round(bb.xlen, 3), round(bb.ylen, 3), round(bb.zlen, 3)],
            "bbox_min": [round(bb.xmin, 3), round(bb.ymin, 3), round(bb.zmin, 3)],
            "faces": len(faces), "holes": {str(d): len(v) for d, v in sorted(holes.items())}}, comp

def run(code, out=None):
    t = time.perf_counter(); g = {"cq": cq, "math": math}
    exec(code, g)
    r = g.get("result")
    if r is None: return {"ok": False, "error": "no `result` variable"}
    m, comp = metrics(r)
    if out:
        cq.exporters.export(cq.Workplane(obj=comp), out + ".step"); cq.exporters.export(cq.Workplane(obj=comp), out + ".stl")
    m["exec_s"] = round(time.perf_counter() - t, 4); return m

if __name__ == "__main__":
    print("ready", flush=True)
    for line in sys.stdin:
        req = json.loads(line)
        try: res = run(req["code"], req.get("out"))
        except Exception as e: res = {"ok": False, "error": f"{type(e).__name__}: {e}"[:400]}
        print(json.dumps(res), flush=True)
