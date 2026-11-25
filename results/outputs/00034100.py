import cadquery as cq

L = 0.47368
W = 0.31579
H = 0.75
hole_d = 0.196206
hole_r = hole_d / 2.0
slit_w = 0.007895
slit_depth = 0.196132

cyl_top_z = H - 0.146132
cyl_bottom_z = -1.0
cyl_height = cyl_top_z - cyl_bottom_z

hole_cy = W / 2.0

slit_top_z = H
slit_height = slit_depth

slit_y_start = 0.0
slit_y_end = hole_cy
slit_len = slit_y_end - slit_y_start

base = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
)

hole = (
    cq.Workplane("XY")
    .workplane(offset=cyl_top_z)
    .center(0, 0)
    .circle(hole_r)
    .extrude(-cyl_height)
)

slit = (
    cq.Workplane("XY")
    .workplane(offset=slit_top_z)
    .center(0, -(W / 2.0) + slit_len / 2.0)
    .rect(slit_w, slit_len)
    .extrude(-slit_height)
)

result = base.cut(hole).cut(slit)
