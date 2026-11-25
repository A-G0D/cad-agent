import cadquery as cq
import math

# Part 1: base rectangle (length X, width Y, height Z)
L1, W1, H1 = 1.40217, 0.062517, 0.75
base = cq.Workplane("XY").box(L1, W1, H1, centered=(True, True, False))

# Part 2: second rectangle on top, slightly narrower in width than first
L2, W2, H2 = 1.27174, 0.103421, 0.75
second = (
    cq.Workplane("XY")
    .workplane(offset=H1)
    .box(L2, W2, H2, centered=(True, True, False))
)

# Part 3: isosceles trapezoid on top, base width 1.33696 (X), extruded along Y by W2
Bw, H3, angle = 1.33696, 0.75, 72.0
inset = H3 / math.tan(math.radians(angle))
Tw = Bw - 2 * inset

# Build trapezoid in XZ plane: local x -> global X, local y -> global Z
pts = [
    (-Bw / 2, 0),
    (Bw / 2, 0),
    (Tw / 2, H3),
    (-Tw / 2, H3),
]
trap = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(W2)
    .translate((0, -W2 / 2, H1 + H2))
)

result = base.union(second).union(trap)
