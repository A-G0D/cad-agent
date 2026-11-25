import cadquery as cq

L = 1.125
W = 1.5
H = 0.039474
D = 0.059211
inset_x = 0.108553
inset_y = 0.098684

# Build rectangle centered in XY, from z=0 to z=H
body = cq.Workplane("XY").rect(L, W).extrude(H)

# Hole positions: left side, inset from edges
x_left = -L/2 + inset_x
y_top = W/2 - inset_y
y_bot = -W/2 + inset_y

body = (
    body.faces(">Z").workplane()
    .pushPoints([(x_left, y_top), (x_left, y_bot)])
    .circle(D/2)
    .cutThruAll()
)

result = body
