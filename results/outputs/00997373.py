import cadquery as cq

L = 1.5
W = 0.016304
H = 1.22283
D = 0.130435
spacing = 0.195652
x0 = 0.433378

# Build rectangle centered in X and Y, from z=0 to z=H
result = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
)

# Hole centers along X: first at x0 from left edge -> x = -L/2 + x0
x_first = -L / 2 + x0
xs = [x_first, x_first + spacing, x_first + 2 * spacing]

# Cut holes as a single union of cylinders to keep one solid
holes = (
    cq.Workplane("XY")
    .pushPoints([(x, 0) for x in xs])
    .circle(D / 2)
    .extrude(H)
)

result = result.cut(holes).clean()
