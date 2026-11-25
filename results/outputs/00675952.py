import cadquery as cq

base = 1.49593
top = 0.910569
height = 0.382114
shift = 0.026423
width = 0.589754

pts = [
    (-base / 2 + shift, -height / 2),
    (base / 2 + shift, -height / 2),
    (top / 2 + shift, height / 2),
    (-top / 2 + shift, height / 2),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(width)
)
