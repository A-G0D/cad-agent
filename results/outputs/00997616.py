import cadquery as cq

W = 1.30586
H_rect = 0.616516
H_total = 1.25576
H_tri = H_total - H_rect
cb = 0.019678
ch = 0.101205
t = 0.023051

# Build pentagon profile in XY (rectangle + isosceles triangle on top), centered on rect
pts = [
    (-W/2, 0),
    (W/2, 0),
    (W/2, H_rect),
    (0, H_total),
    (-W/2, H_rect),
]

# We'll construct via workplane polyline
wp = cq.Workplane("XY")

# Start at bottom-left, go clockwise/counterclockwise to form face
outer = (
    wp.moveTo(-W/2, 0)
      .lineTo(W/2, 0)
      .lineTo(W/2, H_rect)
      .lineTo(0, H_total)
      .lineTo(-W/2, H_rect)
      .close()
)

# Cut corner triangles from bottom-left and bottom-right
# Bottom-left triangle: base along bottom from (-W/2,0) to (-W/2+cb,0), height up ch
bl = cq.Workplane("XY").moveTo(-W/2, 0).lineTo(-W/2 + cb, 0).lineTo(-W/2, ch).close()
# Bottom-right triangle: base from (W/2-cb,0) to (W/2,0), height up ch
br = cq.Workplane("XY").moveTo(W/2 - cb, 0).lineTo(W/2, 0).lineTo(W/2, ch).close()

# Build face then cut
solid = outer.extrude(t)
cut1 = bl.extrude(t)
cut2 = br.extrude(t)

result = solid.cut(cut1).cut(cut2)

# Rotate -90 about Z
result = result.rotate((0, 0, 0), (0, 0, 1), -90)

# Translate to center at (0.605354, -0.75, 0) - center of bbox
# After rotation: original X range [-W/2, W/2] -> Y range [-W/2, W/2]; original Y [0, H_total] -> X [-H_total, 0]
# bbox after rotation: X in [-H_total, 0], Y in [-W/2, W/2], Z in [0, t]
# Center = (-H_total/2, 0, t/2)
cx = -H_total/2
cy = 0
cz = t/2
dx = 0.605354 - cx
dy = -0.75 - cy
dz = 0 - cz
result = result.translate((dx, dy, dz))
