import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cadquery as cq
from agent import gate
from kernel import metrics, run

M = {"ok": True, "valid": True, "solids": 1, "volume": 1000.0, "bbox": [10, 10, 10], "holes": {"4.0": 1}}

def test_gate_pass():
    assert gate({"bbox": [10, 10, 10], "holes": {"4": 1}, "volume": 1010}, M) == []

def test_gate_bbox_hole_volume_fail():
    f = gate({"bbox": [10, 10, 12], "holes": {"4": 2}, "volume": 1200}, M)
    assert len(f) == 3

def test_gate_exec_error():
    assert gate({}, {"ok": False, "error": "boom"}) == ["boom"]

def test_metrics_box_with_hole():
    r = cq.Workplane("XY").box(20, 20, 10).faces(">Z").workplane().hole(6)
    m, _ = metrics(r)
    assert m["holes"] == {"6.0": 1} and m["solids"] == 1 and m["valid"]
    assert m["bbox"] == [20, 20, 10] and abs(m["volume"] - (4000 - 3.14159265 * 9 * 10)) < 0.1

def test_solid_cylinder_is_not_a_hole():
    assert run("import cadquery as cq\nresult = cq.Workplane('XY').circle(5).extrude(10)")["holes"] == {}

def test_gate_roundtrip_with_kernel():
    m = run("import cadquery as cq\nresult = cq.Workplane('XY').box(10,10,10)")
    assert gate({"bbox": [10, 10, 10], "holes": {}, "volume": 1000}, m) == []
