import cadquery as cq
import math

L = 0.75
W = 0.605769
base = 0.375
leg = 0.028846
ang = math.radians(45)
t = 0.018035
off = 0.02

# trapezium: base along +Y edge (y=W/2), centered at x=off
# base endpoints
bx1 = off - base/2
bx2 = off + base/2
# top edge is shorter; legs lean inward at 45 deg
dx = leg * math.cos(ang)
dy = leg * math.sin(ang)
tx1 = bx1 + dx
tx2 = bx2 - dx
ty = W/2 + dy

pts = [(bx1, W/2), (bx2, W/2), (tx2, ty), (tx1, ty)]

plate = cq.Workplane("XY").rect(L, W).extrude(t)
trap = cq.Workplane("XY").polyline(pts).close().extrude(t)

result = plate.union(trap)
