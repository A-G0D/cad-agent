import cadquery as cq
import math

d = 0.375
h = 0.691189
r = d / 2.0
top_len = 0.208765

# Cylinder: base at z=0, centered on Z axis
cyl = cq.Workplane("XY").circle(r).extrude(h)

# Cutting plane through three points:
#   A = (-r, 0, 0)             base, left side
#   B = (-r + top_len, 0, h)   top, shifted right by top_len
#   C = (r, 0, 0)              base, right side
# All three points have y = 0, so the plane is the XZ plane (y = 0).
# To remove ~1/3 of the material, tilt the cut so it starts at the base
# on one side and rises to the top with top_len along the top, then
# angles down to the opposite side at the base.

# Build a wedge cutter whose cross-section in XZ is the triangle
# A(-r,0), B(-r+top_len,h), C(r,0), extruded along Y to cover the cylinder.
# Remove the material on the +Y side of this slanted plane.

# Cross-section polygon in XZ (as points in XY workplane then rotate)
# We'll build the cutter as a solid using a polyline in the XZ plane,
# extruded along Y.

# Points of the cutting triangle in XZ:
# A = (-r, 0)
# B = (-r + top_len, h)
# C = (r, 0)
# Extend the triangle upward/outward to ensure full coverage.

# Build cutter in XZ plane: use Workplane("XZ") where local x -> global X, local y -> global Z
# Then extrude along -Y (or +Y) to make the wedge.

# Triangle points (local x, local y) = (global X, global Z)
pA = (-r, 0.0)
pB = (-r + top_len, h)
pC = (r, 0.0)

# Extend the triangle to a large region on the +Y side of the slanted line AB.
# The slanted line AB: from A to B. The region to remove is on the side of
# the line AB that contains +Y direction (i.e., the side away from the cylinder's -Y half).
# Actually we want to remove ~1/3, so cut with a plane that is tilted.

# Simpler robust approach: build a large box, then cut it with a half-space
# defined by the slanted plane, then subtract from cylinder.

# Plane through A, B, C: normal = AB x AC
ax, ay, az = -r, 0.0, 0.0
bx, by, bz = -r + top_len, 0.0, h
cx, cy, cz = r, 0.0, 0.0

abx, aby, abz = bx - ax, by - ay, bz - az
acx, acy, acz = cx - ax, cy - ay, cz - az

nx = aby * acz - abz * acy
ny = abz * acx - abx * acz
nz = abx * acy - aby * acx

nlen = math.sqrt(nx * nx + ny * ny + nz * nz)
nx, ny, nz = nx / nlen, ny / nlen, nz / nlen

# Ensure normal points toward +Y (side to remove)
if ny < 0:
    nx, ny, nz = -nx, -ny, -nz

# Build a large box on the +Y side of the plane and cut it away.
# Create a big box, then cut with a half-space approximated by a large prism.
# Simpler: create a large wedge solid using the plane and extrude outward.

# Make a large box covering the +Y region
big = 10.0
cutter = cq.Workplane("XY").box(big, big, big, centered=(True, True, True))
cutter = cutter.translate((0, big / 2.0, h / 2.0))

# Now cut the cutter with the half-space on the -Y side of the plane.
# Build a large prism representing the -Y half-space and subtract from cutter.
# Use a large box rotated to align with the plane.
# Alternative: construct the cutter directly as a prism from the plane.

# Build the cutting solid as an extruded polygon in the XZ plane, extruded along Y.
# The plane in XZ: line through A(-r,0) and B(-r+top_len,h), extended.
# The region to remove is above/right of this line (toward +Y side).
# Actually the plane is vertical in Y (normal has no Y component? check).
# ny = 0 since all points have y=0. So the plane is vertical (contains Y axis direction).
# The plane is defined by line in XZ extruded along Y.
# Remove material on one side of this vertical plane.

# Line in XZ through A(-r, 0) and B(-r
