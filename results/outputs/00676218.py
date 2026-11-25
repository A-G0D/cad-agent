import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(1.5, 1.5)
    .extrude(0.023438)
    .faces(">Z").workplane()
    .rect(1.5 - 2*0.05625, 1.5 - 2*0.05625)
    .extrude(0.023438)
)
