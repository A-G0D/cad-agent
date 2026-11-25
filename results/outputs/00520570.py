import cadquery as cq

base_w = 0.767871
top_w = 1.04978
height = 0.576632
length = 0.012814

# Build trapezoid profile in XZ plane (X = width, Z = height), extrude along Y
pts = [
    (-base_w / 2, 0),
    (base_w / 2, 0),
    (top_w / 2, height),
    (-top_w / 2, height),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(length)
    .translate((0, -length / 2, 0))
)
