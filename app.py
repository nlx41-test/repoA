import os
import subprocess
import time

try:
    from flask import Flask, request, render_template_string, jsonify
except ImportError:
    import sys
    print("Flask not installed. Run: pip install flask")
    sys.exit(1)

app = Flask(__name__)

# --- Configuration ---
ALLOWED_COMMANDS = []          # empty = allow all; e.g. ["ls", "whoami"] to restrict
WORKDIR = "/app"               # working directory inside the container
TIMEOUT_SEC = 30               # per-command timeout

# Simple in-memory history keyed by client IP
_history: dict[str, list[str]] = {}


def run_command(cmd: str) -> dict:
    """Execute a shell command, return structured result."""
    start = time.time()

    if ALLOWED_COMMANDS:
        base = cmd.split()[0] if cmd.split() else ""
        if base not in ALLOWED_COMMANDS:
            return {"error": f"'{base}' not in allowlist", "stdout": "",
                    "stderr": "", "returncode": -1, "elapsed": 0}

    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=TIMEOUT_SEC, cwd=WORKDIR,
        )
        elapsed = round(time.time() - start, 3)
        return {"stdout": r.stdout, "stderr": r.stderr,
                "returncode": r.returncode, "elapsed": elapsed}
    except subprocess.TimeoutExpired:
        return {"error": f"Timed out after {TIMEOUT_SEC}s",
                "stdout": "", "stderr": "", "returncode": -1, "elapsed": TIMEOUT_SEC}
    except Exception as exc:
        return {"error": str(exc), "stdout": "", "stderr": "",
                "returncode": -1, "elapsed": 0}


PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aiven Shell</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#c9d1d9;font-family:'SF Mono','Cascadia Code',
'Fira Code','Consolas',monospace;font-size:14px;height:100vh;
display:flex;flex-direction:column}
#bar{background:#161b22;border-bottom:1px solid #30363d;padding:8px 16px;
display:flex;align-items:center;gap:8px;flex-shrink:0}
.d{width:12px;height:12px;border-radius:50%}
.d.r{background:#f85149}.d.y{background:#d29922}.d.g{background:#3fb950}
#bar span{color:#8b949e;margin-left:8px;font-size:12px}
#out{flex:1;overflow-y:auto;padding:12px 16px;white-space:pre-wrap;
word-break:break-all;line-height:1.6}
.cmd{color:#58a6ff}.err{color:#f85149}.meta{color:#484f58;font-size:12px}
#row{display:flex;border-top:1px solid #30363d;background:#0d1117;flex-shrink:0}
#pr{padding:12px 8px 12px 16px;color:#3fb950;user-select:none}
#in{flex:1;background:transparent;border:none;color:#c9d1d9;font-family:inherit;
font-size:inherit;outline:none;padding:12px 0}
#in::placeholder{color:#484f58}
#go{background:#21262d;border:1px solid #30363d;color:#8b949e;padding:8px 16px;
cursor:pointer;font-family:inherit;font-size:12px}
#go:hover{background:#30363d;color:#c9d1d9}
</style>
</head>
<body>
<div id="bar"><div class="d r"></div><div class="d y"></div><div class="d g"></div>
<span>{{ hostname }}{{ cwd }}</span></div>
<div id="out"></div>
<div id="row"><span id="pr">$</span>
<input type="text" id="in" autofocus placeholder="command..." autocomplete="off"
spellcheck="false">
<button id="go">run</button></div>

<script>
const O=document.getElementById('out'),I=document.getElementById('in'),G=document.getElementById('go');
let H=JSON.parse(localStorage.getItem('ash')||'[]'),hi=-1;
function a(t,c){const d=document.createElement('div');d.className=c;d.textContent=t;O.appendChild(d);O.scrollTop=O.scrollHeight}
function ar(h){const d=document.createElement('div');d.innerHTML=h;O.appendChild(d);O.scrollTop=O.scrollHeight}
async function exe(cmd){
ar('<span class="cmd">$ '+esc(cmd)+'</span>');
const r=await fetch('/exec',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({command:cmd})});
const d=await r.json();
if(d.error)a(d.error,'err');
if(d.stdout)ar(esc(d.stdout));
if(d.stderr&&!d.error)a(d.stderr,'err');
ar('<span class="meta">exit: '+d.returncode+' · '+d.elapsed+'s · '+new Date().toISOString()+'</span>');
if(cmd.trim()){H=[cmd,...H.filter(x=>x!==cmd)].slice(0,100);localStorage.setItem('ash',JSON.stringify(H))}
}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
I.addEventListener('keydown',e=>{
if(e.key==='Enter'){const c=I.value.trim();if(c){exe(c);I.value=''}}
else if(e.key==='ArrowUp'){e.preventDefault();if(hi<H.length-1){hi++;I.value=H[hi]}}
else if(e.key==='ArrowDown'){e.preventDefault();if(hi>0){hi--;I.value=H[hi]}else{hi=-1;I.value=''}}
});
G.addEventListener('click',()=>{const c=I.value.trim();if(c){exe(c);I.value=''}});
ar('<span class="meta">Aiven Shell — authorized container test interface</span>');
ar('<span class="meta">↑ / ↓ : history &nbsp; Enter : execute</span>');
ar('<span class="meta">&nbsp;</span>');
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE,
        hostname=f"@{os.environ.get('HOSTNAME', 'unknown')}",
        cwd=f"  pwd={os.getcwd()}"
    )


@app.route('/exec', methods=['POST'])
def exec_route():
    cmd = (request.get_json().get('command') or '').strip()
    if not cmd:
        return jsonify({"error": "Empty command", "stdout": "", "stderr": "",
                        "returncode": -1, "elapsed": 0})
    ip = request.remote_addr
    _history.setdefault(ip, []).append(cmd)
    return jsonify(run_command(cmd))


@app.route('/history', methods=['GET'])
def history_route():
    ip = request.remote_addr
    return jsonify(history=_history.get(ip, []))


if __name__ == '__main__':
    print(f"Listening on http://0.0.0.0:8080")
    print(f"Allowed commands: {ALLOWED_COMMANDS if ALLOWED_COMMANDS else '(all)'}")
    print(f"Working dir: {WORKDIR}")
    app.run(host='0.0.0.0', port=8080)
