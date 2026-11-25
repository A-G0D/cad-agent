import cadquery as cq

R = 1.498046 / 2.0
H = 0.6
chan_len = 0.188827
chan_w = R
pad = 0.142454

# Main cylinder
body = cq.Workplane("XY").circle(R).extrude(H)

# Central through hole
body = body.faces(">Z").workplane().hole(0.748126)

# Rectangular channel cut into the outer edge.
# The channel lies along the X axis, its inner face at x = R - pad.
# To keep bbox in X at full diameter, cut only up to x = R (the rim),
# so the notch is a slot of depth = pad into the rim.
x_outer = R
x_inner = R - pad
slot_len = pad
rect = (
    cq.Workplane("XY")
    .center((x_inner + x_outer) / 2.0, 0)
    .rect(slot_len, chan_w)
    .extrude(H)
)
body = body.cut(rect)

result = body
