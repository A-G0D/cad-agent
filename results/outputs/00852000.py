import cadquery as cq

L = 0.830095
H = 0.1703531
pocket = 0.676879
pocket_depth = 0.105467
center_d = 0.327945
center_h = 0.105467
corner_d = 0.25606
corner_h = 0.094448

# Base square
result = cq.Workplane("XY").rect(L, L).extrude(H)

# Hollow out inside from top (keep top rim)
result = (
    result.faces(">Z").workplane()
    .rect(pocket, pocket)
    .cutBlind(-pocket_depth)
)

# Center circle from bottom
center_hole = (
    cq.Workplane("XY")
    .circle(center_d / 2)
    .extrude(center_h)
)
result = result.cut(center_hole)

# Four corner circles on top
offset = (L - corner_d) / 2 - 0.02
corner_holes = (
    cq.Workplane("XY").workplane(offset=H)
    .rect(offset * 2, offset * 2, forConstruction=True).vertices()
    .circle(corner_d / 2)
    .extrude(-corner_h)
)
result = result.cut(corner_holes)
