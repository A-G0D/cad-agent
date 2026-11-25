import cadquery as cq

outer = 1.5
pad = 0.17649
h = 0.00265

result = (
    cq.Workplane("XY")
    .rect(outer, outer)
    .rect(outer - 2 * pad, outer - 2 * pad)
    .extrude(h)
)
