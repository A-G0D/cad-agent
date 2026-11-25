import cadquery as cq

b = 0.20312
h = 0.20312
e = 0.75

tri = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(b, 0)
    .lineTo(0, h)
    .close()
    .extrude(e)
)

result = tri.rotate((0, 0, 0), (0, 1, 0), -90)
