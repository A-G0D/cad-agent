import cadquery as cq

L = 60.0
W = 60.0
H = 750.0
t = 4.5

result = (
    cq.Workplane("XY")
    .rect(L, W)
    .extrude(H)
    .faces(">Z")
    .workplane()
    .rect(L - 2 * t, W - 2 * t)
    .cutThruAll()
)
