import cadquery as cq

# Base rectangle: 0.75 x 0.75 x 0.00195
base = cq.Workplane("XY").box(0.75, 0.75, 0.00195)

# Second smaller rectangle: 0.281257 x 0.0625 x 0.00195
# Positioned connecting to right edge of base, starting halfway up its height.
# Right edge of base is at x = 0.75 (base centered at origin, half-length 0.375).
# Second rectangle's left edge touches x = 0.375, so its center x = 0.375 + 0.281257/2.
# Vertically: starts halfway up base height (z=0), so its center z = 0.00195/2 + 0.00195/2 = 0.00195.
# Actually: second rect bottom at z=0 (halfway up base's height from bottom at -0.000975 -> z=0),
# so its center z = 0 + 0.00195/2 = 0.000975. Its width centered at y=0.

second = (
    cq.Workplane("XY")
    .box(0.281257, 0.0625, 0.00195)
    .translate((0.375 + 0.281257 / 2, 0, 0.000975))
)

result = base.union(second)
