import cadquery as cq

L, W, H = 0.231564, 0.028954, 0.926255
hl, hw = 0.12897, 0.479215
gap = 0.005463

# plate centered in X/Y, from z=0 to H
plate = cq.Workplane("XY").rect(L, W).extrude(H)

# hole: width hl along X, height hw along Y; bottom edge at y = -W/2 + gap
cy = -W/2 + gap + hw/2
hole = (
    cq.Workplane("XY")
    .center(0, cy)
    .rect(hl, hw)
    .extrude(H)
)

result = plate.cut(hole).translate((-0.050509, -0.014477, 0.286873))
