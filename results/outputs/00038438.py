import cadquery as cq

length = 0.375
width = 0.11438
height = 0.75

# Rhombus with diagonals = length and width
pts = [
    (0, width / 2),
    (length / 2, 0),
    (0, -width / 2),
    (-length / 2, 0),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)

# Analytic volume: (d1*d2/2)*h
volume = (length * width / 2) * height
