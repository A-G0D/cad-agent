import cadquery as cq

L = 0.525
W = 0.75
H = 0.1125
short_base = 0.3

# Rectangle block: length L along X, width W along Y, height H along Z
rect = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Trapezium profile in XZ plane: longer base = L (bottom), shorter base = short_base (top)
# height = H, extruded along Y by W
trap_pts = [
    (-L / 2, 0),
    (L / 2, 0),
    (short_base / 2, H),
    (-short_base / 2, H),
]

trap = (
    cq.Workplane("XZ")
    .polyline(trap_pts)
    .close()
    .extrude(W)
)

# The XZ workplane extrudes along -Y by default; center it on Y
trap = trap.translate((0, W / 2, 0))

# Place trapezium on top of the rectangle
trap = trap.translate((0, 0, H))

result = rect.union(trap)
