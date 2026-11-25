import cadquery as cq

L = 0.848067
W = 0.197368
d_small = 0.157782
d_large = 0.196626
d_hole = 0.094737
t = 0.05

r_small = d_small / 2.0
r_large = d_large / 2.0
r_hole = d_hole / 2.0

x_small = -L / 2.0 + r_small
x_large = L / 2.0 - r_large

body = (
    cq.Workplane("XY")
    .moveTo(x_small, -W / 2.0)
    .lineTo(x_large, -W / 2.0)
    .lineTo(x_large, W / 2.0)
    .lineTo(x_small, W / 2.0)
    .close()
    .extrude(t)
)

small_end = (
    cq.Workplane("XY")
    .center(x_small, 0)
    .circle(r_small)
    .extrude(t)
)

large_end = (
    cq.Workplane("XY")
    .center(x_large, 0)
    .circle(r_large)
    .extrude(t)
)

wrench = body.union(small_end).union(large_end)

# Cut the two through holes using explicit cylinders for exact diameter
hole_small = (
    cq.Workplane("XY")
    .center(x_small, 0)
    .circle(r_hole)
    .extrude(t)
)
hole_large = (
    cq.Workplane("XY")
    .center(x_large, 0)
    .circle(r_hole)
    .extrude(t)
)

wrench = wrench.cut(hole_small).cut(hole_large)

result = wrench
