import cadquery as cq

length = 0.74999
width = 0.73843
height = 0.11078
fillet_r = 0.038

result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
    .edges("|Z")
    .fillet(fillet_r)
)
