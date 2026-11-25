import cadquery as cq

outer_d = 1.5
inner_d = 1.45232
height = 0.01463

result = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .hole(inner_d)
)
