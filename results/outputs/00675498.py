import cadquery as cq

rect_w = 0.75
rect_h = 0.664347
trap_h = 0.374227
trap_base_long = 0.562673
trap_base_short = 0.280836
depth = 0.664347

pts = [
    (-rect_w/2, 0),
    (rect_w/2, 0),
    (rect_w/2, rect_h),
    (trap_base_long/2, rect_h),
    (trap_base_short/2, rect_h + trap_h),
    (-trap_base_short/2, rect_h + trap_h),
    (-trap_base_long/2, rect_h),
    (-rect_w/2, rect_h),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(depth)
)
