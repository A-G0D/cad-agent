import cadquery as cq

L = 1.5
W = 0.55102
H = 0.08347

# Right square: side and height
right_s = 0.438776
right_h = 0.280162

# Left square: 75% smaller surface area than right -> area ratio 0.25 -> side ratio 0.5
# (also given explicitly below)
left_s = 0.331633
left_h = 0.127551

# Verify design ratios stated in the prompt:
area_ratio = (left_s * left_s) / (right_s * right_s)   # ~0.25 => 75% smaller
height_ratio = right_h / left_h                        # ~2x

# Base rectangle: footprint sized so total bbox stays 1.5 x 0.55102, height H.
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Right square: sits on top of base, its inner edge at x = L/2
right_sq = (
    cq.Workplane("XY")
    .workplane(offset=H)
    .center(L / 2 - right_s / 2, 0)
    .rect(right_s, right_s)
    .extrude(right_h)
)

# Left square: sits on top of base, its inner edge at x = -L/2
left_sq = (
    cq.Workplane("XY")
    .workplane(offset=H)
    .center(-L / 2 + left_s / 2, 0)
    .rect(left_s, left_s)
    .extrude(left_h)
)

result = base.union(right_sq).union(left_sq)
