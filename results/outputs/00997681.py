import cadquery as cq

length = 0.058594
width = 0.75
height = 0.216797
fillet_radius = height - 0.1875

# Build the 2D profile with two rounded corners on one long edge,
# then extrude. Fillet radius is small relative to the width.
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
    .edges("|Z")
    .fillet(fillet_radius)
)
