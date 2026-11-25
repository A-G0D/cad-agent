import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(0.66788, 0.75)
    .extrude(0.32847)
)
