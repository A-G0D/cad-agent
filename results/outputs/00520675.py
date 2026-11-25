import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(1.5 / 2)
    .extrude(0.6)
    .faces(">Z")
    .shell(-0.075)
    .translate((0, 0, -0.3))
)
