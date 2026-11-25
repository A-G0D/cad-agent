import cadquery as cq

cyl_h = 0.681818
cyl_d = 0.681818
top_d = 1.5
top_h = 0.252273

result = (
    cq.Workplane("XY")
    .circle(cyl_d / 2.0)
    .extrude(cyl_h)
    .faces(">Z")
    .workplane()
    .circle(top_d / 2.0)
    .extrude(top_h)
)
