import cadquery as cq

L = 0.02812
H = 0.75

result = cq.Workplane("XY").rect(L, L).extrude(H)
