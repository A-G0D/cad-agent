import cadquery as cq

# Main square profile
square = cq.Workplane("XY").rect(1.1056, 1.22951).extrude(0.122951)

# Side rectangles (length along X = 1.76342, width along Y = 0.368852)
# Centered on horizontal centerline, on left and right edges
side_rect = cq.Workplane("XY").rect(1.76342, 0.368852).extrude(0.122951)

# Union the solids
result = square.union(side_rect)
