import cadquery as cq

D = 0.02262
H = 0.75
hd = 0.015476
r = D / 2.0

body = cq.Workplane("XY").circle(r).extrude(H)

z_top = H - 0.06399
z_b1 = 0.004167 + hd / 2.0
z_b2 = 0.123228

for zc in [z_top, z_b1, z_b2]:
    cutter = (
        cq.Workplane("XZ")
        .center(0, zc)
        .circle(hd / 2.0)
        .extrude(D * 2)
        .translate((0, -D, 0))
    )
    body = body.cut(cutter)

result = body
