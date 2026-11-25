import cadquery as cq

d = 0.374906
h = 0.1875

circle = (
    cq.Workplane("XY")
    .moveTo(d / 2, d * 2 - 0.187124)
    .circle(d / 2)
    .extrude(h)
)

poly = (
    cq.Workplane("XY")
    .polyline([(0, 0), (0, d), ((d * 0.7) + 0.01883 - 0.0001, d)])
    .close()
    .extrude(h)
)

result = circle.union(poly).translate((0, 0, -h / 2))
