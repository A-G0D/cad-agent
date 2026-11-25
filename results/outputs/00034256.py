import cadquery as cq

# Dimensions
base_len = 0.75
u_width = 0.3
wall_thick = 0.15          # derived to fill the U shape
cap_width = u_width + 0.45  # 0.75
base_h = 0.15
total_h = 0.45

# U-shaped body: base plate plus two vertical uprights
base = cq.Workplane("XY").box(base_len, u_width, base_h, centered=(False, True, False))

left_wall = (
    cq.Workplane("XY")
    .box(wall_thick, u_width, total_h, centered=(False, True, False))
)
right_wall = (
    cq.Workplane("XY")
    .box(wall_thick, u_width, total_h, centered=(False, True, False))
    .translate((base_len - wall_thick, 0, 0))
)

u_body = base.union(left_wall).union(right_wall)

# Cap rectangle closing the open top, wider than the U width
cap = (
    cq.Workplane("XY")
    .box(base_len, cap_width, wall_thick, centered=(False, True, False))
    .translate((0, 0, total_h - wall_thick))
)

result = u_body.union(cap)
