"""Improvements on by default; opt out with CAD_NO_FIX1/2/3 (see agent.py). Pure functions so they can be unit-tested without an API."""
import re

POLYGON_RULE = ("\nBenchmark convention: for a regular polygon (hexagon, octagon, triangle...) whose prompt gives one size number "
    "(side length / length), pass that number unchanged as the second argument of polygon(n, size); do not convert side to circumradius.")

UNIT_RULE = "\nUnits: use the numbers in the prompt as given (units, meters or mm alike); do not multiply or divide them by 1000."

_HINTS = [  # (substring of the error, advice); first match wins
    ("BRep_API: command not done", "A fillet/chamfer/shell/boolean failed in OCCT. Use a smaller radius (under half the thinnest wall), fillet before cutting holes, select fewer edges, or drop that feature."),
    ("Cannot find a solid on the stack", "The call needs a solid in the workplane chain. Build the solid first (extrude/box), then select faces or edges from it; do not call it right after a 2D sketch or on a list."),
    ("must have at least one solid", "`result` must be a Workplane holding a solid. Extrude/revolve the sketch, or union the parts, and assign that to `result`."),
    ("object has no attribute 'filter'", "A Python list was used like a Workplane. Use Workplane methods (.faces(), .edges(), .vals()) or union the Workplane objects, not lists of solids."),
    ("no `result` variable", "End the program with `result = <Workplane>`."),
    ("kernel timeout", "The program was too slow or hung. Avoid loops over many booleans and huge arrays; keep it to a few operations."),
]
def hint(err):
    return next((h for k, h in _HINTS if k in (err or "")), "")

_NUM = re.compile(r"(?<![\w.])\d+\.?\d*(?:[eE][-+]?\d+)?")
def _nums(s): return {float(x) for x in _NUM.findall(s)}
def missing_numbers(prompt, code, scales=(1, 1000, 0.001)):
    """Prompt numbers (non-integer, or integer > 10) that appear in no form (x1, x1000, /1000) among the program's numeric literals.
    shortcut: derived values (a sum, 1/4 of a length) and counts are false positives; used only as one retry nudge."""
    lit = _nums(re.sub(r"#.*", "", code)); out = []
    for n in sorted(_nums(prompt)):
        if n == 0 or (n == int(n) and n <= 10): continue
        if not any(abs(n * s - l) <= 1e-6 * max(1, abs(l)) for s in scales for l in lit): out.append(n)
    return out
