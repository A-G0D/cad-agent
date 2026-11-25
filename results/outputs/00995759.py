import cadquery as cq

length = 0.75
width = 0.5
height = 0.375
diameter = 0.5357
radius = diameter / 2.0

# Base rectangular block
base = cq.Workplane("XY").box(length, width, height, centered=(False, False, False))

# Semi-circular cutout on the longer side (front face at y=0), flat edge aligned with surface
# Sketch on XZ plane at y=0, cut inward along +Y
semi = (
    cq.Workplane("XZ")
    .center(length / 2.0, height / 2.0)
    .moveTo(-radius, 0)
    .threePointArc((0, radius), (radius, 0))
    .close()
    .extrude(width)
)

result = base.cut(semi)
