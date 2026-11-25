import fixes

def test_hint_matches_known_errors():
    assert "smaller radius" in fixes.hint("Standard_Failure: BRep_API: command not done")
    assert "list" in fixes.hint("AttributeError: 'list' object has no attribute 'filter'")
    assert fixes.hint("something else") == "" and fixes.hint(None) == ""

def test_missing_numbers():
    p = "a plate 12.5 long, 0.036 wide, 4 holes"
    assert fixes.missing_numbers(p, "box(12.5, 36, 3)") == []       # 0.036 found as 36 (x1000)
    assert fixes.missing_numbers(p, "box(12.5, 3)") == [0.036]       # integer 4 ignored
    assert fixes.missing_numbers(p, "x = 12.5  # 0.036") == [0.036]  # comments do not count

def test_fixes_default_on():
    import agent
    assert fixes.POLYGON_RULE in agent.SYS and fixes.UNIT_RULE in agent.SYS
