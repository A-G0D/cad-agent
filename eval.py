# Independent ground truth (hand-computed bbox / hole counts / analytic volume). Does NOT use the agent's own spec.
import sys, json, math, time, concurrent.futures as cf
sys.path.insert(0, ".")
from agent import Worker, design
pi = math.pi
def box(a,b,c): return a*b*c
def cyl(d,h): return pi*(d/2)**2*h
CASES = [  # prompt, bbox, holes{dia:count}, volume
 ("a 40x20x10 mm plate with a 6 mm hole through the center, hole axis along the 10 mm thickness", [40,20,10], {6:1}, box(40,20,10)-cyl(6,10)),
 ("a 60x30x5 mm plate with four 4 mm through holes, 5 mm in from each edge at the corners", [60,30,5], {4:4}, box(60,30,5)-4*cyl(4,5)),
 ("a 100 mm cube", [100]*3, {}, 1e6),
 ("a 50x25x8 mm block with all four vertical edges filleted at 3 mm radius", [50,25,8], {}, 8*(50*25-(4-pi)*9)),
 ("a cylinder 30 mm diameter by 15 mm tall with a 10 mm through bore along its axis", [30,30,15], {10:1}, cyl(30,15)-cyl(10,15)),
 ("an 80x40x6 mm plate with two 5 mm through holes 60 mm apart, centered, in the 80 mm direction", [80,40,6], {5:2}, box(80,40,6)-2*cyl(5,6)),
 ("a 60 mm diameter disc 5 mm thick", [60,60,5], {}, cyl(60,5)),
 ("a 50 mm diameter sphere", [50]*3, {}, 4/3*pi*25**3),
 ("a 50 mm OD disc 4 mm thick with a 20 mm center hole", [50,50,4], {20:1}, cyl(50,4)-cyl(20,4)),
 ("a rectangular tube, 40 mm square outside, 2 mm walls, 20 mm long, open both ends", [40,40,20], {}, 20*(1600-36*36)),
 ("a 90x60x15 mm tray, 2 mm walls and 2 mm floor, open top", [90,60,15], {}, box(90,60,15)-86*56*13),
 ("a 120x80x10 mm plate with a 20 mm diameter round pocket 5 mm deep in the center of the top face", [120,80,10], {20:1}, box(120,80,10)-cyl(20,5)),
 ("a 70x30x10 mm block with a 2 mm 45 degree chamfer on the four edges of the top face", [70,30,10], {}, 0),
 ("a hex bolt: 8 mm diameter shaft 30 mm long under a hex head 13 mm across flats and 5 mm tall (head and shaft share an axis, bolt is one solid)", [15.011,13,35], {}, 5*(13**2*math.sqrt(3)/2)+cyl(8,30)),
 ("a flange: 80 mm diameter disc 8 mm thick with a 30 mm center bore and six 6 mm holes evenly spaced on a 60 mm bolt circle", [80,80,8], {30:1,6:6}, cyl(80,8)-cyl(30,8)-6*cyl(6,8)),
 ("a washer: 20 mm OD, 10 mm ID, 2 mm thick", [20,20,2], {10:1}, cyl(20,2)-cyl(10,2)),
 ("an L bracket made of two 4 mm thick plates: a 50 mm wide, 40 mm long base and a 50 mm wide, 30 mm tall vertical wall at one end of the base (outer height 30 mm total)", [50,40,30], {}, 50*(40*4+(30-4)*4)),
 ("a 100 mm long solid cylinder 20 mm diameter with a 2 mm x 45 degree chamfer ignored: just a plain 100 mm long, 20 mm diameter rod", [20,20,100], {}, cyl(20,100)),
 ("a 60x40x20 mm block with a 20 mm diameter hole 10 mm deep (blind) in the top face center", [60,40,20], {20:1}, box(60,40,20)-cyl(20,10)),
 ("a pipe: 50 mm OD, 4 mm wall, 200 mm long", [50,50,200], {42:1}, 200*pi*(25**2-21**2)),
 ("a cone frustum 40 mm bottom diameter, 20 mm top diameter, 30 mm tall", [40,40,30], {}, pi*30/3*(20**2+20*10+10**2)),
 ("a 100x20x20 mm bar with five 4 mm through holes equally spaced along its length, centered on the 20 mm width, axes along the 20 mm height", [100,20,20], {4:5}, box(100,20,20)-5*cyl(4,20)),
 ("a stepped shaft: 20 mm diameter 30 mm long, then 12 mm diameter 40 mm long, coaxial, one solid", [20,20,70], {}, cyl(20,30)+cyl(12,40)),
 ("a plate 100x60x4 mm with a 30x20 mm rectangular through window in the center", [100,60,4], {}, 4*(6000-600)),
 ("a 30 mm cube with a 10 mm radius sphere-shaped dimple removed centered on the top face (sphere center on the top face plane)", [30,30,30], {}, 27000-2/3*pi*1000),
 ("a counterbored plate 50x50x10 mm with one center through hole 6 mm diameter counterbored 10 mm diameter 4 mm deep from the top", [50,50,10], {6:1,10:1}, box(50,50,10)-cyl(6,6)-cyl(10,4)),
 ("a ring: torus-free ring 60 mm outer diameter 40 mm inner diameter 10 mm tall", [60,60,10], {40:1}, 10*pi*(900-400)),
 ("a 2x3 grid of 5 mm diameter through holes with 15 mm pitch in a 60x45x6 mm plate, grid centered", [60,45,6], {5:6}, box(60,45,6)-6*cyl(5,6)),
 ("a solid 25 mm cube unioned with a 25 mm diameter cylinder 25 mm tall standing on top of it, same axis through cube center", [25,25,50], {}, 25**3+cyl(25,25)),
]

CASES += [
 ("a gear-like disc: 60 mm diameter, 8 mm thick, with 12 rectangular teeth each 5 mm wide radially 4 mm tall added around the rim at 30 degree spacing, and a 10 mm center bore", [68,68,8], {10:1}, None),
 ("a bottle: revolve a profile into a 40 mm diameter cylindrical body 60 mm tall, solid, with a 16 mm diameter, 20 mm tall neck on top, coaxial", [40,40,80], {}, cyl(40,60)+cyl(16,20)),
 ("a 60x40x30 mm block, hollowed to a 3 mm wall box open at the top (shell), with four 5 mm diameter through holes in the floor at the corners 8 mm in from the edges", [60,40,30], {5:4}, box(60,40,30)-54*34*27-4*cyl(5,3)),
 ("an I-beam cross-section extruded 100 mm: 40 mm wide flanges 4 mm thick top and bottom, 32 mm tall web 4 mm thick between them, total height 40 mm", [40,40,100], {}, 100*(2*40*4+32*4)),
 ("a 50 mm diameter, 10 mm tall disc with 8 evenly spaced 4 mm through holes on a 36 mm diameter circle and no center hole", [50,50,10], {4:8}, cyl(50,10)-8*cyl(4,10)),
 ("a rectangular plate 80x50x5 mm with all four corners rounded at 8 mm radius and a 10 mm center hole", [80,50,5], {10:1}, 5*(80*50-(4-pi)*64)-cyl(10,5)),
 ("a T-slot nut block: 30x20x10 mm with a 6 mm diameter through hole centered on the 30x20 face", [30,20,10], {6:1}, box(30,20,10)-cyl(6,10)),
 ("a spool: two 40 mm diameter 3 mm thick end discs separated by a 20 mm diameter, 24 mm long core, all coaxial, with a 8 mm bore through the whole length", [40,40,30], {8:1}, 2*cyl(40,3)+cyl(20,24)-cyl(8,30)),
 ("an arch: 60 mm wide 40 mm tall 10 mm thick rectangular block with a semicircular cut 40 mm diameter whose flat side lies on the bottom edge, centered", [60,40,10], {40:1}, 10*(60*40-pi*400/2)),
 ("a pyramid with a 40x40 mm square base and 30 mm height (loft to a point is not needed; use a polygon extrude with taper or loft)", [40,40,30], {}, 40*40*30/3),
 ("a 4 mm thick plate 60x60 mm with a 50x50 mm square pocket 2 mm deep leaving a 5 mm rim", [60,60,4], {}, 60*60*4-50*50*2),
 ("a dumbbell: two 30 mm diameter spheres joined by a 10 mm diameter, 40 mm long cylinder between sphere centers, all on the X axis", [70,30,30], {}, None),
 ("a washer stack: three 20 mm OD 10 mm ID 2 mm thick washers stacked into one coaxial 6 mm tall solid", [20,20,6], {10:1}, 3*(cyl(20,2)-cyl(10,2))),
 ("a 100x40x3 mm sheet bent into a U channel: 40 mm base, two 20 mm tall sides, 3 mm thickness everywhere, 100 mm long (outer dimensions 40 wide x 20 tall)", [100,40,20], {}, 100*(40*3+2*17*3)),
 ("a bracket: 60x40x4 mm base plate with two 6 mm through holes on the centerline 40 mm apart, and a 4 mm thick 60 mm wide 30 mm tall wall rising from one 60 mm edge (wall outer height 30 from base bottom)", [60,40,30], {6:2}, 60*40*4+60*4*26-2*cyl(6,4)),
]
CASES = [c for c in CASES]
def score(m, bbox, holes, vol):
    if not m.get("ok"): return False, "exec"
    if any(abs(a-b) > max(0.05, 0.005*b) for a,b in zip(sorted(m["bbox"]), sorted(bbox))): return False, f"bbox {m['bbox']}"
    mh = {float(k): v for k, v in m["holes"].items()}
    if mh != {float(k): v for k, v in holes.items()}: return False, f"holes {mh}"
    if vol and abs(m["volume"]-vol) > 0.01*vol: return False, f"vol {m['volume']} vs {round(vol,1)}"
    return True, ""
if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    pool = [Worker() for _ in range(N)]; ver = Worker(); rows = []
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    for i, (p, bb, h, v) in list(enumerate(CASES))[lo:]:
        r = design(p, pool, f"out/c{i:02d}")
        m = ver.run(r["code"]) if r.get("code") else {"ok": False}
        ok, why = score(m, bb, h, v); rows.append((ok, r["seconds"], r["tries"], sum(r["usage"])))
        print(f"{'PASS' if ok else 'FAIL'} {r['seconds']:5.1f}s tries={r['tries']} gate={r['ok']} {why} | {p[:60]}", flush=True)
    n = len(rows); ts = sorted(r[1] for r in rows)
    print(f"\npass {sum(r[0] for r in rows)}/{n}  median {ts[n//2]}s  p90 {ts[int(n*.9)-1]}s  tokens {sum(r[3] for r in rows)}")
