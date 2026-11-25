# Text -> verified CadQuery part. LLM writes {spec, code}; kernel executes; deterministic gate checks code vs spec; failures feed back.
# Races N candidates in parallel (no added latency); first that passes the gate wins.
import json, re, subprocess, time, http.client, ssl, threading, queue, sys, os
import fixes
HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("CAD_PY", sys.executable)  # interpreter that has cadquery
def _env(k, d=None):  # environment first, then an optional dotenv file named by CAD_ENV
    if os.environ.get(k): return os.environ[k]
    try:
        for l in open(os.environ.get("CAD_ENV", ".env")):
            if l.startswith(k + "="): return l.split("=", 1)[1].strip().strip("\"'")
    except OSError: pass
    return d
KEY, MODEL = _env("DEEPSEEK_API_KEY"), os.environ.get("CAD_MODEL") or _env("DEEPSEEK_MODEL", "deepseek-flash")
host, _, path = _env("DEEPSEEK_BASE_URL", "https://api.deepseek.com/anthropic").replace("https://", "").rstrip("/").partition("/")
SYS = """You are a CAD engineer. Output exactly two fenced blocks and nothing else:
```json
{"bbox":[X,Y,Z],"holes":{"<diameter_mm>":<count>},"volume":<mm3 or null>,"solids":1}
```
```python
import cadquery as cq
...
result = <Workplane>
```
Rules: millimetres, Z up. bbox = overall size in mm. holes = counts of cylindrical holes/bores/slots-with-round-ends excluded, by diameter (only through/blind round holes incl. pockets with round walls), {} if none. volume = exact analytic volume of the finished solid if you can compute it, else null.
CadQuery 2.x pitfalls: box() is centered; circle().extrude(h) starts at z=0; use .faces(">Z").workplane() before hole()/cboreHole(); rect(forConstruction=True).vertices() for corner patterns; fillet/chamfer need edge selectors like "|Z"; shell via .faces(">Z").shell(-t); cut with .cut(); build one valid single solid; no prints or file IO."""
_LOCAL = None
if not os.environ.get("CAD_NO_FIX2"): SYS += fixes.POLYGON_RULE + fixes.UNIT_RULE
def llm_local(msgs, temp=0.0):
    global _LOCAL
    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler
    if _LOCAL is None: _LOCAL = load(os.environ.get("CAD_LOCAL", "mlx-community/Qwen2.5-Coder-3B-Instruct-4bit"))
    m, tok = _LOCAL
    p = tok.apply_chat_template([{"role": "system", "content": SYS}] + msgs, add_generation_prompt=True, tokenize=False)
    out = generate(m, tok, prompt=p, max_tokens=900, sampler=make_sampler(temp=temp))
    return out, {"input_tokens": len(p) // 4, "output_tokens": len(out) // 4}
def llm_cli(msgs, model):
    # Claude Code CLI backend; multi-turn flattened into one prompt. shortcut: ~9s CLI startup per call, benchmark only.
    p = "\n\n".join(("User: " if m["role"] == "user" else "Assistant: ") + m["content"] for m in msgs)
    r = subprocess.run(["claude", "-p", "--model", model, "--tools", "", "--disable-slash-commands", "--no-session-persistence",
        "--system-prompt", SYS, "--output-format", "json", p], capture_output=True, text=True, timeout=120)
    d = json.loads(r.stdout); u = d.get("usage", {})
    return d["result"], {"input_tokens": u.get("input_tokens", 0), "output_tokens": u.get("output_tokens", 0), "cost": d.get("total_cost_usd")}
def llm(msgs, temp=0.0):
    if os.environ.get("CAD_LOCAL"): return llm_local(msgs, temp)
    if os.environ.get("CAD_CLI"): return llm_cli(msgs, os.environ["CAD_CLI"])
    c = http.client.HTTPSConnection(host, timeout=40, context=ssl.create_default_context())
    c.request("POST", f"/{path}/v1/messages", json.dumps({"model": MODEL, "max_tokens": 12000 if os.environ.get("CAD_THINK") else 1200, "system": SYS, "temperature": temp,
        "thinking": {"type": "enabled", "budget_tokens": 3000} if os.environ.get("CAD_THINK") else {"type": "disabled"}, "messages": msgs}),
        {"content-type": "application/json", "anthropic-version": "2023-06-01", "authorization": f"Bearer {KEY}", "x-api-key": KEY})
    r = c.getresponse(); d = json.loads(r.read())
    if r.status != 200: raise RuntimeError(f"HTTP {r.status} {str(d)[:200]}")
    return next(b["text"] for b in d["content"] if b["type"] == "text"), d["usage"]
def parse(t):
    j = re.search(r"```json\n(.*?)```", t, re.S); p = re.search(r"```python\n(.*?)```", t, re.S)
    if not p: raise ValueError("no python block")
    return (json.loads(j.group(1)) if j else {}), p.group(1)
class Worker:
    def __init__(s):
        s.p = subprocess.Popen([PY, f"{HERE}/kernel.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        s.p.stdout.readline(); s.lock = threading.Lock()
    def run(s, code, out=None, timeout=30):
        with s.lock:
            s.p.stdin.write(json.dumps({"code": code, "out": out}) + "\n"); s.p.stdin.flush()
            q = queue.Queue(); threading.Thread(target=lambda: q.put(s.p.stdout.readline()), daemon=True).start()
            try: return json.loads(q.get(timeout=timeout))
            except Exception: s.p.kill(); s.__init__(); return {"ok": False, "error": "kernel timeout/crash"}
def gate(spec, m):
    """Deterministic check of measured geometry vs the spec. Returns list of failures (empty = pass)."""
    if not m.get("ok"): return [m.get("error", "exec failed")]
    f = []
    if not m["valid"]: f.append("solid invalid")
    if m["solids"] != 1: f.append(f"{m['solids']} solids, need exactly 1")
    sb = spec.get("bbox")
    if sb and any(abs(a - b) > max(0.05, 0.002 * b) for a, b in zip(sorted(m["bbox"]), sorted(sb))):
        f.append(f"bbox measured {m['bbox']} but spec {sb}")
    sh = {str(float(k)): v for k, v in (spec.get("holes") or {}).items()}
    mh = {str(float(k)): v for k, v in m["holes"].items()}
    if sh != mh: f.append(f"holes measured {mh} but spec {sh} (diameter:count)")
    v = spec.get("volume")
    if v and abs(m["volume"] - v) > 0.02 * v: f.append(f"volume measured {m['volume']} but spec {v}")
    return f
def attempt(prompt, w, temp, tries=3):
    msgs = [{"role": "user", "content": prompt}]; usage = [0, 0]; ran = ""; nudged = False
    for i in range(tries):
        t, u = llm(msgs, temp); usage[0] += u["input_tokens"]; usage[1] += u["output_tokens"]
        try: spec, code = parse(t)
        except Exception as e: msgs += [{"role": "assistant", "content": t}, {"role": "user", "content": f"Format error: {e}. Resend both blocks."}]; continue
        m = w.run(code); fails = gate(spec, m)
        if m.get("ok"): ran = code  # last code that executed, kept as unverified fallback
        if not fails and not os.environ.get("CAD_NO_FIX3") and i < tries - 1 and (miss := fixes.missing_numbers(prompt, code)) and not nudged:
            nudged = True; msgs += [{"role": "assistant", "content": t}, {"role": "user", "content": f"Check: these prompt numbers appear nowhere in your code: {miss}. If a dimension was dropped, fix the code; if the code is right, resend it unchanged."}]; continue
        if not fails: return dict(ok=True, code=code, spec=spec, metrics=m, tries=i + 1, usage=usage)
        hint = (" Hint: " + fixes.hint(" ".join(fails))) if not os.environ.get("CAD_NO_FIX1") and fixes.hint(" ".join(fails)) else ""
        msgs += [{"role": "assistant", "content": t}, {"role": "user", "content": "Verification failed: " + "; ".join(fails) + hint + f". Measured: {json.dumps({k: m.get(k) for k in ('bbox','volume','holes','solids')})}. Fix the code (and spec if it was wrong) and resend both blocks."}]
    return dict(ok=False, ran=ran, code=code if 'code' in dir() else "", tries=tries, usage=usage, fails=fails if 'fails' in dir() else ["format"])
def design(prompt, workers, out=None):
    """Race len(workers) candidates (temp 0 + diverse); return first verified one."""
    t0 = time.perf_counter(); q = queue.Queue()
    for i, w in enumerate(workers):
        threading.Thread(target=lambda w=w, i=i: q.put(attempt(prompt, w, 0.0 if i == 0 else 0.8)), daemon=True).start()
    last = None
    for _ in workers:
        try: r = q.get(timeout=int(os.environ.get("CAD_TIMEOUT",90)))
        except queue.Empty: return dict(ok=False, code="", tries=0, usage=[0, 0], fails=["timeout"], seconds=90)
        last = r
        if r["ok"]:
            if out: workers[0].run(r["code"], out)
            r["seconds"] = round(time.perf_counter() - t0, 2); return r
    last["seconds"] = round(time.perf_counter() - t0, 2)
    if out and last.get("ran"): last["fallback"] = workers[0].run(last["ran"], out).get("ok", False)  # unverified: ok stays False
    return last
if __name__ == "__main__":
    ws = [Worker(), Worker()]; r = design(" ".join(sys.argv[1:]), ws, HERE + "/out_last")
    print(json.dumps({k: r[k] for k in r if k != "code"}, indent=1)); print(r["code"])
