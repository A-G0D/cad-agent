import cadquery as cq

L = 1.23418
W = 0.617188
H = 0.75
cyl_h = 0.140625
cyl_d = 0.380469
pad = 0.118359

# base prism sitting on z=0
base = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# two cylinders connected at the bottom center, parallel to Z
spacing = L - 2 * pad - cyl_d
x_off = spacing / 2.0
cyls = (
    cq.Workplane("XY")
    .pushPoints([(-x_off, 0), (x_off, 0)])
    .circle(cyl_d / 2.0)
    .extrude(cyl_h)
    .translate((0, 0, -cyl_h))
)

result = base.union(cyls)
