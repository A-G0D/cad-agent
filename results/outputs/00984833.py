import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(0.475652, 0.049547)
    .extrude(0.317101)
    .faces(">Z")
    .workplane()
    .rect(0.475652, 0.198188)
    .extrude(0.317101)
)
