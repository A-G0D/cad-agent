import cadquery as cq

# Dimensions
rect_len = 0.75
rect_w = 0.75
semi_d = 0.75
semi_r = semi_d / 2.0
height = 0.16071
hole_d = 0.267857

# Rectangle body
rect = cq.Workplane("XY").rect(rect_len, rect_w).extrude(height)

# Semi-circle bulging downward from bottom edge
semi = (
    cq.Workplane("XY")
    .moveTo(-semi_r, 0)
    .threePointArc((0, -semi_r), (semi_r, 0))
    .close()
    .extrude(height)
)

body = rect.union(semi)

# Circular cutout at center of semi-circle
body = body.faces(">Z").workplane().hole(hole_d)

result = body
