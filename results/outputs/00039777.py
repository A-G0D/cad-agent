import cadquery as cq

L = 0.725228
H = 0.103604
y1 = L/4 + 0.0155
y2 = L/2
y3 = L - (L/4 + 0.0155)

pts = [
    (0, 0),
    (L, 0),
    (0.932436, y1),
    (1.05676, y2),
    (0.932436, y3),
    (L, L),
    (0, L),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(H)
)
