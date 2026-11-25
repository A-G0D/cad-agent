import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(0.42, 0.75)
    .extrude(0.015)
)
