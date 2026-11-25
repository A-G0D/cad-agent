import cadquery as cq

L, W, H = 0.75, 0.28043, 0.02045
cl, cw = 0.318403, 0.157741
offset = 0.021963

# Cut-out center: centered along length, offset above width midpoint
cx = 0.0
cy = offset

result = (
    cq.Workplane("XY")
    .box(L, W, H)
    .faces(">Z").workplane()
    .center(cx, cy)
    .rect(cl, cw)
    .cutThruAll()
    .rotate((0, 0, 0), (1, 0, 0), -90)
    .translate((0, 0, 0))
)
