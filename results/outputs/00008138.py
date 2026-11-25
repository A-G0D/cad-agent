import cadquery as cq

height = 0.75
outer_d = 0.07812
inner_d = 0.046741

result = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .extrude(height)
    .faces(">Z").workplane()
    .hole(inner_d)
    .translate((0, 0, -height / 2.0))
)
