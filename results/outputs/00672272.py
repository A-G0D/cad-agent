import cadquery as cq

L = 0.647727
W = 0.051136
H = 0.025568
sl = 0.040483
sh = 0.008523

base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

xoff = L / 2.0 - sl / 2.0

pads = (
    cq.Workplane("XY")
    .pushPoints([(-xoff, 0), (xoff, 0)])
    .rect(sl, W)
    .extrude(sh)
)

result = base.union(pads)
