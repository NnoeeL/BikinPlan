#!/usr/bin/env python3
"""
BikinPlan Mock Server - Instant Zero-Dependency Mock API Server
Mengimplementasikan formula 'Frontend Mock First' dari BikinPlan.
Membaca kontrak API dari plan.json dan melayani request RESTful lengkap dengan CORS.
Prinsip: Ponytail (100% Python stdlib, zero-dependency, type-safe, runnable verification).
"""

import os
import sys
import json
import re
import urllib.parse
import http.server
import socketserver
import webbrowser
from typing import Dict, Any, List, Optional, Tuple

def find_plan_file(target_path: Optional[str] = None) -> Optional[str]:
    """Mencari berkas plan.json di path yang diberikan atau direktori kerja aktif."""
    candidates = []
    if target_path:
        if os.path.isfile(target_path):
            return os.path.abspath(target_path)
        if os.path.isdir(target_path):
            candidates.append(os.path.join(target_path, "plan.json"))

    cwd = os.getcwd()
    candidates.append(os.path.join(cwd, "plan.json"))
    for sample_dir in ["sample-enterprise", "sample-toko", "sample-portfolio", "sample-saas", "sample-rental", "sample-test"]:
        candidates.append(os.path.join(cwd, sample_dir, "plan.json"))

    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(script_dir, "plan.json"))
    for sample_dir in ["sample-enterprise", "sample-toko", "sample-portfolio", "sample-saas", "sample-rental", "sample-test"]:
        candidates.append(os.path.join(script_dir, sample_dir, "plan.json"))

    for c in candidates:
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None

def load_mock_routes(plan_path: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Membaca plan.json dan mengompilasi daftar endpoint mock."""
    with open(plan_path, "r", encoding="utf-8") as f:
        plan_data = json.load(f)

    raw_contracts = plan_data.get("apiContracts") or plan_data.get("api_contracts") or []
    compiled_routes = []

    for item in raw_contracts:
        method = item.get("method", "GET").upper()
        raw_path = item.get("path", "").strip()
        if not raw_path.startswith("/"):
            raw_path = "/" + raw_path

        # Normalisasi path tanpa trailing slash (kecuali root '/')
        norm_path = raw_path.rstrip("/") if raw_path != "/" else "/"

        # Ubah placeholder URL seperti :id atau {id} menjadi regex
        # contoh: /api/v1/items/:id -> ^/api/v1/items/([^/]+)$
        pattern_str = "^" + re.sub(r'(:[a-zA-Z_0-9]+|\{[a-zA-Z_0-9]+\})', r'([^/]+)', norm_path) + "$"
        regex = re.compile(pattern_str)

        compiled_routes.append({
            "method": method,
            "path": norm_path,
            "raw_path": raw_path,
            "regex": regex,
            "desc": item.get("desc", ""),
            "auth": item.get("auth", "Public"),
            "params": item.get("params", ""),
            "request_body": item.get("request_body"),
            "response_200": item.get("response_200", {"success": True, "message": "Mock OK"})
        })

    return plan_data, compiled_routes

def render_mock_dashboard_html(plan_data: Dict[str, Any], routes: List[Dict[str, Any]]) -> str:
    """Menghasilkan antarmuka web interaktif dark-themed untuk menguji endpoint mock langsung dari browser."""
    project_name = plan_data.get("name", "BikinPlan Project")
    category = plan_data.get("categoryTitle", "Modern Cloud Web Application")
    stack_name = plan_data.get("stack", {}).get("name", "Modern Web Stack")

    rows_html = []
    for idx, r in enumerate(routes):
        method = r["method"]
        badge_color = {
            "GET": "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
            "POST": "bg-blue-500/10 text-blue-400 border-blue-500/20",
            "PUT": "bg-amber-500/10 text-amber-400 border-amber-500/20",
            "DELETE": "bg-rose-500/10 text-rose-400 border-rose-500/20",
            "PATCH": "bg-purple-500/10 text-purple-400 border-purple-500/20"
        }.get(method, "bg-gray-500/10 text-gray-400 border-gray-500/20")

        req_body_json = json.dumps(r["request_body"], indent=2) if r.get("request_body") else ""
        resp_json = json.dumps(r["response_200"], indent=2)

        row = f"""
        <div class="bg-[#121722] border border-[#21293a] rounded-xl p-5 mb-4 shadow-sm hover:border-[#334155] transition-all">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div class="flex items-center gap-3">
              <span class="px-2.5 py-1 text-xs font-mono font-bold rounded-md border {badge_color}">{method}</span>
              <code class="text-sm font-mono font-semibold text-white">{r['path']}</code>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-400 bg-[#1b2234] px-2.5 py-1 rounded-md border border-[#2a344d]">🔒 {r['auth']}</span>
              <button onclick="testEndpoint('{method}', '{r['path']}', {idx})" 
                      class="px-3 py-1.5 text-xs font-medium bg-[#ff5c20] hover:bg-[#ff4500] text-white rounded-lg transition-colors flex items-center gap-1.5 shadow-sm">
                <span>▶️</span> Test Fetch
              </button>
            </div>
          </div>
          
          <p class="text-xs text-slate-300 mb-3">{r['desc']}</p>
          
          {f'''<div class="mb-3">
            <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">Request Body (Mock Payload):</span>
            <pre class="bg-[#0b0e14] p-3 rounded-lg text-xs font-mono text-emerald-300 overflow-x-auto border border-[#1b2234]">{req_body_json}</pre>
          </div>''' if req_body_json else ''}

          <div>
            <div class="flex items-center justify-between mb-1">
              <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Response Mock 200 OK:</span>
              <span id="timing-{idx}" class="text-[11px] font-mono text-slate-500"></span>
            </div>
            <pre id="resp-{idx}" class="bg-[#0b0e14] p-3 rounded-lg text-xs font-mono text-slate-300 overflow-x-auto border border-[#1b2234] max-h-48">{resp_json}</pre>
          </div>
        </div>
        """
        rows_html.append(row)

    routes_rendered = "\n".join(rows_html)

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BikinPlan — Instant Mock Server API Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0a0d14; }}
    code, pre {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
</head>
<body class="text-slate-200 min-h-screen py-8 px-4 sm:px-8">
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <header class="mb-8 pb-6 border-b border-[#21293a] flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-2">
          <span class="text-xl font-black bg-gradient-to-r from-[#ff5c20] to-[#ffa500] bg-clip-text text-transparent">⚡ BikinPlan</span>
          <span class="px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded">Mock API Server Active</span>
        </div>
        <h1 class="text-2xl font-bold text-white">{project_name}</h1>
        <p class="text-sm text-slate-400 mt-1">{category} • <span class="text-slate-300 font-medium">{stack_name}</span></p>
      </div>
      <div class="text-right">
        <div class="text-xs text-slate-400">Total Mock Endpoints:</div>
        <div class="text-2xl font-bold text-emerald-400 font-mono">{len(routes)}</div>
      </div>
    </header>

    <!-- Info Box -->
    <div class="bg-[#121722]/80 border border-emerald-500/20 rounded-xl p-4 mb-6 flex items-start gap-3 text-xs text-slate-300">
      <span class="text-lg">💡</span>
      <div>
        <b class="text-white">Frontend Mock First Mode:</b> Server ini melayani response JSON langsung dengan header CORS (<code class="text-emerald-400">Access-Control-Allow-Origin: *</code>). Frontend kamu dapat langsung memanggil <code class="text-white bg-[#1b2234] px-1.5 py-0.5 rounded">fetch('http://localhost:3333/api/...')</code> di browser sebelum membuat database nyata!
      </div>
    </div>

    <!-- Routes List -->
    <div class="space-y-4">
      {routes_rendered}
    </div>

    <!-- Footer -->
    <footer class="mt-12 pt-6 border-t border-[#21293a] text-center text-xs text-slate-500">
      BikinPlan Instant Mock Server • Zero Dependency Engine • Dibuat untuk AI Coding Agents
    </footer>
  </div>

  <script>
    async function testEndpoint(method, path, idx) {{
      const respEl = document.getElementById('resp-' + idx);
      const timingEl = document.getElementById('timing-' + idx);
      respEl.textContent = 'Memuat request ke ' + path + '...';
      timingEl.textContent = '';
      
      const startTime = performance.now();
      try {{
        const options = {{ method: method, headers: {{ 'Accept': 'application/json' }} }};
        if (method === 'POST' || method === 'PUT' || method === 'PATCH') {{
          options.headers['Content-Type'] = 'application/json';
          options.body = JSON.stringify({{ _clientTest: true, timestamp: new Date().toISOString() }});
        }}
        const res = await fetch(path, options);
        const duration = Math.round(performance.now() - startTime);
        const data = await res.json();
        
        timingEl.innerHTML = `<span class="text-emerald-400 font-bold">${{res.status}} OK</span> • ${{duration}}ms`;
        respEl.textContent = JSON.stringify(data, null, 2);
        respEl.classList.remove('text-slate-300', 'text-rose-400');
        respEl.classList.add('text-emerald-300');
      }} catch (err) {{
        const duration = Math.round(performance.now() - startTime);
        timingEl.innerHTML = `<span class="text-rose-400 font-bold">Error</span> • ${{duration}}ms`;
        respEl.textContent = 'Fetch Error: ' + err.message;
        respEl.classList.remove('text-slate-300', 'text-emerald-300');
        respEl.classList.add('text-rose-400');
      }}
    }}
  </script>
</body>
</html>
"""

def create_mock_handler(plan_data: Dict[str, Any], routes: List[Dict[str, Any]], static_dir: str):
    """Membuat HTTP request handler kelas dinamis yang mengikat rute mock dan static directory."""
    dashboard_html = render_mock_dashboard_html(plan_data, routes).encode("utf-8")

    class BikinPlanHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=static_dir, **kwargs)

        def log_message(self, format, *args):
            # Format log bersih dan terstruktur untuk terminal
            msg = format % args
            # Saring pesan noise favicon
            if "favicon.ico" not in msg:
                sys.stdout.write(f"  [HTTP] {msg}\n")
                sys.stdout.flush()

        def send_cors_headers(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, Accept")
            self.send_header("Access-Control-Max-Age", "86400")

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_cors_headers()
            self.end_headers()

        def match_route(self, method: str, clean_path: str) -> Optional[Dict[str, Any]]:
            for r in routes:
                if r["method"] == method:
                    if r["regex"].match(clean_path):
                        return r
            # Jika method tidak cocok tapi path cocok persis (misal route GET tapi di-POST)
            for r in routes:
                if r["regex"].match(clean_path):
                    return r
            return None

        def handle_api_request(self, method: str):
            parsed = urllib.parse.urlparse(self.path)
            clean_path = parsed.path.rstrip("/") if parsed.path != "/" else "/"

            # 1. Dashboard Mock UI
            if clean_path in ["/__mock", "/mock", "/api", "/api-docs"]:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(dashboard_html)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(dashboard_html)
                return

            # 2. Cari rute mock yang cocok
            matched = self.match_route(method, clean_path)
            if matched:
                # Baca body jika ada
                payload = None
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length > 0:
                    try:
                        raw_body = self.rfile.read(content_length)
                        payload = json.loads(raw_body.decode("utf-8"))
                    except Exception:
                        payload = "<raw binary/unparseable>"

                log_desc = f" ({matched['desc']})" if matched.get("desc") else ""
                print(f"✨ [MOCK {matched['method']}] {clean_path}{log_desc}")
                if payload:
                    payload_preview = str(payload)
                    if len(payload_preview) > 100:
                        payload_preview = payload_preview[:100] + "..."
                    print(f"   Payload Diterima: {payload_preview}")

                response_data = matched["response_200"]
                resp_bytes = json.dumps(response_data, indent=2, ensure_ascii=False).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(resp_bytes)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(resp_bytes)
                return

            # 3. Jika path diawali /api/ tapi tidak terdaftar di plan.json
            if clean_path.startswith("/api/"):
                err_data = {
                    "error": "Endpoint mock tidak ditemukan di plan.json",
                    "requested": {
                        "method": method,
                        "path": clean_path,
                        "query": parsed.query
                    },
                    "hint": "Buka http://localhost:3333/__mock untuk melihat daftar seluruh endpoint yang tersedia.",
                    "available_endpoints": [{"method": r["method"], "path": r["path"], "desc": r["desc"]} for r in routes]
                }
                err_bytes = json.dumps(err_data, indent=2).encode("utf-8")
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(err_bytes)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(err_bytes)
                return

            # 4. Fallback ke file statis jika request GET/HEAD
            if method in ["GET", "HEAD"]:
                super().do_GET()
            else:
                self.send_response(405)
                self.send_cors_headers()
                self.end_headers()

        def do_GET(self):
            self.handle_api_request("GET")

        def do_POST(self):
            self.handle_api_request("POST")

        def do_PUT(self):
            self.handle_api_request("PUT")

        def do_DELETE(self):
            self.handle_api_request("DELETE")

        def do_PATCH(self):
            self.handle_api_request("PATCH")

    return BikinPlanHandler

def start_mock_server(plan_path: Optional[str] = None, port: int = 3333, static_dir: Optional[str] = None, open_browser: bool = True) -> None:
    """Menjalankan mock server HTTP lokal."""
    actual_plan_path = find_plan_file(plan_path)
    if not actual_plan_path:
        print("❌ Berkas plan.json tidak ditemukan. Buat spesifikasi dengan: python cli.py 'Nama Proyek' --idea '...'")
        sys.exit(1)

    plan_data, routes = load_mock_routes(actual_plan_path)
    if not static_dir:
        # Default static dir adalah folder tempat plan.json berada atau direktori saat ini
        plan_folder = os.path.dirname(actual_plan_path)
        script_folder = os.path.dirname(os.path.abspath(__file__))
        static_dir = script_folder if os.path.isfile(os.path.join(script_folder, "index.html")) else plan_folder

    handler_class = create_mock_handler(plan_data, routes, static_dir)

    server_url = f"http://localhost:{port}"
    mock_dashboard_url = f"http://localhost:{port}/__mock"

    print("=" * 74)
    print("⚡ BikinPlan Instant Mock Server (Frontend Mock First Engine)")
    print("=" * 74)
    print(f"📁 Proyek         : {plan_data.get('name', 'BikinPlan Project')}")
    print(f"📄 Sumber Plan    : {actual_plan_path}")
    print(f"🌐 Server URL     : {server_url}")
    print(f"🛠️  Dashboard Mock : {mock_dashboard_url}")
    print(f"📂 Static Root    : {static_dir}")
    print("-" * 74)
    print(f"Daftar Mock Endpoints Aktif ({len(routes)} rute):")
    for r in routes:
        print(f"  [{r['method']:<6}] {r['path']:<28} 🔒 {r['auth']:<15} ({r['desc'][:36]}...)")
    print("-" * 74)
    print("💡 Tips: Panggil endpoint di atas dari kode frontend kamu menggunakan fetch().")
    print("Tekan Ctrl+C untuk menghentikan server.\n")

    if open_browser:
        # Buka dashboard mock di browser
        webbrowser.open(mock_dashboard_url)

    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler_class) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Mock server dihentikan.")
            sys.exit(0)

if __name__ == "__main__":
    target_plan = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
    port_num = 3333
    if "--port" in sys.argv:
        p_idx = sys.argv.index("--port")
        if p_idx + 1 < len(sys.argv):
            port_num = int(sys.argv[p_idx + 1])
    no_browser = "--no-browser" in sys.argv
    start_mock_server(plan_path=target_plan, port=port_num, open_browser=not no_browser)
