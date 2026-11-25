import cadquery as cq

L1, W1, H1 = 0.416808, 0.033235, 0.75
L2, W2, H2 = 0.211685, 0.065736, 0.411987
pad = 0.0065309

# Larger rectangle in X-Y plane, extruded in Z
big = cq.Workplane("XY").box(L1, W1, H1, centered=(True, True, False))

# Smaller rectangle in Y-Z plane: build in X-Y then rotate 90 deg about Z
# After rotation: length L2 lies along Y, width W2 lies along X, height H2 along Z
small = (
    cq.Workplane("XY")
    .box(L2, W2, H2, centered=(True, True, False))
    .rotate((0, 0, 0), (0, 0, 1), 90)
)

# Connect at one edge of the larger rectangle (its +X face), offset by pad from base
small = small.translate((L1 / 2 + W2 / 2, 0, pad))

result = big.union(small)
