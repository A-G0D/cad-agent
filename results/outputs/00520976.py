import cadquery as cq

# Base square 0.75 x 0.75, extruded 0.25 in Z
base = cq.Workplane("XY").rect(0.75, 0.75).extrude(0.25)

# Smaller square 0.15 x 0.15 at top-right corner, cut downward 0.5
# Top-right corner of base is at (0.375, 0.375); smaller square shares that corner
cut = (
    cq.Workplane("XY")
    .center(0.375 - 0.075, 0.375 - 0.075)
    .rect(0.15, 0.15)
    .extrude(0.5)
)

result = base.cut(cut)
