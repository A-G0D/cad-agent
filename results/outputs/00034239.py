import cadquery as cq

L, W, H = 1.5, 1.2, 0.15
D_big = 0.675
D_small = 0.1968
edge_gap = 0.033

result = cq.Workplane("XY").box(L, W, H)

result = result.faces(">Z").workplane().hole(D_big)

x_small = L/2 - edge_gap - D_small/2
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-x_small, 0), (x_small, 0)])
    .hole(D_small)
)
