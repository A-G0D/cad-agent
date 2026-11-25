import cadquery as cq

length = 1.5
width = 1.37143
height = 0.078171
slot_len = 0.085714
slot_start = 0.685714

# Build plate centered at origin in XY, extruded up in Z
plate = cq.Workplane("XY").box(length, width, height)

# Slot: rectangle on front profile (XZ plane), cut through the width (Y)
# Slot spans full height, positioned along X starting at slot_start from left edge
# Left edge is at x = -length/2, so slot center x = -length/2 + slot_start + slot_len/2
slot_center_x = -length/2 + slot_start + slot_len/2

slot = (
    cq.Workplane("XZ")
    .center(slot_center_x, 0)
    .rect(slot_len, height)
    .extrude(width)
    .translate((0, -width/2, 0))
)

result = plate.cut(slot)
