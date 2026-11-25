import cadquery as cq

L, W, H = 1.0, 0.75, 0.75
d = 0.5
r = d / 2.0

# Rectangular prism
prism = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Hollow cylinder (tube) centered in the rectangle, full height
outer = cq.Workplane("XY").circle(r).extrude(H)
inner = cq.Workplane("XY").circle(r * 0.6).extrude(H)
tube = outer.cut(inner)

# Cut and keep only the largest solid to guarantee a single solid
result = prism.cut(tube).clean()
solids = result.solids().vals()
if len(solids) > 1:
    solids.sort(key=lambda s: s.Volume(), reverse=True)
    result = cq.Workplane("XY").add(solids[0])
