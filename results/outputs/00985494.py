import cadquery as cq

bottom = 0.495408
top = 0.148743
height = 0.233091
width = 0.744939

half_bottom = bottom / 2.0
half_top = top / 2.0
half_h = height / 2.0

pts = [
    (-half_bottom, -half_h),
    (half_bottom, -half_h),
    (half_top, half_h),
    (-half_top, half_h),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(width / 2.0, both=True)
)
