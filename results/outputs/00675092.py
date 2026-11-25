import cadquery as cq

# Triangle vertices in XZ: (0,0), (0.75,0), (0,0.75) - right triangle, legs 0.75
# In XZ workplane, coordinates are (x, z). Extrude along Y by 0.03.
# To get exact volume 0.008, the triangle must have area = 0.008/0.03 = 0.26666...
# But a right triangle with legs 0.75 has area 0.28125 -> volume 0.0084375.
# The spec volume 0.008 is inconsistent with legs 0.75; measured volume is correct.
# Keep geometry as specified (legs 0.75) and report measured volume.

base = 0.75
height = 0.75
thickness = 0.03

result = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (base, 0), (0, height), (0, 0)])
    .close()
    .extrude(thickness)
    .translate((0, -thickness / 2, 0))
)
