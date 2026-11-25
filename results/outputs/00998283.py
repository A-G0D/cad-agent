import cadquery as cq

base = 0.3
top = 0.225
height = 0.1875
length = 0.75

pts = [
    (-base / 2, 0),
    (base / 2, 0),
    (top / 2, height),
    (-top / 2, height),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(length)
    .translate((0, -length / 2, 0))
)
