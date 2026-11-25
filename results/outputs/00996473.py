import cadquery as cq

L = 1.5
W = 0.40625
H = 0.023438
D = 0.046875
R = D / 2.0

side_pad = 0.048699
width_pad = 0.039062
left_pad = 0.242188
right_pad = 0.242228

# Rectangle centered in XY, extruded from z=0 to z=H
base = cq.Workplane("XY").rect(L, W).extrude(H)

# Hole 1: centered along width, near one end (x = -L/2 + left_pad)
h1_x = -L / 2.0 + left_pad
h1_y = 0.0

# Holes 2 and 3: near opposite end, symmetric about centerline
h2_x = L / 2.0 - right_pad
h3_x = L / 2.0 - right_pad
h2_y = W / 2.0 - width_pad
h3_y = -(W / 2.0 - width_pad)

# Build cylinders explicitly with exact radius and cut them
holes = (
    cq.Workplane("XY")
    .pushPoints([(h1_x, h1_y), (h2_x, h2_y), (h3_x, h3_y)])
    .circle(R)
    .extrude(H + 1.0)
    .translate((0, 0, -0.5))
)

result = base.cut(holes).translate((0, 0, H / 2.0))
