import cadquery as cq

base = cq.Workplane("XZ").rect(0.307377, 0.307377).extrude(0.012295)
pillar = cq.Workplane("XZ").rect(0.307377, 0.184426).extrude(0.737705)
result = base.union(pillar)
