import cadquery as cq
s = 0.86802
h = 0.152284
result = (
    cq.Workplane("XY")
    .moveTo(-s/2, 0)
    .lineTo(s/2, 0)
    .lineTo(s/2, s)
    .threePointArc((0, s + s/2), (-s/2, s))
    .close()
    .extrude(h)
)
