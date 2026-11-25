import cadquery as cq

L = 0.982759
W = 0.124138
H = 0.827586
cut_len = 0.444828

sketch = (
    cq.Workplane("XY")
    .rect(L, W)
    .rect(cut_len, W)
    .vertices()
    .rect(cut_len, W)
)

result = (
    cq.Workplane("XY")
    .rect(L, W)
    .extrude(H)
    .translate((0, 0, 0.077586))
)
