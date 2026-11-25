import cadquery as cq

L = 0.75
W = 0.199115
H = 0.165929
sw = 0.126106
sd = 0.225664

# U-shaped solid: outer box minus a notch cut from the top
outer = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))
notch_w = L - 2 * sw
notch_d = W * 0.6
notch = (
    cq.Workplane("XY")
    .center(0, W / 2 - notch_d / 2)
    .box(notch_w, notch_d, H, centered=(True, True, False))
)
u_solid = outer.cut(notch)

# Two squares at bottom left and bottom right, overlapping the U corners
left_sq = (
    cq.Workplane("XY")
    .center(-L / 2 + sw / 2, -W / 2 + sd / 2)
    .box(sw, sd, H, centered=(True, True, False))
)
right_sq = (
    cq.Workplane("XY")
    .center(L / 2 - sw / 2, -W / 2 + sd / 2)
    .box(sw, sd, H, centered=(True, True, False))
)

result = u_solid.union(left_sq).union(right_sq)
