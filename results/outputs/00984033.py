import cadquery as cq

L = 1.5
W = 0.017559
H = 0.546823
d = 0.301003
x1 = 0.446488
y_top = 0.050167
pitch = d + 0.050167

# Build plate in XY plane: length along X, width along Y, height along Z
plate = cq.Workplane("XY").box(L, W, H, centered=False)

# Hole centers: x1 from left edge, y_top from top edge (top edge at Y=W)
y_center = W - y_top
xs = [x1, x1 + pitch, x1 + 2 * pitch]

# Cut holes through the full height using a single workplane on top face
plate = (
    plate.faces(">Z").workplane()
    .pushPoints([(x, y_center - W / 2.0) for x in xs])
    .hole(d)
)

# Rotate 180 degrees around Z
result = plate.rotate((0, 0, 0), (0, 0, 1), 180)
