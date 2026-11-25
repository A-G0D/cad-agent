import cadquery as cq

Lx = 0.9375
Ly = 1.5
H = 0.375
arm_w = 0.234375
L_h = 0.328125

# Base block centered at origin in XY, sitting z in [-H/2, H/2]
base = cq.Workplane("XY").box(Lx, Ly, H)

# L footprint drawn directly in XY using a polyline, then extruded up from z=H/2
pts = [
    (-Lx/2, -Ly/2),
    (-Lx/2 + arm_w, -Ly/2),
    (-Lx/2 + arm_w, Ly/2 - arm_w),
    (Lx/2, Ly/2 - arm_w),
    (Lx/2, Ly/2),
    (-Lx/2, Ly/2),
]
Lblock = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(L_h)
    .translate((0, 0, H/2))
)

result = base.union(Lblock)
result = result.translate((0, 0, -H/2))
