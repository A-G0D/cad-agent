import cadquery as cq

bottom = 0.628103
top = 0.240157
height = 0.722001
shift = 0.009237
thickness = 0.011084
dx = -0.018474

# Isosceles trapezium, bottom centered at origin, top centered at (shift, height)
bx = bottom / 2.0
tx = top / 2.0

pts = [
    (-bx, 0.0),
    (bx, 0.0),
    (shift + tx, height),
    (shift - tx, height),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
    .translate((dx, 0.0, 0.0))
)
