import cadquery as cq

L = 0.676776
W = 0.20312
x0 = -0.349931

# Profile in XY plane (X = length, Y = height), then extrude in Z by W
pts = [
    (0.0, 0.0),
    (0.059507, 0.059507),
    (0.102138, 0.0),
    (0.135891, 0.135891),
    (0.05773, 0.05773),
    (0.089704, 0.089704),
    (L, 0.0),
]

profile = cq.Workplane("XY").polyline(pts).close().extrude(W)
profile = profile.translate((x0, 0.0, 0.0))
result = profile
