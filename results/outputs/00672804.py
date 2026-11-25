import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(1.5, 1.5)
    .extrude(0.1125)
    .faces(">Z")
    .workplane()
    .hole(0.15)
)
