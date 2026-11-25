import cadquery as cq

L = 1.5
W = 0.75
base_t = 0.034954
col_l = 0.35911
col_w = 0.581568
col_h = 0.699153
margin = 0.055864

# Base plate: top at z=0, bottom at z=-base_t
base = cq.Workplane("XY").box(L, W, base_t, centered=(True, True, False)).translate((0, 0, -base_t))

# Columns protrude upward from the top surface of the base
col_x = L/2 - margin - col_l/2
col1 = cq.Workplane("XY").box(col_l, col_w, col_h, centered=(True, True, False)).translate((col_x, 0, 0))
col2 = cq.Workplane("XY").box(col_l, col_w, col_h, centered=(True, True, False)).translate((-col_x, 0, 0))

result = base.union(col1).union(col2)
