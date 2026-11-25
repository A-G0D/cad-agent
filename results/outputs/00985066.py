import cadquery as cq

# Dimensions (meters, used as given)
col_len = 0.05
col_wid = 0.35
horiz_len = 1.175
horiz_wid = 0.35
col_h = 0.725
horiz_h = 0.025

# Base horizontal slab
base = cq.Workplane("XY").box(horiz_len, horiz_wid, horiz_h)

# Two upright columns at the ends, rising from the base
col = cq.Workplane("XY").box(col_len, col_wid, col_h)
left = col.translate((-(horiz_len - col_len) / 2, 0, horiz_h / 2 + col_h / 2))
right = col.translate(((horiz_len - col_len) / 2, 0, horiz_h / 2 + col_h / 2))

result = base.union(left).union(right)
