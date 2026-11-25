import cadquery as cq

# Dimensions
col_w = 0.416667      # width of each upright column (leg)
horiz_w = 0.083333    # thickness of horizontal top plate
height = 0.475
hole_d = 0.1375

# Overall footprint
total_x = 1.0
total_y = 0.583333

# Horizontal top plate at bottom: thickness horiz_w in Z
top = cq.Workplane("XY").box(total_x, total_y, horiz_w, centered=(True, True, False))

# Two upright columns (legs) rising from the plate
leg_h = height - horiz_w
leg_x_offset = (total_x - col_w) / 2
leg1 = cq.Workplane("XY").box(col_w, total_y, leg_h, centered=(True, True, False)).translate((-leg_x_offset, 0, horiz_w))
leg2 = cq.Workplane("XY").box(col_w, total_y, leg_h, centered=(True, True, False)).translate((leg_x_offset, 0, horiz_w))

result = top.union(leg1).union(leg2)

# Hole at center of horizontal (top) surface, through the plate
result = result.faces("<Z").workplane().hole(hole_d)

result = result.clean()
