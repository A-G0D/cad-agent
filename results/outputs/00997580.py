import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(1.125, 1.5)
    .extrude(0.06)
    .faces(">Z")
    .workplane()
    .rect(0.3825, 0.7575)
    .cutBlind(-0.03)
)
