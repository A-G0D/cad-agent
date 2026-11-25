import cadquery as cq

L = 0.636792
W = 0.56638
tab_L = L + 0.113207 * 2
tab_W = 0.141509
H = 0.099057
hole_d = 0.32

main = cq.Workplane("XY").rect(L, W).extrude(H)
tabs = cq.Workplane("XY").rect(tab_L, tab_W).extrude(H)
body = main.union(tabs)
result = (
    body.faces(">Z")
    .workplane()
    .hole(hole_d)
)
