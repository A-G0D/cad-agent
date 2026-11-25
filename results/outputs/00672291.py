import cadquery as cq

# Main body: length 0.75 (X), width 0.015 (Y), height 0.3 (Z)
# Top extension: width 0.15 (Y), height equal to main body width = 0.015 (Z)
# L-shaped profile in the YZ plane, extruded along X by 0.75

L = 0.75
w_main = 0.015
h_main = 0.3
w_ext = 0.15
h_ext = w_main  # 0.015

# Build L profile in YZ plane (sketch on YZ workplane), extrude along X
# Profile points (y, z): base rectangle main body + extension on top
pts = [
    (0.0, 0.0),
    (w_ext, 0.0),
    (w_ext, h_ext),
    (w_main, h_ext),
    (w_main, h_main),
    (0.0, h_main),
]

profile = cq.Workplane("YZ").polyline(pts).close()
result = profile.extrude(L)
