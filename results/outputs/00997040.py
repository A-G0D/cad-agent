import cadquery as cq

# Side profile in XZ plane, extruded along Y
# Thin rectangle: length 0.75 (X), height 0.0018 (Z)
# First square: side 0.021, bottom-right at top-right of rectangle
# Second square: side 0.0192, bottom-right at top-right of first square
# Extrude depth = 20 * 0.042 = 0.84

w = 0.042
rect_len = 0.75
rect_h = 0.0018
sq1 = 0.021
sq2 = 0.0192
depth = 20.0 * w

pts = [
    (0.0, 0.0),
    (rect_len, 0.0),
    (rect_len, rect_h),
    (rect_len, rect_h + sq1),
    (rect_len, rect_h + sq1 + sq2),
    (rect_len - sq2, rect_h + sq1 + sq2),
    (rect_len - sq2, rect_h + sq1),
    (rect_len - sq1, rect_h + sq1),
    (rect_len - sq1, rect_h),
    (0.0, rect_h),
]

profile = cq.Workplane("XZ").polyline(pts).close()
result = profile.extrude(depth)
