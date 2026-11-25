import cadquery as cq

cyl_h = 0.468766
cyl_d = 1.31858
cyl_r = cyl_d / 2.0

prism_l = 1.5
prism_w = 0.1875
prism_h = 0.075

cylinder = cq.Workplane("XY").circle(cyl_r).extrude(cyl_h)
prism = (
    cq.Workplane("XY")
    .box(prism_l, prism_w, prism_h, centered=(True, True, True))
    .translate((0, 0, cyl_h + prism_h / 2.0))
)
result = cylinder.union(prism)
