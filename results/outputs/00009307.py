import cadquery as cq

L = 1.5
W = 0.32143
T = 0.064286
legH = 0.47129
legL = 0.064286

top = cq.Workplane("XY").box(L, W, T).translate((0, 0, legH + T / 2))

leg_x = L / 2 - L / 3
leg = cq.Workplane("XY").box(legL, W, legH).translate((0, 0, legH / 2))
left = leg.translate((-leg_x, 0, 0))
right = leg.translate((leg_x, 0, 0))

result = top.union(left).union(right)
