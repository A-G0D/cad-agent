import cadquery as cq

L = 0.00875
W = 0.74801
H = 0.03125

cut_w = 0.1625
cut_h = 0.0125
cut_x = 0.01875

base = cq.Workplane("XY").box(L, W, H)

cut = (
    cq.Workplane("XY")
    .box(L * 2, cut_w, cut_h)
    .translate((0, -W / 2 + cut_x + cut_w / 2, -H / 2 + cut_h / 2))
)

result = base.cut(cut)
