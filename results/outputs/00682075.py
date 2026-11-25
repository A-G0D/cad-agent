import cadquery as cq

# Three-step pedestal: three connected rectangles forming a staircase profile.
# Step 1 (base): 0.75 x 0.5, height 0.25
# Step 2:        0.50 x 0.5, height 0.25
# Step 3 (top):  0.25 x 0.5, height 0.25
# Steps aligned on one side (x=0), centered in Y.

base = cq.Workplane("XY").box(0.75, 0.5, 0.25, centered=(False, True, False))
step2 = cq.Workplane("XY").box(0.50, 0.5, 0.25, centered=(False, True, False)).translate((0, 0, 0.25))
step3 = cq.Workplane("XY").box(0.25, 0.5, 0.25, centered=(False, True, False)).translate((0, 0, 0.50))

result = base.union(step2).union(step3)

# Translate to the requested final position
result = result.translate((0.375, -0.25, -0.020659))
