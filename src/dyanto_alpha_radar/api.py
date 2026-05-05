from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

from dyanto_alpha_radar.analyzer import analyze
from dyanto_alpha_radar.report import render_markdown_report

app = FastAPI(title="Dyanto AlphaRadar", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "dyanto-alpha-radar"}


@app.get("/api/scan")
async def api_scan(target: str = Query(..., description="Token address, pair, symbol, or search query")) -> dict:
    return await analyze(target)


@app.get("/report", response_class=PlainTextResponse)
async def report(target: str = Query(...)) -> str:
    result = await analyze(target)
    return render_markdown_report(result) if "error" not in result else str(result)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
<!doctype html>
<html>
<head>
  <title>Dyanto AlphaRadar</title>
  <style>
    body { font-family: Inter, Arial, sans-serif; max-width: 980px; margin: 40px auto; background:#080b12; color:#e8eefc; }
    input { width: 70%; padding: 12px; border-radius: 10px; border:1px solid #334; background:#111827; color:#fff; }
    button { padding: 12px 18px; border:0; border-radius: 10px; background:#4f46e5; color:white; font-weight:700; }
    pre { white-space: pre-wrap; background:#0f172a; border:1px solid #253047; padding:20px; border-radius:16px; }
    .card { background:linear-gradient(135deg,#111827,#0f172a); padding:24px; border-radius:20px; border:1px solid #263149; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Dyanto AlphaRadar</h1>
    <p>Autonomous crypto market intelligence agent for Solana memecoins and DEX opportunities.</p>
    <input id="target" placeholder="Paste token address or search query" />
    <button onclick="scan()">Scan</button>
  </div>
  <h2>Report</h2>
  <pre id="out">Waiting for scan...</pre>
<script>
async function scan(){
  const target = document.getElementById('target').value;
  const out = document.getElementById('out');
  out.textContent = 'Scanning...';
  const res = await fetch('/report?target=' + encodeURIComponent(target));
  out.textContent = await res.text();
}
</script>
</body>
</html>
"""
