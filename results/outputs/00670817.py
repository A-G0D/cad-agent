import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(0.75)
    .extrude(0.113636)
    .faces(">Z")
    .workplane()
    .hole(0.738636)
)
