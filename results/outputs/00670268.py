import cadquery as cq

# Large cylinder
d1 = 0.470339
h1 = 0.75
large = cq.Workplane("XY").circle(d1 / 2).extrude(h1)

# Second cylinder
d2 = 0.152542
h2 = 0.082627
pad = 0.247881
# positioned slightly below center, at distance pad from edge
offset = d1 / 2 - pad
second = (
    cq.Workplane("XY")
    .center(0, -offset)
    .circle(d2 / 2)
    .extrude(h2)
)

# Third cylinder concentric with second
d3 = 0.075981
h3 = 0.190678
third = (
    cq.Workplane("XY")
    .center(0, -offset)
    .circle(d3 / 2)
    .extrude(h3)
)

# Union all and rotate -90 deg around Y
result = (
    large.union(second)
    .union(third)
    .rotate((0, 0, 0), (0, 1, 0), -90)
)
