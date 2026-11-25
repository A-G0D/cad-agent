import cadquery as cq

# Base cylinder: diameter 1.5, height 0.06
base = cq.Workplane("XY").circle(1.5 / 2.0).extrude(0.06)

# Second cylinder: diameter 0.75, height 0.375, centered on base
boss = cq.Workplane("XY").circle(0.75 / 2.0).extrude(0.375)
result = base.union(boss)

# Rectangle cut: length 0.21 (X), width 0.45 (Y), on right side of boss
# Padding 0.12 from edge of first cylinder (radius 0.75)
# Rectangle right edge at x = 0.75 - 0.12 = 0.63, so center x = 0.63 - 0.21/2 = 0.525
rect_center_x = 1.5 / 2.0 - 0.12 - 0.21 / 2.0
cut = (
    cq.Workplane("XY")
    .center(rect_center_x, 0)
    .rect(0.21, 0.45)
    .extrude(0.06)
)
result = result.cut(cut)

result = result.clean()
