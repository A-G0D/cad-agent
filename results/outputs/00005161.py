import cadquery as cq

d1 = 0.38527
h1 = 0.256849
d2 = 0.256849
h2 = 0.493151

result = (
    cq.Workplane("XY")
    .circle(d1 / 2)
    .extrude(h1)
    .faces(">Z")
    .workplane()
    .circle(d2 / 2)
    .extrude(h2)
)
