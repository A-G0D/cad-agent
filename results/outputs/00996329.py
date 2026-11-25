import cadquery as cq

width = 0.333333
height = 0.083333
length = 0.666667

# L-shaped profile in XZ plane: horizontal leg along +X, thin in Z
# Extruded along Y by width
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(length, 0)
    .lineTo(length, height)
    .lineTo(height, height)
    .lineTo(height, height * 2)
    .lineTo(0, height * 2)
    .close()
)

result = profile.extrude(width)
