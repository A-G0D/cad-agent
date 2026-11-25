import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(1.5, 1.5, 0.0255)
    .faces(">Z")
    .workplane()
    .rect(0.12, 0.24)
    .cutThruAll()
)
