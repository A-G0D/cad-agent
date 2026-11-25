import cadquery as cq

L = 0.75
W = 0.75
H = 0.1875
t = 0.25  # arm thickness

# L-shape profile: two overlapping rectangles forming an L
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(L, 0)
    .lineTo(L, t)
    .lineTo(t, t)
    .lineTo(t, W)
    .lineTo(0, W)
    .close()
)

result = profile.extrude(H)
