import cadquery as cq

L = 1.20302
W = 0.55872
T = 0.020134
leg = 0.060403
H = 0.75

top = cq.Workplane("XY").box(L, W, T).translate((0, 0, H + T / 2))

legs = (
    cq.Workplane("XY")
    .rect(L - leg, W - leg, forConstruction=True)
    .vertices()
    .rect(leg, leg)
    .extrude(H)
)

result = top.union(legs)
