import cadquery as cq

L = 0.448905  # x
W = 0.75      # y
H = 0.136861  # z

hole_l = 0.328467
hole_w = 0.229927
gap = 0.104015
fillet_r = 0.02

# outer block
block = cq.Workplane("XY").rect(L, W).extrude(H)

# two symmetric holes, rounded corners
offset = gap / 2 + hole_w / 2
hole_centers = [(0, offset), (0, -offset)]

cutters = []
for (cx, cy) in hole_centers:
    hp = (cq.Workplane("XY")
          .center(cx, cy)
          .rect(hole_l, hole_w)
          .extrude(H)
          .edges("|Z")
          .fillet(fillet_r))
    cutters.append(hp)

result = block
for c in cutters:
    result = result.cut(c)
