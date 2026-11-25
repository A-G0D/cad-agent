import cadquery as cq

L = 1.09115
W = 1.5
H = 0.361568
D = 0.427203
CH = 0.271176

block = cq.Workplane("XY").box(L, W, H)
cyl = (
    cq.Workplane("XY")
    .workplane(offset=H / 2)
    .circle(D / 2)
    .extrude(CH)
)
result = block.union(cyl)
