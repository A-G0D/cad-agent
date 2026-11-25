import cadquery as cq

head = cq.Workplane("XY").polygon(6, 0.61859).extrude(0.214286)
shaft = (
    cq.Workplane("XY")
    .circle(0.321427 / 2)
    .extrude(-0.75025)
)
result = head.union(shaft)
