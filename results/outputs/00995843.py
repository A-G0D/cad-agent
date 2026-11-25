import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(0.567213 / 2)
    .extrude(0.5625)
    .faces(">Z")
    .workplane()
    .circle(0.266022 / 2)
    .extrude(0.1875)
)
