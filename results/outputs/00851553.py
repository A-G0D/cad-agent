import cadquery as cq

L = 1.05974
W = 0.362338
H = 0.362338

inner_L = 0.954546
inner_W = 0.261039
inner_depth = 0.314632

leg_L = 0.041039
leg_W = 0.136796
leg_H = 0.314632

rod_d = 0.108522

# Top hollow box
top = (
    cq.Workplane("XY")
    .rect(L, W)
    .extrude(H)
    .faces(">Z")
    .workplane()
    .rect(inner_L, inner_W)
    .cutBlind(-inner_depth)
)

# Legs: two legs on left and right, centered in Y, attached to bottom of top
leg_x = L / 2 - leg_L / 2
legs = (
    cq.Workplane("XY")
    .pushPoints([(-leg_x, 0), (leg_x, 0)])
    .rect(leg_L, leg_W)
    .extrude(-leg_H)
)

# Rod connecting legs near bottom
rod_z = -leg_H + rod_d / 2 + 0.02
rod_len = 2 * leg_x
rod = (
    cq.Workplane("YZ")
    .workplane(offset=-rod_len / 2)
    .center(0, rod_z)
    .circle(rod_d / 2)
    .extrude(rod_len)
)

result = top.union(legs).union(rod)
