import cadquery as cq

# box() length/width/height are full sizes; 0.75 * 0.06429 * 0.03929 = 0.001894855875
result = cq.Workplane("XY").box(0.75, 0.06429, 0.03929, centered=(True, True, True))
