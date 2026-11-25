import cadquery as cq

# Cylinder with diameter 1.27949 (radius 0.639745), height equal to diameter
d = 1.27949
h = 1.27949

# Empty rectangle in the center: length 0.787604 (X), width 0.506095 (Y)
# Interpreted as an internal void (pocket) cut through the center of the cylinder.
rect_len = 0.787604
rect_wid = 0.506095

# Build cylinder
cyl = cq.Workplane("XY").circle(d / 2.0).extrude(h)

# Cut an empty rectangular pocket centered in the cylinder, through full height
result = (
    cyl.faces(">Z").workplane(origin=(0, 0, 0))
    .rect(rect_len, rect_wid)
    .cutThruAll()
)
