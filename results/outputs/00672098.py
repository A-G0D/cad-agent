import cadquery as cq

L = 0.337772
W = 0.75
H = 0.021792
m = 0.01816

# Base rectangle
base = cq.Workplane("XY").rect(L, W).extrude(H)

# Inner cutout: margin m on left, right, and top (in Y), open at bottom (Y = -W/2)
inner_w = L - 2 * m
inner_h = W - m
# Center of inner rectangle: x=0, y = -W/2 + inner_h/2
inner_cy = -W / 2 + inner_h / 2

cut = (
    cq.Workplane("XY")
    .center(0, inner_cy)
    .rect(inner_w, inner_h)
    .extrude(H)
)

result = base.cut(cut)
