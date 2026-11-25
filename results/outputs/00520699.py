import cadquery as cq

# Bulb: cylinder diameter 0.15, height 0.0375
bulb = cq.Workplane("XY").circle(0.075).extrude(0.0375)

# Stem: rectangle 0.691425 x 0.093715, height 0.02625, placed at top edge of bulb
stem = (
    cq.Workplane("XY")
    .rect(0.691425, 0.093715)
    .extrude(0.02625)
    .translate((0.691425 / 2, 0, 0))
)

# Union bulb and stem
result = bulb.union(stem)
