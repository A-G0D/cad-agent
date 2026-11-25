import cadquery as cq

L = 0.70588
W = 0.40809
H = 0.22059
r = 0.08

result = (
    cq.Workplane("XY")
    .box(L, W, H)
    .edges("|Z")
    .fillet(r)
    .translate((0, 0, H / 2))
)
