import cadquery as cq

L = 0.043025
W = 0.985934
H = 1.39258

top_edge = min(H - 1.19693, L)
cut_width = (W - 0.563939) / 2.0

# Build irregular hexagon in XY plane, then extrude along Z
# Rectangle centered at origin: x in [-L/2, L/2], y in [-W/2, W/2]
# Cut top two corners: top edge length = top_edge, cut width from sides = cut_width
inset = (L - top_edge) / 2.0
pts = [
    (-L/2, -W/2),
    ( L/2, -W/2),
    ( L/2,  W/2 - cut_width),
    ( L/2 - inset, W/2),
    (-L/2 + inset, W/2),
    (-L/2,  W/2 - cut_width),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(H)
)
