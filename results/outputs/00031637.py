import cadquery as cq

L = 1.05964
W = 0.56859
H = 0.26362
cl = L / 4.0
ch = H * 3.0 / 4.0

base = cq.Workplane("XY").box(L, W, H, centered=False)
cut = (
    cq.Workplane("XY")
    .box(cl, W, ch, centered=False)
    .translate((L - cl, -W / 2.0 + W / 2.0, H - ch))
)
result = base.cut(cut)

vol = L * W * H - cl * W * ch
