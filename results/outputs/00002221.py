import cadquery as cq

L = 0.0625
W = 0.75
H = 0.0034

# Floor plate: length L along X, width W along Y, thickness H along Z
floor = cq.Workplane("XY").box(L, W, H, centered=(False, False, False))

# Wall plate: perpendicular, standing up along Z, sharing the elongated edge
# Length L along X, height W along Z, thickness H along Y
wall = cq.Workplane("XY").box(L, H, W, centered=(False, False, False))

result = floor.union(wall).clean()
