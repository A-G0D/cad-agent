import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(0.75, 0.5)
    .extrude(0.75)
    .faces(">Z")
    .workplane()
    .center(0, 0.125)
    .rect(0.25, 0.5)
    .cutBlind(-0.25)
)
