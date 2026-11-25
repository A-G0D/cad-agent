import cadquery as cq

W = 0.399631
H = 0.091591
L = W * 2.0 / 3.0
HW = 0.188808
T = 0.133054

# Rectangle in XZ plane (width along X, height along Z), extruded along Y
rect = cq.Workplane("XZ").rect(W, H).extrude(T)

# Semi-hexagon attached to the longer (top) edge, starting at one end
# Hexagon with flat-to-flat = HW, so circumradius = HW/sqrt(3)
R = HW / (3 ** 0.5)
hexagon = (
    cq.Workplane("XZ")
    .center(-W / 2 + L / 2, H / 2)
    .polygon(6, 2 * R)
    .extrude(T)
)

result = rect.union(hexagon)
