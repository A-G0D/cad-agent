import cadquery as cq

L = 1.5
W = 0.52105
H = 0.15789
D = 1.701232
R = D / 2.0
offset = 0.067116

# Rectangular prism centered in XY, sitting on z=0
prism = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Semi-circle cutter: half-disc of radius R whose flat side lies on the long face
# (y = W/2) and which protrudes outward, so cutting it removes a semicircular
# notch from the long face. The offset positions the flat edge relative to the face.
cutter = (
    cq.Workplane("XY")
    .moveTo(-R, W / 2.0 + offset)
    .lineTo(R, W / 2.0 + offset)
    .threePointArc((0, W / 2.0 + offset + R), (-R, W / 2.0 + offset))
    .close()
    .extrude(H)
)

result = prism.cut(cutter)
