import cadquery as cq

L = 0.03547
W = 1.27689
H = 0.14188

hole_w = 0.5677508
hole_h = 0.094585
pad = 0.047292

# Plate
plate = cq.Workplane("XY").box(L, W, H)

# Two symmetric rectangular holes cut through the plate (through in X)
# Positioned along Y, separated by pad, not touching edges
# Total hole span along Y: 2*hole_w + pad
# Center them symmetrically about Y=0
y_center_offset = (hole_w + pad) / 2.0

hole1 = (
    cq.Workplane("YZ")
    .center(-y_center_offset, 0)
    .rect(hole_w, hole_h)
    .extrude(L * 2)
    .translate((-L, 0, 0))
)

hole2 = (
    cq.Workplane("YZ")
    .center(y_center_offset, 0)
    .rect(hole_w, hole_h)
    .extrude(L * 2)
    .translate((-L, 0, 0))
)

result = plate.cut(hole1).cut(hole2)

# Translate: centered in z, offset 0.111555 in y
result = result.translate((0, 0.111555, 0))
