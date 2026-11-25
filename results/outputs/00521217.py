import cadquery as cq

d1 = 0.059646
h1 = 0.750036
d2 = 0.029823
h2 = 3.75018

# Large cylinder: z from h2 to h2+h1
big = cq.Workplane("XY").workplane(offset=h2).circle(d1 / 2.0).extrude(h1)

# Small longer cylinder: z from 0 to h2, attached to the bottom of the big one
small = cq.Workplane("XY").circle(d2 / 2.0).extrude(h2)

result = big.union(small)
