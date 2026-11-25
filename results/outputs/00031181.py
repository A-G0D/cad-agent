import cadquery as cq

L = 611.35
W = 360.26
H = 338.43

result = cq.Workplane("XY").box(L, W, H)
