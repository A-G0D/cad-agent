import cadquery as cq

h1, d1 = 0.248985, 0.192096
h2, d2 = 0.220645, 0.13302
h3, d3 = 0.070261, 0.250707
d_hole = 0.098666
r_hole = d_hole / 2

c1 = cq.Workplane("XY").circle(d1 / 2).extrude(h1)
c2 = cq.Workplane("XY").workplane(offset=h1).circle(d2 / 2).extrude(h2)
c3 = cq.Workplane("XY").workplane(offset=h1 + h2).circle(d3 / 2).extrude(h3)

solid = c1.union(c2).union(c3)

# Explicit through-hole cylinder cut over full height, centered on axis
hole = (
    cq.Workplane("XY")
    .workplane(offset=-1.0)
    .circle(r_hole)
    .extrude(h1 + h2 + h3 + 2.0)
)

result = solid.cut(hole)
