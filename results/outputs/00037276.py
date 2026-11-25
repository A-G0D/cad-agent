import cadquery as cq
import math

D_large = 0.485133
D_small = 0.157385
total_length = 0.993343
width = 0.243343

R = D_large / 2.0
r = D_small / 2.0

# Distance between centers so total length (outer tangent length around both) matches
d = total_length - (R + r)

# External tangent line geometry for two circles
# angle of tangent line relative to center line
alpha = math.asin((R - r) / d)

# Points on large circle (left, center at origin) and small circle (right, center at (d,0))
# Tangent points: upper and lower
# For upper tangent, tangent point on large circle at angle (90 + alpha) from x-axis? Derive:
# Tangent line makes angle alpha with center line (x-axis). Normal to tangent points toward tangent line.
# Upper tangent on large circle: angle = pi/2 + alpha
# Upper tangent on small circle: angle = pi/2 + alpha
theta = math.pi / 2 + alpha

p1 = (R * math.cos(theta), R * math.sin(theta))          # large circle upper
p2 = (d + r * math.cos(theta), r * math.sin(theta))      # small circle upper

# Lower tangent points (mirror)
p3 = (R * math.cos(-theta), R * math.sin(-theta))
p4 = (d + r * math.cos(-theta), r * math.sin(-theta))

# Build shape: start at p1, arc around large circle through left side to p3, line to p4, arc around small circle through right to p2, line back to p1
# Use Workplane with moveTo/lineTo/threePointArc
# Large circle leftmost point at (-R, 0)
# Small circle rightmost point at (d + r, 0)

left_pt = (-R, 0.0)
right_pt = (d + r, 0.0)

wp = cq.Workplane("XY")
shape = (
    wp.moveTo(p1[0], p1[1])
    .threePointArc(left_pt, p3)
    .lineTo(p4[0], p4[1])
    .threePointArc(right_pt, p2)
    .close()
    .extrude(width)
)

result = shape
