import cadquery as cq

L = 0.668421
W = 0.334211
H = 0.668421
d = 0.2625
r = d / 2.0

# Build the solid first, then cut the corner circle through it
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(L, 0)
    .lineTo(L, W)
    .lineTo(0, W)
    .close()
    .extrude(H)
    .faces(">Z")
    .workplane()
    .moveTo(L, W)
    .circle(r)
    .cutThruAll()
)
