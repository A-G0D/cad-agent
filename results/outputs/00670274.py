import cadquery as cq

L = 0.333015
W = 0.908225
H = 0.006055
c = 0.090822

result = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .rect(L - c, W - c, forConstruction=True)
    .vertices()
    .rect(c, c)
    .cutThruAll()
)
