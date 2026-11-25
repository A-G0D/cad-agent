import cadquery as cq

L = 1.5
W = 0.004152
H = 0.720946
r = 0.077855

# The requested radius exceeds half the width; clamp to a safe value
r = min(r, W / 2.0 * 0.99)

result = (
    cq.Workplane("XY")
    .box(L, W, H, centered=(True, True, False))
    .edges("|X")
    .fillet(r)
)
