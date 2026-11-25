import cadquery as cq

result = (
    cq.Workplane("XY")
    .center(0.375, 0.25)
    .rect(0.75, 0.5)
    .extrude(0.25)
    .faces(">Z")
    .workplane()
    .center(0, -0.125)
    .rect(0.25, 0.25)
    .cutThruAll()
)
