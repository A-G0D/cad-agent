import cadquery as cq

L = 1.5
W = 0.413793
H = 0.031034

cut_l = (L - 1.28276) / 2
cut_w = W - 0.31034
r = 0.025

# Main plate
plate = cq.Workplane("XY").box(L, W, H)

# Build one rounded-corner cutout profile on top face, then mirror for symmetry
# Cutout rectangle with two rounded corners on the longer edge
cut = (
    cq.Workplane("XY")
    .rect(cut_l, cut_w)
    .extrude(H)
    .edges("|Z")
    .fillet(r)
)

# Position cutouts symmetrically along X, aligned to the long edges (centered in Y)
x_off = (L - cut_l) / 2
cut1 = cut.translate((x_off, 0, 0))
cut2 = cut.translate((-x_off, 0, 0))

result = plate.cut(cut1).cut(cut2)
