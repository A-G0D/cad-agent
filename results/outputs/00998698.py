import cadquery as cq

# Base rectangle dimensions
L = 0.5
W = 0.433013
H = 0.125

# Build the octagonal slab: rectangle with right-angle triangles cut at each corner.
# Construct the octagon as a polygon by clipping corners.
c = 0.1  # corner cut size (small relative to rectangle)

# Octagon vertices (ordered counter-clockwise) after cutting triangles of leg c from each corner
pts = [
    (-L/2 + c, -W/2),
    ( L/2 - c, -W/2),
    ( L/2,     -W/2 + c),
    ( L/2,      W/2 - c),
    ( L/2 - c,  W/2),
    (-L/2 + c,  W/2),
    (-L/2,      W/2 - c),
    (-L/2,     -W/2 + c),
]

slab = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(H)
)

# Hexagonal columns protruding from the top surface
# Hexagon "diameter" 0.5 -> circumradius 0.25
hex_d = 0.5
hex_r = hex_d / 2.0

# Place two hexagons symmetrically on opposite ends (along X), aligned with each end.
# Center them at x = ±(L/2 - hex_r) so they sit at the ends but fully on the slab.
xoff = L/2 - hex_r
col_h = 0.75

def hex_column(xc):
    return (
        cq.Workplane("XY")
        .workplane(offset=H)
        .center(xc, 0)
        .polygon(6, hex_d)
        .extrude(col_h)
    )

col1 = hex_column(-xoff)
col2 = hex_column( xoff)

result = slab.union(col1).union(col2)
