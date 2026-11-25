import cadquery as cq

L = 1.48234
W = 0.413495
H = 0.039009

# Right cutout
r_len = 0.147465
r_wid = 0.183609
r_from_right = 0.115044

# Left cutout
l_len = 0.320737
l_wid = 0.187173
l_from_left = 0.101171

# Base rectangle centered at origin in XY, extruded from z=0 to H
base = cq.Workplane("XY").rect(L, W).extrude(H)

# Right cutout: positioned r_from_right from right edge, centered in Y
r_cx = L/2 - r_from_right - r_len/2
right_cut = (
    cq.Workplane("XY")
    .center(r_cx, 0)
    .rect(r_len, r_wid)
    .extrude(H)
)

# Left cutout: positioned l_from_left from left edge, centered in Y
l_cx = -L/2 + l_from_left + l_len/2
left_cut = (
    cq.Workplane("XY")
    .center(l_cx, 0)
    .rect(l_len, l_wid)
    .extrude(H)
)

result = base.cut(right_cut).cut(left_cut)

# Adjust in X and center vertically
result = result.translate((0.008832, 0, H/2))
